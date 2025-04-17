import random
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.app.entities.quiz_attempt import QuizAttempt
from src.app.entities.quiz_attempt_questions import AttemptQuestion
from src.app.repositories.mcq_repository import MCQRepository
from src.app.repositories.quiz_attempt_repository import QuizAttemptRepository
from src.app.repositories.quiz_attempt_question_repository import AttemptQuestionRepository
from src.app.repositories.category_repository import CategoryRepository
from src.app.schemas.quiz_schema import QuizSubmitRequest
from src.app.common.utils import generate_unique_attempt_id
from src.app.services.unit_of_work import MCQUnitOfWork


class QuizService:
    def __init__(self, session):
        self.mcq_repo = MCQRepository(session)
        self.attempt_repo = QuizAttemptRepository(session)
        self.attempt_q_repo = AttemptQuestionRepository(session)
        self.category_repo = CategoryRepository(session)
        self.session = session

    def start_quiz(self, user_id: int, category_id: int) -> dict:
        """
        Starts a quiz for the user by fetching random MCQs from the specified category.
        """
        mcqs = self.mcq_repo.get_by_category(category_id)
        if not mcqs:
            raise HTTPException(status_code=404, detail="No questions found for this category")

        # generate unique 6-digit attempt ID
        attempt_id = generate_unique_attempt_id(self.attempt_repo)
        print("Attempt ID:", attempt_id)

        # fetch 25 MCQs randomly
        selected_mcqs = random.sample(mcqs, min(len(mcqs), 25))

        questions = [
            {"id": q.id, "question": q.question, "options": q.options}
            for q in selected_mcqs
        ]
        return {"attempt_id": attempt_id, "questions": questions}

    def submit_quiz(self, user_id: int, payload: QuizSubmitRequest) -> dict:
        """
        Submits the quiz attempt and calculates the score.
        """
        print("payload:", payload)
        # Ensure category exists
        if not self.category_repo.get_one(payload.category_id):
            raise HTTPException(status_code=404, detail="Category not found")

        # total = 25 (or fewer if less MCQs exist)
        all_mcqs = self.mcq_repo.get_by_category(payload.category_id)
        total_questions = min(len(all_mcqs), 25)

        with MCQUnitOfWork() as uow:
            session = uow.session

            qa = QuizAttempt(
                user_id=user_id,
                attempt_id=payload.attempt_id,
                category_id=payload.category_id,
                total_questions=total_questions,
                questions_attempted=0,
                questions_unattempted=total_questions,
                correct_answers=0,
                score=0,
                created_date=datetime.now()
            )
            print("quiz attempt:", qa)
            session.add(qa)
            try:
                session.flush()
            except IntegrityError as e:
                if 'quiz_attempts_attempt_id_key' in str(e.orig):
                    raise HTTPException(
                        status_code=409,
                        detail="A quiz with this attempt_id already exists. Please retry to start a new quiz."
                    )
                raise HTTPException(
                    status_code=500,
                    detail="Failed to record quiz attempt. Please try again later."
                )

            # map of question_id with correct_option list
            mcq_map = {q.id: q.correct_option for q in all_mcqs}

            attempted = 0
            correct = 0

            for ans in payload.answers:
                if not ans.answer:
                    continue
                attempted += 1
                correct_options = mcq_map.get(ans.question_id, [])

                # submitted answer and correct options to lower case for comparison
                is_corr = ans.answer.strip().lower() in [option.strip().lower for option in correct_options]
                if is_corr:
                    print("is_corr:", is_corr)
                    correct += 1

                aq = AttemptQuestion(
                    attempt_id=payload.attempt_id,
                    question_id=ans.question_id,
                    attempted_answer=ans.answer,
                    is_correct=is_corr
                )
                session.add(aq)

            wrong = attempted - correct
            unattempted = total_questions - attempted
            score = correct * 4  # 4 marks per correct answer

            # Update the QuizAttempt row
            qa.questions_attempted = attempted
            qa.questions_unattempted = unattempted
            qa.correct_answers = correct
            qa.score = score

            session.commit()

        return {
            "attempt_id": payload.attempt_id,
            "total_questions": total_questions,
            "questions_attempted": attempted,
            "questions_unattempted": unattempted,
            "correct_answers": correct,
            "wrong_answers": wrong,
            "score": score
        }

    def get_user_attempts(self, current_user) -> list[dict]:
        """
        If admin user_id is passed, fetches all quiz attempts made by all users.
        Otherwise: return only the attempts belonging to the current user.
        """
        if current_user.role == 1:
            attempts = self.attempt_repo.get_all()
        else:
            attempts = self.attempt_repo.get_by_user(current_user.id)
        print("attempts:", attempts)
        return [a.to_dict() for a in attempts]
