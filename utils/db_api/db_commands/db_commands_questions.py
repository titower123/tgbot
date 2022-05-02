from typing import List
from utils.db_api.quset import Question
from utils.db_api.database import db


async def add_question(user_id, full_name, question, date_time):
    await Question.create(user_id=str(user_id), full_name=full_name, question=question, date_and_time=date_time)

