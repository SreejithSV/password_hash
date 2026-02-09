import hashlib
from passlib.hash import nthash

def md5_hash(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

def sha256_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def ntlm_hash(password: str) -> str:
    return nthash.hash(password)
