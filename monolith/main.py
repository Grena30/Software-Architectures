from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import model
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Server")
    yield

    print("Shutting Down")


app = FastAPI()
app.include_router(model.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
