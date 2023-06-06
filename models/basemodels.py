from typing import Optional
from pydantic import BaseModel, EmailStr

class _Credencials(BaseModel):
    alternative_id: Optional[str]
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]

class _New_User(BaseModel):
    alternative_id: Optional[str]
    nome: Optional[str]
    email: Optional[str]
    tel: Optional[str]
    cep: Optional[str]
    hash: Optional[str]
    endereco: Optional[str]
    num: Optional[str]
    complemento: Optional[str]
    bairro: Optional[str]
    cidade: Optional[str]
    uf: Optional[str]
    password: Optional[str]
    provider: Optional[int]
    access_token: Optional[str]
    refresh_token: Optional[str]
    is_admin: Optional[bool]
    is_authenticated: Optional[bool]

class MagicLink(BaseModel):
    identifier: EmailStr
    payload: dict