import asyncio
import logging
from datetime import datetime

from tracker.model import nodes
from tracker.settings import get_settings

logger = logging.getLogger(__name__)


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

    asyncio.ensure_future(loop())
