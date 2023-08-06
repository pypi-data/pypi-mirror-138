from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import Response, RedirectResponse
from starlette.types import Scope


class CustomStaticFiles(StaticFiles):

    async def get_response(self, path: str, scope: Scope) -> Response:
        r = await super().get_response(path, scope)
        if r.status_code == 404:
            # if file not found, then it is probably react frontend route
            return RedirectResponse('/')
        return r


static_app = FastAPI()

static_path = Path(__file__).parent.joinpath('app')
if not static_path.exists():
    static_path.mkdir(exist_ok=True)

index_path = static_path.joinpath('index.html')
if not index_path.exists():
    with static_path.joinpath('index.html').open('w') as f:
        f.write('Frontend app not build correctly')

static_app.mount('/', CustomStaticFiles(directory=str(static_path), html=True))
