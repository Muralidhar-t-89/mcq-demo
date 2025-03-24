from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List


from src.app.schemas import mcq_schema
from src.app.services import mcq_services
from src.app.services.unit_of_work import MCQUnitOfWork

mcq_blueprint = APIRouter()


@mcq_blueprint.get("/mcq", response_model=List[mcq_schema.MCQ])
async def get_all_mcqs() -> List[mcq_schema.MCQ]:
    """
    Endpoint to list all MCQs.

    Returns
    -------
    list[MCQ]
    """
    mcqs = await mcq_services.get_all_mcqs(unit_of_work=MCQUnitOfWork())
    return mcqs


@mcq_blueprint.get("/mcq/{id}", response_model=mcq_schema.MCQ)
async def get_one_mcq(id: int) -> mcq_schema.MCQ:
    """
    Endpoint to retrieve a single MCQ by ID.

    Parameters
    ----------
    id: int

    Returns
    -------
    MCQ
    """
    mcq = await mcq_services.get_single_mcq(mcq_id=id, unit_of_work=MCQUnitOfWork())
    if mcq is None:
        raise HTTPException(status_code=404, detail="MCQ not found")
    return mcq


@mcq_blueprint.post("/mcq", response_model=mcq_schema.MCQ)
async def add_mcq(mcq: mcq_schema.MCQCreate) -> mcq_schema.MCQ:
    """
    Endpoint to add a new MCQ.

    Parameters
    ----------
    mcq: MCQCreate (Request Body)

    Returns
    -------
    MCQ
    """
    created_mcq = await mcq_services.add_mcq(mcq_data=mcq, unit_of_work=MCQUnitOfWork())
    return created_mcq


@mcq_blueprint.put("/mcq/{id}", response_model=mcq_schema.MCQ)
async def update_mcq(id: int, mcq: mcq_schema.MCQUpdate) -> mcq_schema.MCQ:
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
    updated_mcq = await mcq_services.update_mcq(mcq_id=id, mcq_data=mcq, unit_of_work=MCQUnitOfWork())
    if updated_mcq is None:
        raise HTTPException(status_code=404, detail="MCQ not found")
    return updated_mcq


@mcq_blueprint.delete("/mcq/{id}", status_code=204)
async def delete_mcq(id: int):
    """
    Endpoint to delete an MCQ by ID.

    Parameters
    ----------
    id: int (MCQ ID)

    Returns
    -------
    None
    """
    result = await mcq_services.delete_mcq(mcq_id=id, unit_of_work=MCQUnitOfWork())
    if not result:
        raise HTTPException(status_code=404, detail="MCQ not found")
    return JSONResponse(status_code=204, content={"message": "MCQ deleted successfully"})
