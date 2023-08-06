from typing import List

from fastapi import APIRouter

from signalboard.modules.classifier.model import ClassifierModel

classifier_router = APIRouter(
    prefix="/classifiers",  # /api/dataset
    tags=["Classifier"]
)

MODEL = ClassifierModel


@classifier_router.get("/", response_model=List[MODEL])
async def get_all():
    return MODEL.all()


@classifier_router.get("/{_id}", response_model=MODEL)
async def get_one(_id: str):
    return MODEL.get_by_id(_id)


@classifier_router.get("/{_id}/json_schema", response_model=dict)
async def get_one_json_schema(_id: str):
    return MODEL.get_by_id(_id).json_schema
