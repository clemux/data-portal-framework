from pydantic import BaseModel


class CircResult(BaseModel):
    code_dept: str
    code_circ: str
    candidates: dict[str, float]
