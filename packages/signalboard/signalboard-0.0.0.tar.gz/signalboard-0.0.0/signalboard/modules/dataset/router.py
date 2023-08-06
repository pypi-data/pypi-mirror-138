from typing import List

from fastapi import APIRouter

from signalboard.modules.dataset.model import DatasetModel

dataset_router = APIRouter(
    prefix="/datasets",  # /api/dataset
    tags=["Dataset"]
)

MODEL = DatasetModel


@dataset_router.get("/", response_model=List[MODEL])
async def get_all():
    return MODEL.all()


@dataset_router.get("/{_id}", response_model=MODEL)
async def get_one(_id: str):
    return MODEL.get_by_id(_id)


@dataset_router.get("/{_id}/json_schema", response_model=dict)
async def get_one_json_schema(_id: str):
    return MODEL.get_by_id(_id).json_schema
