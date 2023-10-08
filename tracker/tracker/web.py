from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import ORJSONResponse

from tracker import prune
from tracker.routers import nodes, status
from tracker.settings import Settings, get_settings

app = FastAPI(
    default_response_class=ORJSONResponse,
    title="Tracker",
    version=get_settings().version,
    # TODO inject contact info from env vars
    # contact={},
    # license_info="MIT",
)


app.on_event("startup")(prune.register_node_pruner)


app.include_router(nodes.router, prefix="/nodes", tags=["nodes"])
app.include_router(status.router, prefix="/status", tags=["status"])


@app.get("/")
async def root(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    return {"message": "Welcome to the Tracker API"}
