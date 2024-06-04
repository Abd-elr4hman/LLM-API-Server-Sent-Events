from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from schemas import Input

from service import stream
from chain import get_chain

app = FastAPI()
chain = get_chain()

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

@app.post("/api/v1/stream")
async def stream_output(input:Input):
    return await stream(chain, input)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
