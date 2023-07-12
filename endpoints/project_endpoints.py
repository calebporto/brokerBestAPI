from fastapi import APIRouter

from services.project_services import _get_premium_projects, _get_project_by_id, _get_project_names, _get_projects


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