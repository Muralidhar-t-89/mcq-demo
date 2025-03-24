from sqlalchemy.orm import Session
from typing import List

from src.app.entities.mcq import MCQ
from src.app.repositories.mcq_repository import MCQRepository
from src.app.schemas.mcq_schema import MCQCreate, MCQUpdate


class MCQService:
    def __init__(self, session: Session):
        self.repository = MCQRepository(session)

    async def get_all_mcqs(self) -> List[MCQ]:
        return self.repository.get_all()

    async def get_single_mcq(self, mcq_id: int) -> MCQ:
        return self.repository.get_one(mcq_id)

    async def add_mcq(self, mcq_data: MCQCreate) -> MCQ:
        mcq = MCQ(**mcq_data.model_dump())
        self.repository.add(mcq)
        return mcq

    async def update_mcq(self, mcq_id: int, mcq_data: MCQUpdate):
        existing_mcq = self.repository.get_one(mcq_id)
        if existing_mcq:
            updated_mcq = MCQ(**mcq_data.model_dump(), id=mcq_id)
            self.repository.update(updated_mcq)
            return updated_mcq
        return None

    async def delete_mcq(self, mcq_id: int) -> bool:
        return self.repository.delete(mcq_id)

    async def bulk_add_mcqs(self, mcqs_data: List[MCQCreate]) -> List[MCQ]:
        mcqs = [MCQ(**data.model_dump()) for data in mcqs_data]
        for mcq in mcqs:
            self.repository.add(mcq)
        return mcqs
