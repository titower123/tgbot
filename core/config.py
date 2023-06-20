import enum
from functools import wraps

from environs import Env

# используем библиотеку environs

env = Env()
env.read_env()
BOT_TOKEN = env.str("BOT_TOKEN")
LOGGING_PATH = env.str("LOGGING_PATH")
BASE_URL_SERVER = env.str("BASE_URL_SERVER")
BASE_URL_AI = env.str("BASE_URL_AI")
LOGIN = env.str("LOGIN")
PASSWORD = env.str("PASSWORD")

admins = []
operators = []
moderators = []

class user_role(enum.Enum):
    user = 0
    operator = 1
    moderator = 2
    administrator = 3
    system_users = 6

FILE_ID = env.str("file_id")





def check_role(role: user_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            message = kwargs["call"]
            match role:
                case user_role.operator:
                    if message.from_user.id in operators:
                        return func(*args, **kwargs)
                    else:
                        return None
                case user_role.moderator:
                    if message.from_user.id in moderators:
                        return func(*args, **kwargs)
                    else:
                        return None
                case user_role.administrator:
                    if message.from_user.id in admins:
                        return func(*args, **kwargs)
                    else:
                        return None
                case user_role.system_users:
                    if message.from_user.id in operators or message.from_user.id in moderators or message.from_user.id in admins:
                        return func(*args, **kwargs)
                    else:
                        return None
        return wrapper
    return decorator



