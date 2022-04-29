from typing import List
from sqlalchemy import and_
from utils.db_api.new_users import NewUsers
from utils.db_api.database import db
from datetime import datetime

async def add_user(user_id, full_name):
    now_time = datetime.now()
    now = now_time.strftime("[%m/%d/%Y][%H:%M:%S]")
    await NewUsers.create(user_id=str(user_id), full_name=full_name, date_and_time=now)

async def find_user(user_id):
    user = await NewUsers.query.where(NewUsers.user_id == str(user_id)).gino.first()
    if user == None:
        return True
    else:
        return False