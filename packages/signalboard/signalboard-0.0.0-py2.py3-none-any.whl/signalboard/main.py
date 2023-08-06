import multiprocessing

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from signalboard.api import api_app
from signalboard.static import static_app

app = FastAPI(description="API docs can be found under /api/docs")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount('/api', app=api_app)
app.mount('/', app=static_app)


def run(port=5000, reload=False, workers=None):
    max_workers = max(4, (multiprocessing.cpu_count() * 2) + 1)
    uvicorn.run(
        'signalboard.main:app',
        host="0.0.0.0",
        port=port,
        reload=reload,
        workers=workers if workers else max_workers
    )


if __name__ == "__main__":
    run(reload=True)
