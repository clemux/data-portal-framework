from datetime import date

from dpf.lib.db import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import models, schemas

router = APIRouter(prefix='/covid', tags=['covid'])


@router.get('/cases', response_model=list[schemas.Cases])
async def get_data(start: date, db: Session = Depends(get_db)):
    return db.query(models.Cases).filter(models.Cases.date > start).all()
