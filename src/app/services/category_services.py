from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from src.app.schemas.category_schema import CategoryCreate, CategoryUpdate
from src.app.services.unit_of_work import MCQUnitOfWork
from src.app.entities.category import Category


def get_all_categories(unit_of_work: MCQUnitOfWork) -> list[Category]:
    with unit_of_work as uow:
        categories = uow.category_repo.get_all()
        print("categories:", categories)
        result = [category.to_dict() for category in categories]
    return result


async def get_category_by_id(category_id: int, unit_of_work: MCQUnitOfWork) -> Category | None:
    async with unit_of_work as uow:
        category = await uow.category_repo.get_by_id(category_id)
        return category.to_dict() if category else None


async def create_category(category_data: CategoryCreate, admin_user, unit_of_work: MCQUnitOfWork) -> Category:

    new_category = Category(
        name=category_data.name,
        created_by=admin_user.id,
        created_date=datetime.now(),
    )
    print("new_category:", new_category)

    with unit_of_work as uow:
        try:
            created_category = uow.category_repo.add(new_category)
            uow.commit()
            return created_category.to_dict()
        except SQLAlchemyError:
            uow.rollback()
            raise HTTPException(status_code=500, detail="Failed to create category")


async def update_category(category_id: int, category_data: CategoryUpdate, admin_user,
                          unit_of_work: MCQUnitOfWork) -> Category | None:

    with unit_of_work as uow:
        category = uow.category_repo.get_one(category_id)
        print("category:", category)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        category.name = category_data.name
        category.updated_by = admin_user.id
        category.updated_date = datetime.now()

        try:
            updated_category = uow.category_repo.update(category)
            print("updated_category:", updated_category)
            uow.commit()
            return updated_category.to_dict() if updated_category else None
        except SQLAlchemyError:
            uow.rollback()
            raise HTTPException(status_code=500, detail="Failed to update category")


async def delete_category(category_id: int, admin_user, unit_of_work: MCQUnitOfWork) -> bool:

    with unit_of_work as uow:
        category = uow.category_repo.get_one(category_id)
        print("got the category:", category)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        try:
            result = uow.category_repo.delete(category_id)
            print("result:", result)
            uow.commit()
            return result
        except SQLAlchemyError:
            uow.rollback()
            raise HTTPException(status_code=500, detail="Failed to delete category")
