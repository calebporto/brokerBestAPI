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
    is_data_complete: Optional[bool]
    is_admin: Optional[bool]

class MagicLink(BaseModel):
    identifier: EmailStr
    payload: dict

class _Auth_Email(BaseModel):
    alternative_id: Optional[str]
    name: Optional[str]
    email: Optional[str]
    is_authenticated: Optional[str]

class _Send_New_Password(BaseModel):
    email: str

class _Password_Token_Validate(BaseModel):
    type: str
    token: Optional[str]
    hash: Optional[str]
    email: Optional[str]

class _Response(BaseModel):
    status: int
    body: str | dict | list