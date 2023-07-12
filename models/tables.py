from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import JSON, Column, Date, ForeignKey, Integer, String, Boolean, Float, Text

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    alternative_id = Column(String, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
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
    is_complete_data = Column(Boolean)
    is_admin = Column(Boolean)
    company_user_id = relationship('Company')

    def __init__(self, alternative_id, name, email, tel, hash, address, num, district, \
                 complement, city, uf, cep, provider, is_admin, is_complete_data):
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
        self.is_admin = is_admin
        self.is_complete_data = is_complete_data

class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    email = Column(String, nullable=False)
    tel = Column(String, nullable=False)
    address = Column(String, nullable=False)
    num = Column(String, nullable=False)
    complement = Column(String)
    district = Column(String, nullable=False)
    city = Column(String, nullable=False)
    uf = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    thumb = Column(String)
    images = Column(JSON)
    admin_id = Column(Integer, ForeignKey(User.id), nullable=False)
    is_active = Column(Boolean, nullable=False)
    project_company_id = relationship('Project')
    property_company_id = relationship('Property')

    def __init__(self, name, description, email, tel, address, num, complement, district, city, uf, cep, thumb, images, admin_id, is_active):
        self.name = name
        self.email = email
        self.description = description
        self.tel = tel
        self.address = address
        self.num = num
        self.complement = complement
        self.district = district
        self.city = city
        self.uf = uf
        self.cep = cep
        self.thumb = thumb
        self.images = images
        self.admin_id = admin_id
        self.is_active = is_active

class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    company_id = Column(Integer, ForeignKey(Company.id), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    delivery_date = Column(Date)
    address = Column(String)
    num = Column(String)
    complement = Column(String)
    district = Column(String)
    zone = Column(String)
    city = Column(String)
    uf = Column(String)
    cep = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    status = Column(String)
    thumb = Column(String)
    images = Column(JSON)
    videos = Column(JSON)
    link = Column(String) # Link do drive original da corretora
    book = Column(String) # Link do book em PDF
    property_project_id = relationship('Property')
    premium_project_id = relationship('Premium')

    def __init__(self, company_id, name, description, delivery_date, address, num,\
                  complement, district, zone, city, uf, cep, latitude, longitude, status, thumb, images, videos, link, book):
        self.company_id = company_id
        self.name = name
        self.description = description
        self.delivery_date = delivery_date
        self.address = address
        self.num = num
        self.complement = complement
        self.district = district
        self.zone = zone
        self.city = city
        self.uf = uf
        self.cep = cep
        self.latitude = latitude
        self.longitude = longitude
        self.status = status
        self.thumb = thumb
        self.images = images
        self.videos = videos
        self.link = link
        self.book = book

class Premium(Base):
    __tablename__ = 'premium'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    project_id = Column(Integer, ForeignKey(Project.id), nullable=False)

class Property(Base):
    __tablename__ = 'property'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    company_id = Column(Integer, ForeignKey(Company.id), nullable=False)
    project_id = Column(Integer, ForeignKey(Project.id), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    delivery_date = Column(Date)
    model = Column(String)
    measure = Column(String)
    size = Column(Float)
    price = Column(Float)
    status = Column(String)
    thumb = Column(String)
    images = Column(JSON)
    videos = Column(JSON)
    
    def __init__(self, company_id, project_id, name, description, delivery_date, model, measure, size, price, status, thumb, images, videos):
        self.company_id = company_id
        self.project_id = project_id
        self.name = name
        self.description = description
        self.delivery_date = delivery_date
        self.model = model
        self.measure = measure
        self.size = size
        self.price = price
        self.status = status
        self.thumb = thumb
        self.images = images
        self.videos = videos
