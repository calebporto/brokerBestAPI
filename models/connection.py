from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

engine = create_async_engine(os.environ['DATABASE_URL'])
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)