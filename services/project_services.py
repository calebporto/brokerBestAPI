import asyncio
from json import dumps

from sqlalchemy import func
from fastapi import Response
from models.basemodels import _BasicProject, _Project, _ProjectView, _Property
from models.tables import Company, Premium, Project, Property
from models.connection import async_session
from sqlalchemy.future import select

loop = asyncio.get_event_loop()


async def _get_project_names(filter: str):
    async with async_session() as session:
        if filter == 'bairro':
            query = await session.execute(select(Project.district).distinct())
            result = query.scalars().all()
        elif filter == 'regiao':
            query = await session.execute(select(Project.zone).distinct())
            result = query.scalars().all()
        elif filter == 'construtora':
            query = await session.execute(
                select(Project.id)
                .column(Company.name)
                .join(Company, Project.company_id == Company.id)
                .distinct(Company.name)
            )
            raw_result = query.all()
            result = [item[1] for item in raw_result]
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
        
        query = query.limit(12)

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
                select(Project).select_from(Premium)\
                .join(Project, Premium.project_id == Project.id)
            )
            result = query.scalars().all()
            
            response = []
            for project in result:
                response.append(_Project(
                    id = project.id,
                    company_id = project.company_id,
                    name = project.name,
                    description = project.description,
                    delivery_date = project.delivery_date,
                    address = project.address,
                    num = project.num,
                    complement = project.complement,
                    district = project.district,
                    zone = project.zone,
                    city = project.city,
                    uf = project.uf,
                    cep = project.cep,
                    latitude = project.latitude,
                    longitude = project.longitude,
                    status = project.status,
                    thumb = project.thumb,
                    images = project.images,
                    videos = project.videos,
                    link = project.link,
                    book = project.book
                ).dict())

            return Response(dumps(response, default=str), 200)
        except Exception as error:
            print(str(error))
            return Response('Erro no servidor', 500)
        

async def _get_project_by_id(id: int):
    async with async_session() as session:
        try:
            query = select(Project)\
                .add_columns(Company.name, Property)\
                .join(Company, Project.company_id == Company.id)\
                .outerjoin(Property, Project.id == Property.project_id)\
                .where(Project.id == 1)
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
                response.cp_name = project_result[0][1]
                response.properties = []
            for item in project_result:
                property = item[2]
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