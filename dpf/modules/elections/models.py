from sqlalchemy import Column, Float, String

from dpf.lib.db import Base


class CircResultOrm(Base):
    __tablename__ = 'circ_results'
    code_dept = Column('code_dept', String, primary_key=True)
    code_circ = Column('code_circ', String, primary_key=True)
    candidate = Column('candidate', String, primary_key=True)
    percentage = Column('percentage', Float)

    def __repr__(self):
        return f"{self.code_dept}{self.code_circ} {self.candidate} {self.percentage}"
