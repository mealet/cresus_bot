import nextcord
import os

BOT_TOKEN = os.environ.get("CRESUS_BOT_TOKEN")
COMMAND_PREFIX = "!"

INTENTS = nextcord.Intents.default()
INTENTS.message_content = True

PRESENCE_STATUS = nextcord.Status.online
PRESENCE_ACTIVITY = nextcord.Game(name="Пашет на заводе")
