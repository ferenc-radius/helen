from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import ORJSONResponse

from settings import Settings, get_settings

app = FastAPI(default_response_class=ORJSONResponse)


@app.get("/")
async def root(settings: Annotated[Settings, Depends(get_settings)]):
    return {"message": "Hello world"}
