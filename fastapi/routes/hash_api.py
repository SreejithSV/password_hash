from fastapi import APIRouter
from services.hash_service import md5_hash, sha256_hash, ntlm_hash

router = APIRouter(prefix="/api/hash")

@router.post("/md5")
def md5(password: str):
    return {"hash": md5_hash(password)}

@router.post("/sha256")
def sha256(password: str):
    return {"hash": sha256_hash(password)}

@router.post("/ntlm")
def ntlm(password: str):
    return {"hash": ntlm_hash(password)}
