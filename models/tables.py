from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import JSON, Column, Date, ForeignKey, Integer, String, Boolean, Float

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    alternative_id = Column(String, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    tel = Column(String)
    hash = Column(String)
    address = Column(String)
    num = Column(String)
    district = Column(String)
    complement = Column(String)
    city = Column(String)
    uf = Column(String)
    cep = Column(String)
    provider = Column(Integer, nullable=False) # 1 - Credentials, 2 - Google, 3 - Facebook
    access_token = Column(String)
    refresh_token = Column(String)
    is_admin = Column(Boolean)
    is_authenticated = Column(Boolean)
    company_user_id = relationship('Company')

    def __init__(self, alternative_id, name, email, tel, hash, address, num, district, \
                 complement, city, uf, cep, provider, access_token, refresh_token, is_admin, is_authenticated):
        self.alternative_id = alternative_id
        self.name = name
        self.email = email
        self.tel = tel
        self.hash = hash
        self.address = address
        self.num = num
        self.district = district
        self.complement = complement
        self.city = city
        self.uf = uf
        self.cep = cep
        self.provider = provider
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.is_admin = is_admin
        self.is_authenticated = is_authenticated

class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    tel = Column(String, nullable=False)
    address = Column(String, nullable=False)
    num = Column(String, nullable=False)
    complement = Column(String)
    district = Column(String, nullable=False)
    city = Column(String, nullable=False)
    uf = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    images = Column(JSON)
    admin_id = Column(Integer, ForeignKey(User.id))
    project_company_id = relationship('Project')
    property_company_id = relationship('Property')

    def __init__(self, name, email, tel, address, num, complement, district, city, uf, cep, images, admin_id):
        self.name = name
        self.email = email
        self.tel = tel
        self.address = address
        self.num = num
        self.complement = complement
        self.district = district
        self.city = city
        self.uf = uf
        self.cep = cep
        self.images = images
        self.admin_id = admin_id

class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    name = Column(String)
    project_status_id = relationship('Project')
    property_status_id = relationship('Property')
    
    def __init__(self, name):
        self.name = name

class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    delivery_date = Column(Date)
    address = Column(String)
    num = Column(String)
    complement = Column(String)
    district = Column(String)
    city = Column(String)
    uf = Column(String)
    cep = Column(String)
    status = Column(Integer, ForeignKey(Status.id))
    images = Column(JSON)
    company_id = Column(Integer, ForeignKey(Company.id), nullable=False)
    property_project_id = relationship('Property')

    def __init__(self, name, description, delivery_date, address, num,\
                  complement, district, city, uf, cep, status, images, company_id):
        self.name = name
        self.description = description
        self.delivery_date = delivery_date
        self.address = address
        self.num = num
        self.complement = complement
        self.district = district
        self.city = city
        self.uf = uf
        self.cep = cep
        self.status = status
        self.images = images
        self.company_id = company_id

class Property(Base):
    __tablename__ = 'property'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    delivery_date = Column(Date)
    model = Column(String)
    measure = Column(String)
    size = Column(Float)
    price = Column(Float)
    status = Column(Integer, ForeignKey(Status.id))
    images = Column(JSON)
    company_id = Column(Integer, ForeignKey(Company.id), nullable=False)
    project_id = Column(Integer, ForeignKey(Project.id), nullable=False)
    
    def __init__(self, name, description, delivery_date, model, measure, size, price, status, images, company_id, project_id):
        self.name = name
        self.description = description
        self.delivery_date = delivery_date
        self.model = model
        self.measure = measure
        self.size = size
        self.price = price
        self.status = status
        self.images = images
        self.company_id = company_id
        self.project_id = project_id
