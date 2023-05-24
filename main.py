from fastapi import FastAPI, Request
from endpoints import auth_endpoints

app = FastAPI(
    title='API - Broker Best',
    description='API destinada a transações com o banco de dados da aplicação.',
    version=1.0
)

@app.middleware('http')
async def auth(request: Request, call_next):
    '''
    Middleware para filtro de requisições.
    Verifica se a requisição contém os padrões exigidos.
    '''
    print('Antes')

    response = await call_next(request)

    print('Depois')
    return response

app.include_router(auth_endpoints.router)