from typing import Union

from sqlalchemy.orm import Session

from . import models


def get_circ_results(db: Session, code_dept: str, code_circ: str) -> dict[str, Union[str, float]]:
    print(code_dept, code_circ)
    circ_candidate_results = db.query(models.CircResultOrm).filter_by(
        code_circ=code_circ,
        code_dept=code_dept,
    ).all()

    candidates = {}
    for result in circ_candidate_results:
        candidates[result.candidate] = result.percentage

    circ_result_dict = {
        'code_circ': circ_candidate_results[0].code_circ,
        'code_dept': circ_candidate_results[0].code_dept,
        'candidates': candidates,
    }

    return circ_result_dict
