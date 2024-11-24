from fastapi import FastAPI

from handlers import routers

app = FastAPI()

for router in routers:
    app.include_router(router)


@app.get("/")
def read_root():
    """
        This endpoint returns a simple JSON message.

        The purpose of this endpoint is to provide a simple way to test
        whether the FastAPI application is online and responding to
        requests.

        The response is a JSON object with a single key-value pair.
    The key is "Hello", and the value is "World".
    """
    return {"Hello": "World"}

