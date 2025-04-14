from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List

from src.app.schemas import category_schema
from src.app.services import category_services
from src.app.services.unit_of_work import MCQUnitOfWork
from src.app.common.utils import get_current_user

category_blueprint = APIRouter()


@category_blueprint.get("/category", response_model=List[category_schema.Category])
def get_all_categories() -> List[category_schema.Category]:
    """
    Endpoint to list all categories.
    """
    with MCQUnitOfWork() as uow:
        categories = category_services.get_all_categories(unit_of_work=uow)
    return categories


@category_blueprint.get("/category/{id}", response_model=category_schema.Category)
async def get_one_category(id: int) -> category_schema.Category:
    """
    Endpoint to retrieve a single category by ID.
    """
    with MCQUnitOfWork() as uow:
        category = await category_services.get_category_by_id(category_id=id, unit_of_work=uow)
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")
    return category


@category_blueprint.post("/category", response_model=category_schema.Category)
async def add_category(category: category_schema.CategoryCreate,
                       current_user=Depends(get_current_user)) -> category_schema.Category:
    """
    Endpoint to add a new category (Admin only).
    """
    print("current_user:", current_user)
    if current_user.role != 1:
        raise HTTPException(status_code=403, detail="Admin access required")

    created_category = await category_services.create_category(
        category_data=category,
        admin_user=current_user,
        unit_of_work=MCQUnitOfWork()
    )
    return created_category


@category_blueprint.put("/category/{id}", response_model=category_schema.Category)
async def update_category(id: int,category: category_schema.CategoryUpdate,
        current_user=Depends(get_current_user)) -> category_schema.Category:
    """
    Endpoint to update an existing category by ID (Admin only).
    """
    if current_user.role != 1:
        raise HTTPException(status_code=403, detail="Admin access required")

    updated_category = await category_services.update_category(
        category_id=id,
        category_data=category,
        admin_user=current_user,
        unit_of_work=MCQUnitOfWork()
    )
    if updated_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category


@category_blueprint.delete("/category/{id}")
async def delete_category(id: int, current_user=Depends(get_current_user)) -> JSONResponse:
    """
    Endpoint to delete a category by ID (Admin only).
    """
    if current_user.role != 1:
        raise HTTPException(status_code=403, detail="Admin access required")

    result = await category_services.delete_category(
        category_id=id,
        admin_user=current_user,
        unit_of_work=MCQUnitOfWork()
    )
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    return JSONResponse(status_code=200, content={"message": "Category deleted successfully"})
