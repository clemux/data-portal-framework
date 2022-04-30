from fastapi import FastAPI, Depends
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from dpf.db import schemas, crud
from dpf.db.database import SessionLocal, Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


@app.get('/results', response_model=schemas.CircResult)
async def get_results(code_dept: str, code_circ: str, db: Session = Depends(get_db)):
    votes = crud.get_circ_results(db, code_dept, code_circ)

    return votes
