from typing import Annotated

from fastapi import APIRouter, Depends

from tracker.routers.dto import StatusResponse, VersionInfoResponse
from tracker.settings import Settings, get_settings

router = APIRouter()


@router.get("/ready", include_in_schema=False)  # hide this endpoint from swagger
async def ready() -> StatusResponse:
    return {"status": "Running"}


@router.get("/health", include_in_schema=False)  # hide this endpoint from swagger
async def health() -> StatusResponse:
    return {"status": "Running"}


@router.get("/version", description="Get the version of the API")
async def version(settings: Annotated[Settings, Depends(get_settings)]) -> VersionInfoResponse:
    return {"version": settings.version}
