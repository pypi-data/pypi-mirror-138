"""Handler for file upload/download."""
import os
from typing import List, Optional, Tuple
import gzip

import tenacity
import httpx

from redbrick_slicer.utils.async_utils import gather_with_concurrency


def uniquify_path(path: str) -> str:
    """Provide unique path with number index."""
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path


async def download_files(files: List[Tuple[str, str]]) -> List[Optional[str]]:
    """Download files from url to local path."""

    @tenacity.retry(
        reraise=True,
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=1, min=1, max=10),
        retry=tenacity.retry_if_not_exception_type(
            (KeyboardInterrupt, PermissionError, ValueError)
        ),
    )
    async def _download_file(url: str, path: str) -> Optional[str]:
        if not url or not path:
            return None
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                path = uniquify_path(path)
                data = response.content
                if response.headers.get("Content-Encoding") == "gzip":
                    try:
                        data = gzip.decompress(data)
                    except Exception:  # pylint: disable=broad-except
                        pass
                with open(path, "wb") as file_:
                    file_.write(data)
                return path
            return None

    coros = [_download_file(url, path) for url, path in files]

    return await gather_with_concurrency(20, coros)
