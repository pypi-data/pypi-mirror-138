"""URL parsing library for the tool."""
from typing import Tuple


def tool_url_parse(url: str) -> Tuple[str, str, str, str]:
    """Parse a tool url to all of the sub data."""
    if ".com/" in url:
        path = url.split(".com/")[1]
    if "localhost" in url:
        path = url.split("localhost:3000/")[1]

    patha = path.split("?")[0]
    querystring = path.split("?")[1]
    taskid = querystring.replace("taskid=", "")
    projectid = patha.split("/")[2]
    orgid = patha.split("/")[0]
    stagename = patha.split("/")[4]

    return (orgid, projectid, taskid, stagename)


def generate_task_url(url: str) -> str:
    """Generate task modal url."""
    pos = url.index("/projects/")
    from_index = url.index("/", pos + 10) + 1
    to_index = url.index("?", from_index + 1)
    return url[:from_index] + "data/all/all" + url[to_index:]
