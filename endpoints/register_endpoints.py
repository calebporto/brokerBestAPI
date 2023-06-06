from typing import Dict
from fastapi import APIRouter, Response
from models.basemodels import _Credencials, _New_User
from services.user_services import new_user

router = APIRouter(prefix='/user-register')

@router.post('/new')
async def get_token(user: _New_User):
    add_user = await new_user(user)
    if add_user:
        # return magic link
        return Response('Tudo ok', 200)
    else:
        return Response('Erro no servidor', 500)