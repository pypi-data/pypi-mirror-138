from fastapi import FastAPI

from signalboard.modules.classifier.router import classifier_router
from signalboard.modules.dataset.router import dataset_router
from signalboard.modules.health.router import health_router

# api starts with /api/*
api_app = FastAPI()

api_app.include_router(health_router)
api_app.include_router(dataset_router)
api_app.include_router(classifier_router)
