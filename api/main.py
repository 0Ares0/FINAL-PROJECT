import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import index as indexRoute
from .models import model_loader
from .dependencies.config import conf

app = FastAPI(
    title="Restaurant Ordering System",
    description="API for managing sandwich orders, menu, resources, and recipes.",
    version="1.0.0",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)

if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)
