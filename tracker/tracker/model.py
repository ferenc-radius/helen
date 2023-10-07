import asyncio
import logging
import uuid
from asyncio import ensure_future
from datetime import datetime
from multiprocessing import Manager
from typing import List, Optional

from pydantic import BaseModel, IPvAnyAddress

from tracker.settings import get_settings

logger = logging.getLogger(__name__)


class Node(BaseModel):
    uid: str
    ip: IPvAnyAddress
    port: int
    last_seen: datetime


# We use a multiprocessing.Manager to share state between processes
# https://docs.python.org/3/library/multiprocessing.html#sharing-state-between-processes
# The state of the nodes will automatically be recovered by the updates from the nodes
manager = Manager()

initial_data: List[Node] = []
nodes = manager.list(initial_data)


async def register_node(ip: str, port: int, uid: Optional[str] = None) -> Node:
    uid = uid or str(uuid.uuid4())[:8]
    node = Node(uid=uid, ip=ip, port=port, last_seen=datetime.now())
    nodes.append(node)
    return node


async def update_node(uid: str, ip: str, port: int) -> Node:
    node = next((n for n in nodes if n.uid == uid), None)
    if node:
        node.ip = ip
        node.port = port
        node.last_seen = datetime.now()
    else:
        node = await register_node(ip, port, uid)

    return node


async def get_nodes() -> List[Node]:
    return list(nodes)


async def prune_nodes() -> None:
    interval = get_settings().prune_node_interval
    now = datetime.now()
    for node in nodes:
        if (now - node.last_seen).total_seconds() > interval:
            logger.info(f"Pruning node {node.uid}")
            nodes.remove(node)


async def register_node_pruner() -> None:
    """
    Register a background task to prune nodes

    Interval can be set with the env var `PRUNE_NODE_INTERVAL`
    """
    logger.info("Registering node pruner")
    interval = get_settings().prune_node_interval

    async def loop() -> None:
        while True:
            await asyncio.sleep(interval)
            await prune_nodes()

    ensure_future(loop())
