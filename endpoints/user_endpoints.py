from json import dumps
from typing import Optional
from fastapi import APIRouter, Response
from models.basemodels import _New_User
from services.user_services import _get_user


router = APIRouter(prefix='/user-services')

@router.get('/get-context-user')
async def get_context_user(alternative_id: str | None = None, email: str | None = None):
    user = await _get_user(alternative_id=alternative_id) if alternative_id else await _get_user(email=email)
    if user:
        user_data = {
            'id': user.id,
            'alternative_id': user.alternative_id,
            'name': user.name,
            'email': user.email,
            'tel': user.tel,
            'cep': user.cep,
            'address': user.address,
            'num': user.num,
            'district': user.district,
            'complement': user.complement,
            'city': user.city,
            'uf': user.uf,
            'provider': user.provider,
            'is_admin': user.is_admin,
            'is_complete_data': user.is_complete_data
        }
        return Response(dumps(user_data), 200)
    else:
        return Response('unauthorizated',401)