from fastapi import APIRouter
from models.basemodels import _Company, _Project

from services.project_services import _add_company, _add_project, _get_companies, _get_company_by_id, _get_premium_projects, _get_project_by_id, _get_project_names, _get_projects


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
    print(id)
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

@router.get('/get-company-by-id')
async def get_company_by_id(id: str | int):
    return await _get_company_by_id(int(id))