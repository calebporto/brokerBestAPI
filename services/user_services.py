from secrets import token_hex
from models.connection import async_session
from models.tables import User
from sqlalchemy.future import select

async def new_alternative_id():
    async with async_session() as session:
        alternative_id = token_hex(16)
        result = await session.execute(select(User.alternative_id).where(User.alternative_id == alternative_id))
        person_id = result.scalars().first()
        if (person_id):
            new_alternative_id()
        return alternative_id

async def new_user(user_data):
    async with async_session() as session:
        alternative_id = await new_alternative_id()

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
            user_data.access_token,
            user_data.refresh_token,
            False,
            False
        ))
        await session.commit()
        return True
    
async def get_user(id = None, email = None):
    async with async_session() as session:
        result = None
        if id:
            result = await session.execute(select(User).where(User.id == id))
            return result.scalars().first()
        elif email:
            result = await session.execute(select(User).where(User.email == email))
            return result.scalars().first()
        else:
            return None