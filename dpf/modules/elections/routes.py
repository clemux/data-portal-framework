from typing import Union, Optional

from dpf.lib.db import Session, get_db
from fastapi import APIRouter, Query, Depends, HTTPException
from . import models, schemas


def get_circ_results(db: Session, code_dept: str, code_circ: str) -> Optional[dict[str, Union[str, float]]]:
    print(code_dept, code_circ)
    circ_candidate_results = db.query(models.CircResultOrm).filter_by(
        code_circ=code_circ,
        code_dept=code_dept,
    ).all()

    if len(circ_candidate_results) == 0:
        raise HTTPException(status_code=400, detail="Département ou circonscription non trouvée")
    candidates = {}
    for result in circ_candidate_results:
        candidates[result.candidate] = result.percentage

    circ_result_dict = {
        'code_circ': circ_candidate_results[0].code_circ,
        'code_dept': circ_candidate_results[0].code_dept,
        'candidates': candidates,
    }

    return circ_result_dict


router = APIRouter(prefix='/elections', tags=['elections'])


@router.get('/results', response_model=schemas.CircResult)
async def get_results(
        code_dept: str = Query(..., description="Numéro de département", example="67", min_length=2),
        code_circ: str = Query(..., description="Numéro de circonscription", example="02", min_length=2),
        db: Session = Depends(get_db)):
    votes = get_circ_results(db, code_dept, code_circ)

    return votes
