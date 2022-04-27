from sqlalchemy import sql, Column, Sequence
from utils.db_api.database import db


class Items(db.Model):
    __tablename__ = 'items1'
    query: sql.Select

    id = Column(db.Integer, Sequence("user_id_seq"), primary_key=True)
    faculties_code = Column(db.String(20))
    faculties_name = Column(db.String(255))

    form_code = Column(db.String(20))
    form_name = Column(db.String(255))

    specialization_code = Column(db.String(20))
    specialization_name = Column(db.String(255))

    name = Column(db.String(255))
    description = Column(db.String(255))
    exams = Column(db.String(255))
