from sqlalchemy import sql, Column, Sequence
from utils.db_api.database import db


class NewUsers(db.Model):
    __tablename__ = 'new_users'
    query: sql.Select

    id = Column(db.Integer, Sequence("new_user_seq"), primary_key=True)
    user_id = Column(db.String(40))
    full_name = Column(db.String(255))
    date_and_time = Column(db.String(60))

