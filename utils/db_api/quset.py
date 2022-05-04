from utils.db_api.database import db
from sqlalchemy import sql, Column, Sequence

class Question(db.Model):
    __tablename__ = 'question'
    query: sql.Select

    id = Column(db.Integer, Sequence("qusetion_seq"), primary_key=True)
    user_id = Column(db.String(60))
    message_id = Column(db.Integer)
    question = Column(db.Text)
    date_and_time = Column(db.String(60))