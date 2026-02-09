from fastapi import FastAPI
from routes import status, hash_api, rainbow_api

app = FastAPI(title="GPU Rainbow Table System")

app.include_router(status.router)
app.include_router(hash_api.router)
app.include_router(rainbow_api.router)
