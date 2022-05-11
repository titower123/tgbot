from sqlalchemy import sql, Column, Sequence
from utils.db_api.database import db


class Erros(db.Model):
    __tablename__ = 'errors'
    query: sql.Select

    id = Column(db.Integer, Sequence("errors_seq"), primary_key=True)
    date_and_time = Column(db.String(60))
    error = Column(db.Text)

