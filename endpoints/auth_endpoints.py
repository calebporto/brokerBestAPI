from fastapi import APIRouter
from models.basemodels import _Credencials

router = APIRouter(prefix='/auth')

@router.post('/get-token')
async def get_token(data: _Credencials):
    return 'ok'