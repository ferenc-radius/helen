import logging
import uuid
from datetime import datetime
from multiprocessing import Manager
from typing import List, Optional

from pydantic import BaseModel, IPvAnyAddress

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
