from dpf.modules import covid, elections
from fastapi import FastAPI, APIRouter
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory='website/')


async def homepage(request):
    return templates.TemplateResponse('index.html', {
        'request': request,
    })


app = FastAPI(routes=[
    Route('/index.html', homepage),
    Route('/', homepage),
    Mount('/static', StaticFiles(directory='website/static'), name='static')
])


app.include_router(elections.router)
app.include_router(covid.router)
