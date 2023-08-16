from json import dumps
import os
from typing import List, Optional
from fastapi import APIRouter, Response
from models.basemodels import _Company, _PremiumCompanyData, _Project, _Property
from services.project_services import _add_company, _add_project, _add_property, _changePremium, _company_delete, _company_edit, _get_companies, _get_company_by_id, _get_premium_projects, _get_premium_query, _get_project_by_id, _get_project_names, _get_projects, _get_projects_by_position, _project_delete, _project_edit, _property_delete
from botocore.exceptions import ClientError
import boto3

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

router = APIRouter(prefix='/project-services')


@router.get('/get-project-names')
async def get_project_names(filter: str = None):
    return await _get_project_names(filter)


@router.get('/get-projects')
async def get_projects(
    filterBy: str,
    key: str,
    orderBy: str,
    offset: str | int,
    guidance: str
):

    return await _get_projects(filterBy, key, orderBy, offset, guidance)


@router.get('/get-premium-projects')
async def get_premium_projects():
    return await _get_premium_projects()


@router.get('/get-project-by-id')
async def get_project_by_id(id: int):
    return await _get_project_by_id(id)


@router.get('/get-companies')
async def get_companies(userEmail: str):
    return await _get_companies(userEmail)


@router.post('/add-company')
async def add_company(newCompany: _Company):
    return await _add_company(newCompany)


@router.post('/add-project')
async def add_project(newProject: _Project):
    return await _add_project(newProject)


@router.get('/get-company-by-id', response_model=_Company)
async def get_company_by_id(id: int = None, projectId: int = None):
    return await _get_company_by_id(id, projectId)


@router.post('/add-property')
async def add_property(newProperty: _Property):
    return await _add_property(newProperty)


@router.get('/get-projects-by-position')
async def get_projects_by_position(lat: float, lng: float, radius: int):
    return await _get_projects_by_position(lat, lng, radius)


@router.get('/company-delete')
async def company_delete(id: int):
    return await _company_delete(id)


@router.get('/project-delete')
async def project_delete(id: int):
    return await _project_delete(id)


@router.get('/property-delete')
async def property_delete(id: int):
    return await _property_delete(id)


@router.post('/company-edit')
async def company_edit(company: _Company):
    return await _company_edit(company)

@router.post('/project-edit')
async def project_edit(project: _Project):
    return await _project_edit(project)

@router.get('/get-premium-query')
async def get_premium_query():
    return await _get_premium_query()

@router.post('/change-premium')
async def change_premium(data: List[_PremiumCompanyData]):
    return await _changePremium(data)