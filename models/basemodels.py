from pydantic import BaseModel

class _Credencials(BaseModel):
    email: str
    password: str