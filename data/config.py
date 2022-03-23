from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

PGUSER = env.str("pguser")
PGPASSWORD = env.str("pgpassword")
DB = env.str('database')

POSTGRESURI = f"postgresql://{PGUSER}:{PGPASSWORD}@{IP}/{DB}"

support_ids = [
    467341786,
]