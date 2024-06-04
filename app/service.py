from langchain_core.runnables.history import RunnableWithMessageHistory
from sse_starlette import EventSourceResponse
from langserve.serialization import WellKnownLCSerializer

from typing import (AsyncIterator)
import json

from schemas import Input

async def stream(runnable:RunnableWithMessageHistory, input:Input) -> EventSourceResponse:
    async def _stream(runnable:RunnableWithMessageHistory, input:Input) -> AsyncIterator[dict]:
        """Stream the output of the runnable."""
        _serializer = WellKnownLCSerializer()
        try:
            async for chunk in runnable.astream(input):
                yield {
                    # EventSourceResponse expects a string for data
                    # so after serializing into bytes, we decode into utf-8
                    # to get a string.
                    "data": _serializer.dumps(chunk).decode("utf-8"),
                    "event": "data",
                }
            yield {"event": "end"}
        except BaseException:
            yield {
                "event": "error",
                # Do not expose the error message to the client since
                # the message may contain sensitive information.
                # We'll add client side errors for validation as well.
                "data": json.dumps(
                    {"status_code": 500, "message": "Internal Server Error"}
                ),
            }
            raise

    return EventSourceResponse(_stream(runnable, input))