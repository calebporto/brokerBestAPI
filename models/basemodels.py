from datetime import date
import datetime
import json
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Json

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
    imobiliaria: Optional[str]
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
    is_complete_data: Optional[bool]
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

class _BasicProject(BaseModel):
    id: Optional[int]
    name: Optional[str]
    thumb: Optional[str]
    delivery_date: Optional[date]
    admin_id: Optional[int]

class _Project(BaseModel):
    id: Optional[int]
    company_id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    delivery_date: Optional[datetime.datetime | date]
    address: Optional[str]
    num: Optional[str]
    complement: Optional[str]
    district: Optional[str]
    zone: Optional[str]
    city: Optional[str]
    uf: Optional[str]
    cep: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    status: Optional[str]
    thumb: Optional[str]
    images: Optional[List[str]]
    videos: Optional[List[str]]
    link: Optional[str]
    book: Optional[str]

class _Property(BaseModel):
    id: Optional[int]
    company_id: Optional[int]
    project_id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    delivery_date: Optional[datetime.datetime | date]
    model: Optional[str]
    measure: Optional[str]
    size: Optional[str]
    price: Optional[float]
    status: Optional[str]
    thumb: Optional[str]
    images: Optional[List[str]]
    videos: Optional[List[str]]

class _Company(BaseModel):
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    email: Optional[str]
    tel: Optional[str]
    address: Optional[str]
    num: Optional[str]
    complement: Optional[str]
    district: Optional[str]
    city: Optional[str]
    uf: Optional[str]
    cep: Optional[str]
    thumb: Optional[str]
    images: Optional[List[str]]
    admin_id: Optional[int]
    is_active: bool = True

class _ProjectView(BaseModel):
    project: Optional[_Project]
    company: Optional[_Company]
    properties: Optional[List[_Property]]

class _PremiumCompanyData(BaseModel):
    id: int
    name: str

class _PremiumQuery(BaseModel):
    premiumList: List[_PremiumCompanyData]
    companyList: List[_PremiumCompanyData]