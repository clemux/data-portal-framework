from dpf.lib.db import Session
from dpf.lib.db import get_db
from dpf.db import schemas, crud
from dpf.modules import covid
from fastapi import FastAPI, Depends, Query, APIRouter
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

router = APIRouter(prefix='/elections', tags=['elections'])


@router.get('/results', response_model=schemas.CircResult)
async def get_results(
        code_dept: str = Query(..., description="Numéro de département", example="67", min_length=2),
        code_circ: str = Query(..., description="Numéro de circonscription", example="02", min_length=2),
        db: Session = Depends(get_db)):
    votes = crud.get_circ_results(db, code_dept, code_circ)

    return votes


app.include_router(router)
app.include_router(covid.router)
