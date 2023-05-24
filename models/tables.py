from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, Boolean, Float

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    tel = Column(String, nullable=False)


class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    tel = Column(String, nullable=False)
    address = Column(String, nullable=False)
    number = Column(String, nullable=False)
    district = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)

    def __init__(self, id, name, email, tel, address, number, district, cep, city, state):
        self.id = id
        self.name = name
        self.email = email
        self.tel = tel
        self.address = address
        self.number = number
        self.district = district
        self.cep = cep
        self.city = city
        self.state = state


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String)
    number = Column(String)
    reference = Column(String)
    city = Column(String)
    cep = Column(String)
    state = Column(String)
    company_id = Column(Integer, ForeignKey(Company.id), nullable=False)

class Property(Base):
    __tablename__ = 'property'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    measure = Column(String)
    size = Column(Float)
    price = Column(Float)
    image_id = Column(String)
    company_id = Column(Integer, ForeignKey(Company.id), nullable=False)
    project_id = Column(Integer, ForeignKey(Project.id), nullable=False)
    
    def __init__(self, id, name, description, measure, size, price, image_id):
        self.id = id
        self.name = name
        self.name = name
        self.description = description
        self.measure = measure
        self.size = size
        self.price = price
        self.image_id = image_id