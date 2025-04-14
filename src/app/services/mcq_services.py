import pandas as pd
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List

from src.app.entities.mcq import MCQ
from src.app.repositories.category_repository import CategoryRepository
from src.app.repositories.mcq_repository import MCQRepository
from src.app.schemas.mcq_schema import MCQCreate, MCQUpdate
from src.app.services.unit_of_work import MCQUnitOfWork


class MCQService:
    def __init__(self, session: Session):
        self.repository = MCQRepository(session)

    async def get_all_mcqs(self) -> List[MCQ]:
        """
        Get all MCQs from the database.
        """
        result = self.repository.get_all()
        mcq_dict = [mcq.to_dict() for mcq in result]
        return mcq_dict

    async def get_single_mcq(self, mcq_id: int) -> MCQ | None:
        """
        Get a single MCQ by its ID.
        """
        mcq_by_id = self.repository.get_one(mcq_id)
        if mcq_by_id:
            return mcq_by_id.to_dict()
        return None

    async def add_mcq(self, mcq_data, unit_of_work: MCQUnitOfWork, admin_user) -> MCQ:
        """
        Add a new MCQ to the database. This function checks for duplicates in the database before adding a new MCQ.
        """
        mcq = mcq_data.model_dump()

        # Fetching category from DB!
        category_repo = CategoryRepository(unit_of_work.session)
        category = category_repo.get_one(mcq_data.category)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        mcq["created_by"] = admin_user.id
        mcq["created_date"] = datetime.now()
        mcq["category"] = category.id

        mcq = MCQ(**mcq)
        print("mcq after creation:", mcq)

        mcq_question = mcq.question.strip().lower()

        mcq_options = sorted([option.strip().lower() for option in mcq.options])

        # Add the new MCQ to the database and commit it
        with unit_of_work:
            existing_mcqs = unit_of_work.session.query(MCQ).filter(func.lower(MCQ.question) == mcq_question).all()

            for existing_mcq in existing_mcqs:
                existing_options = sorted([option.strip().lower() for option in existing_mcq.options])

                # Check if the question and options match
                if mcq_question.lower() == existing_mcq.question.lower():
                    if mcq_options == existing_options:
                        raise HTTPException(
                            status_code=400,
                            detail="Duplicate MCQ exists with the same question and options"
                        )

            unit_of_work.mcq_repo.add(mcq)
            unit_of_work.session.flush()
            unit_of_work.session.refresh(mcq)

            result = mcq.to_dict()
            unit_of_work.commit()

        return result

    async def update_mcq(self, mcq_id: int, mcq_data: MCQUpdate, unit_of_work: MCQUnitOfWork, admin_user):
        """
        Update an existing MCQ in the database.
        """
        with unit_of_work:
            existing_mcq = self.repository.get_one(mcq_id)
            if not existing_mcq:
                return None
            existing_mcq.question = mcq_data.question
            existing_mcq.options = mcq_data.options
            existing_mcq.correct_option = mcq_data.correct_option
            existing_mcq.category = mcq_data.category
            existing_mcq.updated_by = admin_user.id
            existing_mcq.updated_date = datetime.now()

            unit_of_work.mcq_repo.update(existing_mcq)

            result = existing_mcq.to_dict()
            unit_of_work.session.commit()

            return result

    async def delete_mcq(self, mcq_id: int) -> bool:
        """
        Delete an MCQ from the database by its ID.
        """
        return self.repository.delete(mcq_id)

    @staticmethod
    def bulk_upload_csv(file, admin_user, unit_of_work: MCQUnitOfWork) -> dict:
        """
        Bulk upload MCQs from a CSV file. This function handles duplicate checking of MCQs both in CSV
        and in database, and also handles errors during the upload process.
        """
        try:
            df = pd.read_csv(file.file)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading CSV: {str(e)}")

        # Validate required columns
        required_columns = {"sno", "Question", "Options", "Correct_options", "Category"}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise HTTPException(status_code=400, detail=f"Missing required columns: {missing_columns}")

        total_questions = len(df)
        existing_mcqs = set()
        duplicate_mcqs_in_csv = 0
        duplicate_mcqs_in_db = 0
        successful_inserts = 0
        failed_records = []

        with unit_of_work as uow:
            session = uow.session
            mcq_repo = MCQRepository(session)
            category_repo = CategoryRepository(session)

            for _, row in df.iterrows():
                question = row["Question"].strip()
                try:
                    options = eval(row["Options"])  # Convert string to list
                    correct_options = eval(row["Correct_options"])  # Convert string to list
                    category_id = int(row["Category"])
                except Exception as e:
                    failed_records.append({"question": question, "error": f"Bad format:{str(e)}"})
                    continue

                question_cmp = question.lower()
                options_cmp = sorted([option.strip().lower() for option in options])
                correct_options_cmp = frozenset([option.strip().lower() for option in correct_options])

                # Build a duplicate key from the current row
                key = (question_cmp, frozenset(options_cmp), correct_options_cmp)
                if key in existing_mcqs:
                    duplicate_mcqs_in_csv += 1
                    continue  # Skip duplicate within CSV
                existing_mcqs.add(key)

                # Check if an MCQ with same question and options already exists
                existing_mcq = mcq_repo.get_by_question_and_options(question_cmp, options_cmp)
                print("existing_mcq:", existing_mcq)
                if existing_mcq:
                    duplicate_mcqs_in_db += 1
                    continue  # Skip duplicate found in DB

                # Fetch the category from DB
                category_obj = category_repo.get_one(category_id)
                if not category_obj:
                    failed_records.append({"question": question, "error": "Category not found"})
                    continue

                try:
                    mcq_data = MCQCreate(
                        question=question,
                        options=options,
                        correct_option=correct_options,
                        category=category_id
                    )

                    # Prepare data for insertion
                    mcq_data = mcq_data.model_dump()
                    mcq_data["created_by"] = admin_user.id
                    mcq_data["created_date"] = datetime.now()
                    mcq_data["category"] = category_obj.id

                    new_mcq = MCQ(**mcq_data)
                    print("new_mcq:", new_mcq)
                    session.add(new_mcq)
                    session.flush()
                    session.refresh(new_mcq)
                    successful_inserts += 1

                except Exception as e:
                    failed_records.append({"question": question, "error": str(e)})

            uow.commit()

        if successful_inserts == 0 and (duplicate_mcqs_in_csv + duplicate_mcqs_in_db) == total_questions:
            message = "All records are duplicates"
        elif duplicate_mcqs_in_csv + duplicate_mcqs_in_db == 0:
            message = "All records inserted successfully"
        elif duplicate_mcqs_in_csv > 0:
            message = f"Bulk upload completed with {duplicate_mcqs_in_csv} duplicates in CSV"
        elif duplicate_mcqs_in_db > 0:
            message = f"Bulk upload completed with {duplicate_mcqs_in_db} duplicates in DB"
        elif failed_records:
            message = "Bulk upload completed with some errors"
        else:
            message = "Bulk upload successful"

        return {
            "message": message,
            "total_questions": total_questions,
            "uploaded_count": successful_inserts,
            "duplicate_questions_in_csv": duplicate_mcqs_in_csv,
            "duplicate_questions_in_db": duplicate_mcqs_in_db,
            "failed_count": len(failed_records),
            "errors": failed_records
        }
