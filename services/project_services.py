import asyncio
from datetime import date, datetime
from json import dumps
from typing import List, Optional

from sqlalchemy import delete, func
from fastapi import Response
from models.basemodels import _BasicProject, _Company, _PremiumCompanyData, _PremiumQuery, _Project, _ProjectView, _Property
from models.tables import Company, Premium, Project, Property, User
from models.connection import async_session
from sqlalchemy.future import select

loop = asyncio.get_event_loop()


async def _get_project_names(filter: str):
    async with async_session() as session:
        if filter == 'bairro':
            query = await session.execute(select(Project.district).where(Project.district != None).distinct())
            result = query.scalars().all()
        elif filter == 'regiao':
            query = await session.execute(select(Project.zone).where(Project.zone != None).distinct())
            result = query.scalars().all()
        elif filter == 'construtora':
            query = await session.execute(
                select(Company.name).select_from(Project)\
                .join(Company, Project.company_id == Company.id)\
                .where(Company.name != None)\
                .distinct(Company.name)
            )
            raw_result = query.scalars().all()
            print(raw_result)
            result = raw_result
        else:
            return Response('filtro invalido', 400)
        return Response(dumps(result), 200)
    
async def _get_projects(
        filterBy: str,
        key: str,
        orderBy: str,
        offset: str | int,
        guidance: str
    ):
    async with async_session() as session:
        query = select(Project)\
                .add_columns(Company.admin_id)\
                .join(Company, Project.company_id == Company.id)
        
        count_query = select(func.count()).select_from(Project)\
                .join(Company, Project.company_id == Company.id)
        
        match filterBy:
            case 'bairro':
                query = query.where(Project.district == key)
                count_query = count_query.where(Project.district == key)
            case 'regiao':
                query = query.where(Project.zone == key)
                count_query = count_query.where(Project.zone == key)
            case 'construtora':
                query = query.where(Company.name == key)
                count_query = count_query.where(Company.name == key)
            case 'companyId':
                query = query.where(Company.id == int(key))
                count_query = count_query.where(Company.id == int(key))
            case _:
                return Response('filterBy invalido')
        

        match orderBy:
            case 'id':
                if guidance == 'desc':
                    query = query.order_by(Project.id.desc())
                else:
                    query = query.order_by(Project.id)
            case 'name':
                if guidance == 'desc':
                    query = query.order_by(Project.name.desc())
                else:
                    query = query.order_by(Project.name)
            case 'deliveryDate':
                if guidance == 'desc':
                    query = query.order_by(Project.delivery_date.desc())
                else:
                    query = query.order_by(Project.delivery_date)
            case _:
                return Response('orderBy invalido')
        

        if int(offset) > 0:
            query = query.offset(int(offset))
        
        query = query.limit(50)

        result = await session.execute(query)
        count = await session.execute(count_query)
        
        projectsData = result.all()
        countResult = count.scalar_one()
        

        response_data = []
        for projectData in projectsData:
            
            projectResponse = _BasicProject(
                id = int(projectData[0].id),
                name = projectData[0].name,
                thumb = projectData[0].thumb,
                delivery_date = projectData[0].delivery_date,
                admin_id= int(projectData[1])
            )
            response_data.append(projectResponse.dict())
        
        response = {
            'data': response_data,
            'count': countResult
        }

        return Response(dumps(response, default=str), 200)

async def _get_premium_projects():
    async with async_session() as session:
        try:
            query = await session.execute(
                select(Company).select_from(Premium)\
                .join(Company, Premium.company_id == Company.id)
            )
            result = query.scalars().all()
            
            response = []
            for company in result:
                response.append(_Company(**company.__dict__).dict())

            return Response(dumps(response, default=str), 200)
        except Exception as error:
            print(str(error))
            return Response('Erro no servidor', 500)

async def _get_project_by_id(id: int):
    async with async_session() as session:
        try:
            query = select(Project)\
                .add_columns(Company, Property)\
                .join(Company, Project.company_id == Company.id)\
                .outerjoin(Property, Project.id == Property.project_id)\
                .where(Project.id == id)
            result = await session.execute(query)
            project_result = result.all()
            
            response = _ProjectView()
            if len(project_result) > 0:
                response.project = _Project(
                    id = project_result[0][0].id,
                    company_id = project_result[0][0].company_id,
                    name = project_result[0][0].name,
                    description = project_result[0][0].description,
                    delivery_date = project_result[0][0].delivery_date,
                    address = project_result[0][0].address,
                    num = project_result[0][0].num,
                    complement = project_result[0][0].complement,
                    district = project_result[0][0].district,
                    zone = project_result[0][0].zone,
                    city = project_result[0][0].city,
                    uf = project_result[0][0].uf,
                    cep = project_result[0][0].cep,
                    latitude = project_result[0][0].latitude,
                    longitude = project_result[0][0].longitude,
                    status = project_result[0][0].status,
                    thumb = project_result[0][0].thumb,
                    images = project_result[0][0].images,
                    videos = project_result[0][0].videos,
                    link = project_result[0][0].link,
                    book = project_result[0][0].book
                )
                response.company = _Company(**project_result[0][1].__dict__)
                response.properties = []
            for item in project_result:
                property = item[2]
                if (property):
                    response.properties.append(_Property(
                        id=property.id,
                        company_id=property.company_id,
                        project_id=property.project_id,
                        name=property.name,
                        description=property.description,
                        delivery_date=property.delivery_date,
                        model=property.model,
                        measure=property.measure,
                        size=property.size,
                        price=property.price,
                        status=property.status,
                        thumb=property.thumb,
                        images=property.images,
                        videos=property.videos
                    ))

            return Response(dumps(response.dict(), default=str), 200)
        except Exception as error:
            print(str(error))
            return Response('Erro no servidor.', 200)

async def _get_companies(userEmail: str):
    async with async_session() as session:
        is_admin_query = await session.execute(select(User.is_admin).where(User.email == userEmail))
        is_admin = is_admin_query.scalars().first()
        
        query = None
        if is_admin:
            query = await session.execute(select(Company).order_by(Company.id))
        else:
            query = await session.execute(select(Company)\
                    .join(User, Company.admin_id == User.id)\
                    .where(User.email == userEmail))
        
        result = query.scalars().all()
        
        for i, item in enumerate(result):
            result[i] = _Company(**item.__dict__).dict()
        
        return Response(dumps(result), 200)
    
async def _add_company(newCompany: _Company):
    async with async_session() as session:
        try:
            session.add(Company(
                newCompany.name,
                newCompany.description,
                newCompany.email,
                newCompany.tel,
                newCompany.address,
                newCompany.num,
                newCompany.complement,
                newCompany.district,
                newCompany.city,
                newCompany.uf,
                newCompany.cep,
                newCompany.thumbG,
                newCompany.thumbM,
                newCompany.thumbP,
                newCompany.images,
                newCompany.admin_id,
                newCompany.is_active
            ))
            await session.commit()
            return Response('Construtora cadastrada com sucesso', 200)
        except Exception as error:
            print(str(error))
            return Response('Erro no servidor', 500)
        
async def _add_project(newProject: _Project):
    async with async_session() as session:
        try:
            pjDate = newProject.delivery_date.date() if newProject.delivery_date else None
            session.add(Project(
                newProject.company_id,
                newProject.name,
                newProject.description,
                pjDate,
                newProject.address,
                newProject.num,
                newProject.complement,
                newProject.district,
                newProject.zone,
                newProject.city,
                newProject.uf,
                newProject.cep,
                newProject.latitude,
                newProject.longitude,
                newProject.status,
                newProject.thumb,
                newProject.images,
                newProject.videos,
                newProject.link,
                newProject.book
            ))
            await session.commit()
            return Response('Empreendimento cadastrado com sucesso', 200)
        except Exception as error:
            print(str(error))
            return Response('Erro no servidor', 500)
        
async def _get_company_by_id(id: int | None, projectId: int | None):
    async with async_session() as session:
        query = None
        if id:
            query = await session.execute(
                select(Company).where(Company.id == id)
            )
        elif projectId:
            query = await session.execute(
                select(Company)\
                .join(Project, Company.id == Project.company_id)\
                .where(Project.id == projectId)
            )
        else:
            return Response('Você deve fornecer id ou projectId', 422)
        result = query.scalars().first()
        company = _Company(**result.__dict__)
        return Response(company.json(), 200)
    
async def _add_property(newProperty: _Property):
    async with async_session() as session:
        try:
            ppDate = newProperty.delivery_date.date() if newProperty.delivery_date else None
            session.add(Property(
                newProperty.company_id,
                newProperty.project_id,
                newProperty.name,
                newProperty.description,
                ppDate,
                newProperty.model,
                newProperty.measure,
                float(newProperty.size),
                float(newProperty.price),
                newProperty.status,
                newProperty.thumb,
                newProperty.images,
                newProperty.videos
            ))
            await session.commit()
            return Response('Imóvel cadastrado com sucesso', 200)
        except Exception as error:
            print(str(error))
            return Response('Erro no servidor', 500)
        
async def _get_projects_by_position(lat: int, lng: int, radius: int):
    async with async_session() as session:
        query = await session.execute(
            select(Project)\
            .where(6371 *\
                   func.acos(
                    func.cos(func.radians(lat)) *\
                    func.cos(func.radians(Project.latitude)) *\
                    func.cos(func.radians(lng) - func.radians(Project.longitude)) +\
                    func.sin(func.radians(lat)) *\
                    func.sin(func.radians(Project.latitude))
                   ) <= radius)
        )
        result = query.scalars().all()
        print(result)
        
        projects = []
        for project in result:
            projects.append(_Project(**project.__dict__).dict())
        
        return Response(dumps(projects, default=str), 200)
    
async def _company_delete(id: int):
    async with async_session() as session:
        await session.execute(delete(Company).where(Company.id == id))
        await session.commit()
        return Response('Construtora excluída com sucesso.', 200)

async def _project_delete(id: int):
    async with async_session() as session:
        await session.execute(delete(Project).where(Project.id == id))
        await session.commit()
        return Response('Empreendimento excluído com sucesso.', 200)

async def _property_delete(id: int):
    async with async_session() as session:
        await session.execute(delete(Property).where(Property.id == id))
        await session.commit()
        return Response('Imóvel excluído com sucesso.', 200)
    
async def _company_edit(company: _Company):
    async with async_session() as session:
        if not company.id:
            return Response('Id inválido', 400)
        
        query = await session.execute(
            select(Company).where(Company.id == company.id)
        )
        company_db = query.scalars().first()

        company_db.name = company.name if company.name else company_db.name
        company_db.description = company.description if company.description else company_db.description
        company_db.email = company.email if company.email else company_db.email
        company_db.tel = company.tel if company.tel else company_db.tel
        company_db.address = company.address if company.address else company_db.address
        company_db.num = company.num if company.num else company_db.num
        company_db.complement = company.complement if company.complement else company_db.complement
        company_db.district = company.district if company.district else company_db.district
        company_db.city = company.city if company.city else company_db.city
        company_db.uf = company.uf if company.uf else company_db.uf
        company_db.cep = company.cep if company.cep else company_db.cep
        company_db.thumbG = company.thumbG if company.thumbG else company_db.thumbG
        company_db.thumbM = company.thumbM if company.thumbM else company_db.thumbM
        company_db.thumbP = company.thumbP if company.thumbP else company_db.thumbP

        session.add(company_db)
        await session.commit()

async def _project_edit(project: _Project):
    async with async_session() as session:
        if not project.id:
            return Response('Id inválido', 400)
        
        query = await session.execute(
            select(Project).where(Project.id == project.id)
        )
        project_db = query.scalars().first()

        project_db.name = project.name if project.name else project_db.name
        project_db.description = project.description if project.description else project_db.description
        project_db.delivery_date = project.delivery_date if project.delivery_date else project_db.delivery_date
        project_db.address = project.address if project.address else project_db.address
        project_db.num = project.num if project.num else project_db.num
        project_db.complement = project.complement if project.complement else project_db.complement
        project_db.district = project.district if project.district else project_db.district
        project_db.zone = project.zone if project.zone else project_db.zone
        project_db.city = project.city if project.city else project_db.city
        project_db.uf = project.uf if project.uf else project_db.uf
        project_db.latitude = project.latitude if project.latitude else project_db.latitude
        project_db.longitude = project.longitude if project.longitude else project_db.longitude
        project_db.status = project.status if project.status else project_db.status
        project_db.thumb = project.thumb if project.thumb else project_db.thumb
        project_db.images = project.images if project.images else project_db.images
        project_db.videos = project.videos if project.videos else project_db.videos
        project_db.link = project.link if project.link else project_db.link
        project_db.book = project.book if project.book else project_db.book

        session.add(project_db)
        await session.commit()

        return Response('Cadastro alterado com sucesso.', 200)
    
async def _get_premium_query():
    async with async_session() as session:
        companyQuery = await session.execute(
            select(Company)
        )
        companyResult = companyQuery.scalars().all()

        premiumQuery = await session.execute(
            select(Company.id)\
            .add_columns(Company.name)\
            .join(Premium, Company.id == Premium.company_id)\
            .where(Premium.company_id == Company.id)
        )
        premiumResult = premiumQuery.all()

        response = _PremiumQuery(
            premiumList=[],
            companyList=[]
        )

        for company in companyResult:
            response.companyList.append(_PremiumCompanyData(**company.__dict__))
        
        for company in premiumResult:
            response.premiumList.append(_PremiumCompanyData(
                id=company[0],
                name=company[1]
            ))
        
        return Response(response.json(), 200)
        

async def _changePremium(data: List[_PremiumCompanyData]):
    async with async_session() as session:
        await session.execute(delete(Premium))
        for item in data:
            session.add(Premium(
                company_id=item.id
            ))
        await session.commit()

        return Response('Alteração realizada com sucesso.', 200)