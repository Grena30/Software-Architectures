from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import predict_route, model_info
from service_registry import register_gdp_model, deregister_gdp_model
from dotenv import load_dotenv
import uvicorn
import os


load_dotenv()
GDP_MODEL_NAME = os.getenv("GDP_MODEL_NAME", "LinearRegression")


@asynccontextmanager
async def lifespan(app: FastAPI):
    register_gdp_model()
    yield
    deregister_gdp_model()


app = FastAPI(lifespan=lifespan)
app.include_router(predict_route.router)
app.include_router(model_info.router)


@app.get("/health")
def health():
    return {"status": "ok", "model": GDP_MODEL_NAME}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
