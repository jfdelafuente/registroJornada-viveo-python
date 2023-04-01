import BotTelegramRegistro as bTR
import os
import json
from dotenv import load_dotenv

load_dotenv()

# una vez cargados los valores, podemos usarlos
BOT_TOKEN = os.getenv("BOT_TOKEN")

# print(" token : %s chatId: %s"  % (BOT_TOKEN, chatID))

bot = bTR.BotTelegramRegistro(BOT_TOKEN)
bot.send_to_telegram("hola pepe")
