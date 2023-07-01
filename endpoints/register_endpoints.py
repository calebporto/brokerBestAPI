from typing import Dict
from fastapi import APIRouter, Response
from models.basemodels import _Credencials, _New_User
from services.user_services import _complete_user, _new_user

router = APIRouter(prefix='/user-register')

@router.post('/new')
async def new_user(user: _New_User):
    #try:
    return await _new_user(user)
    #except:
     #   return Response('Erro no servidor', 500)

@router.post('/complete')
async def complete_user(user:_New_User):
    '''
    Recebe os dados dos usuários de autenticação social
    '''
    return await _complete_user(user)