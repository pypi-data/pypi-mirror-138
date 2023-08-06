"""Async utils."""
import asyncio
from typing import Awaitable, List, TypeVar, Iterable

ReturnType = TypeVar("ReturnType")


async def gather_with_concurrency(
    max_concurrency: int, tasks: Iterable[Awaitable[ReturnType]]
) -> List[ReturnType]:
    """Utilizes a Semaphore to limit concurrency to n."""
    if not tasks:
        return []

    semaphore = asyncio.Semaphore(max_concurrency)

    async def sem_task(task: Awaitable[ReturnType]) -> ReturnType:
        async with semaphore:
            return await task

    coros = [sem_task(task) for task in tasks]

    return await asyncio.gather(*coros)
