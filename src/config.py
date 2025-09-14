import nextcord
import dotenv
import os

DOTENV_FILE = ".env"

dotenv.load_dotenv(DOTENV_FILE)

BOT_TOKEN = os.environ.get("CRESUS_BOT_TOKEN")
COMMAND_PREFIX = "!"

INTENTS = nextcord.Intents.default()
INTENTS.message_content = True
INTENTS.members = True

PRESENCE_STATUS = nextcord.Status.online
PRESENCE_ACTIVITY = nextcord.Game(name="Пашет на заводе")

GUILD_IDS = [1061673189765283921]
MODERATION_ROLES = [1061676025077051502]
