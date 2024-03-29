from dpf.modules import covid, elections
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

templates_elections = Jinja2Templates(directory='dpf/modules/elections/website/')
templates_covid = Jinja2Templates(directory='dpf/modules/covid/website/')
templates_main = Jinja2Templates(directory='website/')


async def elections_page(request):
    return templates_elections.TemplateResponse('index.html', {
        'request': request,
    })


async def covid_page(request):
    return templates_covid.TemplateResponse('index.html', {
        'request': request,
        'title': 'Covid charts',
    })

async def main_page(request):
    return templates_main.TemplateResponse('index.html', {
        'request': request,
    })

app = FastAPI()
app.mount('/static', StaticFiles(directory='dpf/modules/elections/website/static'), name='static')
app.add_route('/', main_page)
app.add_route('/index.html', main_page)


app.mount('/elections/static', StaticFiles(directory='dpf/modules/elections/website/static'), name='static')
app.add_route('/elections', elections_page)
app.add_route('/elections/index.html', elections_page)
app.include_router(elections.router)


app.mount('/covid/static', StaticFiles(directory='dpf/modules/covid/website/static'), name='static')
app.add_route('/covid', covid_page)
app.add_route('/covid/index.html', covid_page)
app.include_router(covid.router)


