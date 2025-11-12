from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import predict_route
from service_registry import register_gdp_model, deregister_gdp_model
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    register_gdp_model()
    yield
    deregister_gdp_model()


app = FastAPI(lifespan=lifespan)
app.include_router(predict_route.router)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
