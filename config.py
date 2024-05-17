import telegram
import openai
import sys
import os

# get telegram bot token from config
BOT_TOKEN = os.getenv("BOT_TOKEN")

# get password from config
BOT_PASSWORD = os.getenv("BOT_PASSWORD")
# add user ids to access without password, leave empty if not known
AUTHORIZED_USERS = []

# get openai api key from config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Create an instance of the Bot
bot = telegram.Bot(token=BOT_TOKEN)

# Initialize the OpenAI API client
openai.api_key = OPENAI_API_KEY

# Define states for conversation
PASSWORD, ASSISTANT, DOCSEARCH, DOCSUM, SCAN = range(5)

LANGUAGE = "en"
VOICE = False

# Define the persona
global conversation_history
conversation_history = []

# add src folder to path
src_path = os.path.abspath('src')
sys.path.insert(0, src_path)