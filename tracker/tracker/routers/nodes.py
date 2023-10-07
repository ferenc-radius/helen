from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Path

from tracker import model
from tracker.routers.dto import NodeRequestBody, NodeResponse

router = APIRouter()


@router.post("/")
async def register_node(body: NodeRequestBody) -> NodeResponse:
    node = await model.register_node(body.ip, body.port)
    return node


@router.put("/{node_id}", description="Will register the node if it does not exist anymore")
async def update_node(node_id: Annotated[str, Path(min_length=8, max_length=8)], body: NodeRequestBody) -> NodeResponse:
    node = await model.update_node(node_id, body.ip, body.port)
    return node


@router.get("/")
async def get_nodes() -> list[NodeResponse]:
    return await model.get_nodes()
