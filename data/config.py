from environs import Env

# используем библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")

PGUSER = env.str("pguser")
PGPASSWORD = env.str("pgpassword")
DB = env.str('database')

POSTGRESURI = f"postgresql://{PGUSER}:{PGPASSWORD}@{IP}/{DB}"

OPERATORS_IDS = env.list("OPERATORS")

