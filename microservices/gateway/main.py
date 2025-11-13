from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import predict_route, model_management
import uvicorn


app = FastAPI()
app.include_router(predict_route.router)
app.include_router(model_management.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
