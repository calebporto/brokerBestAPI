from datetime import datetime, timedelta
from json import dumps
import os
from fastapi import APIRouter, Response
from models.basemodels import _Credencials
from services.user_services import get_user
import jwt
from providers.email_functions import auth_email

router = APIRouter(prefix='/auth')
JWT_SECRET = os.environ.get('JWT_SECRET')

@router.post('/login')
async def get_token(data: _Credencials):
    user = await get_user(email=data.email)
    if not user:
        return Response(dumps(None), 200)
    print(user.hash)
    return user

@router.post('/send_auth_mail')
async def send_auth_mail(data: _Credencials):
    payload = {
        'alternative_id': data.alternative_id, 
        'email': data.email, 
        'nome': data.name,
        'exp': datetime.now() + timedelta(hours=1)
    }
    encoded_jwt = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    
    nome = data.name
    link = f'{os.environ["APP_URL"]}/auth/email-validate?token={encoded_jwt}'
    if auth_email(data.email, nome, link):
        return dumps(True)
    else:
        return dumps(False)
    
@router.post('/email-validate')
async def email_validate(data: dict):
    print(data['token'])
    decoded_jwt = jwt.decode(data['token'], JWT_SECRET, algorithms=["HS256"])
    print(decoded_jwt)
    return dumps(True)
