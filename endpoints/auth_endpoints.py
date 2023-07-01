from datetime import datetime, timedelta
from json import dumps
import os
from fastapi import APIRouter, Response
from models.basemodels import _Auth_Email, _Credencials, _New_User, _Password_Token_Validate, _Response, _Send_New_Password
from services.user_services import _new_alternative_id, _user_update, _get_user
import jwt
from providers.email_functions import auth_email, new_password_email
from jwt.exceptions import ExpiredSignatureError

router = APIRouter(prefix='/auth')
JWT_SECRET = os.environ.get('JWT_SECRET')

@router.post('/login')
async def get_token(data: _Credencials):
    user = await _get_user(email=data.email)
    if not user:
        return Response(dumps(None), 200)
    return user

@router.post('/send-auth-email')
async def send_auth_mail(data: _Credencials):
    payload = {
        'alternative_id': data.alternative_id, 
        'email': data.email, 
        'nome': data.name,
        'exp': datetime.utcnow() + timedelta(hours=1)
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
    try:
        decoded_jwt = jwt.decode(data['token'], JWT_SECRET, algorithms=["HS256"])
        session = data['session']
        if session['alternative_id'] == decoded_jwt['alternative_id'] and \
            session['name'] == decoded_jwt['nome'] and \
            session['email'] == decoded_jwt['email']:
            return dumps(True)
        
        return dumps(False)
    except ExpiredSignatureError as error:
        print(str(error))
        return dumps(False)

@router.post('/send-new-password')
async def send_new_password(data: _Send_New_Password):
    try:
        user = await _get_user(email=data.email)
        if not user:
            return Response('email invalido', 404)
        else:
            if user.provider == 2:
                return Response('google provider', 460)
            elif user.provider == 3:
                return Response('facebook provider', 461)
            else:
                payload = {
                    'alternative_id': user.alternative_id, 
                    'email': user.email, 
                    'nome': user.name,
                    'action': 'newPassword',
                    'exp': datetime.utcnow() + timedelta(hours=1)
                }
                encoded_jwt = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

                link = f'{os.environ["APP_URL"]}/auth/new-password-auth?token={encoded_jwt}'
                nome = user.name
                if new_password_email(user.email, nome, link):
                    return Response('Email enviado')
                else:
                    return Response('Erro no servidor', 500)
    except Exception as error:
        print(str(error))
        pass

@router.post('/new-password-validate', response_model=_Response)
async def new_password_validade(data: _Password_Token_Validate):
    try:
        if data.type == 'validate':
            decoded_jwt = jwt.decode(data.token, JWT_SECRET, algorithms=["HS256"])
            print(decoded_jwt)
            user = await _get_user(email=decoded_jwt['email'])
            if not user:
                return _Response(
                    status=461,
                    body='email invalido'
                )
            
            if user.alternative_id != decoded_jwt['alternative_id']\
            or user.name != decoded_jwt['nome']\
            or decoded_jwt['action'] != 'newPassword':
                return _Response(
                    status=462,
                    body='credenciais invalidas'
                )
            
            email_dict = {'email': decoded_jwt['email']}
            return _Response(
                    status=200,
                    body=email_dict
                )
        elif data.type == 'recordHash':
            data_to_change = _New_User(
                hash=data.hash
            )
            new_alternative_id = await _new_alternative_id()
            data_to_change.alternative_id = new_alternative_id
            update = await _user_update(email=data.email, data=data_to_change)
            if update == True:
                return _Response(
                    status=200,
                    body='senha alterada com sucesso'
                )
            else:
                return _Response(
                    status=500,
                    body='erro no servidor'
                )
                
    except ExpiredSignatureError as error:
        print(str(error))
        return _Response(
            status=460,
            body='token expirado'
        )