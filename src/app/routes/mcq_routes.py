from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from typing import List

from src.app.common.utils import get_current_user
from src.app.schemas import mcq_schema
from src.app.services.mcq_services import MCQService
from src.app.services.unit_of_work import MCQUnitOfWork

mcq_blueprint = APIRouter()

uow = MCQUnitOfWork()
mcq_service = MCQService(session=uow.session)


@mcq_blueprint.get("/mcq", response_model=List[mcq_schema.MCQ])
async def get_all_mcqs() -> List[mcq_schema.MCQ]:
    """
    Endpoint to list all MCQs.

    Returns
    -------
    list[MCQ]
    """
    with uow:
        mcqs = await mcq_service.get_all_mcqs()
        print("MCQs retrieved successfully..!")
        return mcqs


@mcq_blueprint.get("/mcq/{id}", response_model=mcq_schema.MCQ)
async def get_one_mcq(id: int) -> mcq_schema.MCQ | None:
    """
    Endpoint to retrieve a single MCQ by ID.

    Parameters
    ----------
    id: int

    Returns
    -------
    list[MCQ]
    """
    mcq = await mcq_service.get_single_mcq(mcq_id=id)
    if mcq is None:
        raise HTTPException(status_code=404, detail="MCQ not found")
    return mcq


@mcq_blueprint.post("/mcq", response_model=mcq_schema.MCQ)
async def add_mcq(mcq: mcq_schema.MCQCreate,
                  admin_user: dict = Depends(get_current_user)) -> mcq_schema.MCQ:
    """
    Endpoint to add a new MCQ only by admin users.

    Parameters
    ----------
    mcq: MCQCreate (Request Body)

    Returns
    -------
    MCQ
    """
    if admin_user.role != 1:
        print("Admin access required")
        raise HTTPException(status_code=403, detail="Admin access required")

    created_mcq = await mcq_service.add_mcq(mcq_data=mcq, unit_of_work=uow, admin_user=admin_user)
    return created_mcq


@mcq_blueprint.put("/mcq/{id}", response_model=mcq_schema.MCQ)
async def update_mcq(id: int, mcq: mcq_schema.MCQUpdate,
                     admin_user: dict = Depends(get_current_user)) -> mcq_schema.MCQ:
    """
    Endpoint to update an existing MCQ by ID.

    Parameters
    ----------
    id: int (MCQ ID)
    mcq: MCQUpdate (Request Body)

    Returns
    -------
    MCQ
    """
    if admin_user.role != 1:
        raise HTTPException(status_code=403, detail="Admin access required")

    updated_mcq = await mcq_service.update_mcq(mcq_id=id, mcq_data=mcq,
                                               unit_of_work=uow,
                                               admin_user=admin_user)
    if updated_mcq is None:
        raise HTTPException(status_code=404, detail="MCQ not found")
    return updated_mcq


@mcq_blueprint.delete("/mcq/{id}", status_code=204)
async def delete_mcq(id: int, admin_user: dict = Depends(get_current_user)):
    """
    Endpoint to delete an MCQ by ID.

    Parameters
    ----------
    id: int (MCQ ID)

    Returns
    -------
    None
    """
    if admin_user.role != 1:
        raise HTTPException(status_code=403, detail="Admin access required")

    result = await mcq_service.delete_mcq(mcq_id=id)

    if not result:
        raise HTTPException(status_code=404, detail="MCQ not found")
    return JSONResponse(status_code=200, content={"message": "MCQ deleted successfully"})


@mcq_blueprint.post("/mcq/bulk-upload")
async def bulk_upload_mcqs(file: UploadFile = File(...), admin_user: dict = Depends(get_current_user)):
    """
    Bulk upload MCQs via CSV file with error skipping.
    """
    if admin_user.role != 1:
        raise HTTPException(status_code=403, detail="Admin access required")

    try:
        result = MCQService.bulk_upload_csv(file, admin_user, uow)
        print("result:", result)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")
