from secrets import token_hex

from fastapi import Response
from models.basemodels import _New_User
from models.connection import async_session
from models.tables import User
from sqlalchemy.future import select

async def _new_alternative_id():
    async with async_session() as session:
        alternative_id = token_hex(16)
        result = await session.execute(select(User.alternative_id).where(User.alternative_id == alternative_id))
        person_id = result.scalars().first()
        if (person_id):
            _new_alternative_id()
        return alternative_id

async def _new_user(user_data):
    async with async_session() as session:
        try:
            alternative_id = await _new_alternative_id()

            user = await _get_user(email=user_data.email.lower())
            if user:
                if user.provider == 2:
                    return Response('google provider.', 461)
                elif user.provider == 3:
                    return Response('facebook provider.', 462)
                else:
                    return Response('email ja cadastrado.', 460)



            session.add(User(
                alternative_id,
                user_data.nome.lower(),
                user_data.email.lower(),
                user_data.tel.lower(),
                user_data.password,
                user_data.endereco.lower(),
                user_data.num.lower(),
                user_data.bairro.lower(),
                user_data.complemento.lower(),
                user_data.cidade.lower(),
                user_data.uf.lower(),
                user_data.cep.lower(),
                user_data.provider,
                False,
                True
            ))
            await session.commit()
            return Response('cadastro efetuado com sucesso', 200)
        except Exception as error:
            print(str(error))
            return Response ('erro no servidor', 500)

async def _complete_user(user_data):
    async with async_session() as session:
        user = await _get_user(email=user_data.email.lower())
        if user:
            return Response('Usuário já cadastrado.', 401)
        
        session.add(User(
            None,
            user_data.nome.lower(),
            user_data.email.lower(),
            user_data.tel.lower(),
            None,
            user_data.endereco.lower(),
            user_data.num.lower(),
            user_data.bairro.lower(),
            user_data.complemento.lower() if user_data.complemento.lower() else '',
            user_data.cidade.lower(),
            user_data.uf.lower(),
            user_data.cep.lower(),
            user_data.provider,
            False,
            True
        ))
        await session.commit()
        return Response('cadastro efetuado com sucesso', 200)


async def _get_user(id = None, email = None, alternative_id = None):
    async with async_session() as session:
        result = None
        if id:
            result = await session.execute(select(User).where(User.id == id))
            return result.scalars().first()
        elif email:
            result = await session.execute(select(User).where(User.email == email))
            return result.scalars().first()
        elif alternative_id:
            result = await session.execute(select(User).where(User.alternative_id == alternative_id))
            return result.scalars().first()
        else:
            return None
        
async def _user_update(data: _New_User, email=None, id=None, alternative_id=None):
    async with async_session() as session:
        try:
            user = None
            if id:
                result = await session.execute(select(User).where(User.id == id))
                user = result.scalars().first()
            elif email:
                result = await session.execute(select(User).where(User.email == email))
                user = result.scalars().first()
            elif alternative_id:
                result = await session.execute(select(User).where(User.alternative_id == alternative_id))
                user = result.scalars().first()

            if not user:
                return False
            
            user.alternative_id = data.alternative_id if data.alternative_id else user.alternative_id
            user.name = data.nome if data.nome else user.name
            user.email = data.email if data.email else user.email
            user.tel = data.tel if data.tel else user.tel
            user.hash = data.hash if data.hash else user.hash
            user.address = data.endereco if data.endereco else user.address
            user.num = data.num if data.num else user.num
            user.district = data.bairro if data.bairro else user.district
            user.complement = data.complemento if data.complemento else user.complement
            user.city = data.cidade if data.cidade else user.city
            user.uf = data.uf if data.uf else user.uf
            user.cep = data.cep if data.cep else user.cep
            user.provider = data.provider if data.provider else user.provider
            user.is_admin = data.is_admin if data.is_admin != None else user.is_admin
            user.is_data_complete = data.is_data_complete if data.is_data_complete != None else user.is_data_complete
            
            session.add(user)
            await session.commit()

            return True
        except Exception as error:
            print(str(error))
            return False