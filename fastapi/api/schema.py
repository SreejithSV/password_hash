from pydantic import BaseModel

class HashRequest(BaseModel):
    hash_value: int
