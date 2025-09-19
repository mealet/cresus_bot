import nextcord
import dotenv
import os

# WARNING: Обязательно замените значения с ID на свои!

DOTENV_FILE = ".env"

dotenv.load_dotenv(DOTENV_FILE)

BOT_TOKEN = os.environ.get("CRESUS_BOT_TOKEN")
COMMAND_PREFIX = "!"

INTENTS = nextcord.Intents.all()

PRESENCE_STATUS = nextcord.Status.online
PRESENCE_ACTIVITY = nextcord.Game(name="Пашет на заводе")

GUILD_ID = 1061673189765283921
MODERATION_ROLES = [1061676025077051502]

# Канал для кнопок с заявками на участие в проекте и помощника
PROJECT_APPLICATIONS_CHANNEL = 1063462165002067998
# Канал для получения заявок на участие в проекте
PROJECT_PARTICIPATION_RECIEVER = 1183144659820740618
# Канал для получения заявок на помощника
PROJECT_HELPER_RECIEVER = 1183144659820740618

LOGS_DIRECTORY = ".logs"
SQLITE_DATABASE_PATH = "database.db"
