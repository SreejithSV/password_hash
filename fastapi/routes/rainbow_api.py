from fastapi import APIRouter
from services.rainbow_cpu import generate_rainbow, lookup

router = APIRouter(prefix="/api/rainbow")

@router.post("/generate")
def generate():
    passwords = ["admin", "password", "hello123", "welcome"]
    count = generate_rainbow(passwords)
    return {"entries": count, "status": "completed"}

@router.post("/lookup")
def find(hash: str):
    pwd = lookup(hash)
    return {"password": pwd or "not found"}
