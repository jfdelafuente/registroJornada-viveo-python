from datetime import datetime
import os
import BotTelegramRegistro as botTelegram
from DiaValidator import validate, dummy
from dotenv import load_dotenv

load_dotenv()

USER = os.environ['USUARIO']
PASSW = os.environ['PASS']
BOT_TOKEN = os.environ['BOT_TOKEN']
COD_EMPLEADO = os.environ['COD_EMPLEADO']
CHAT_FLAG =os.getenv('CHAT_FLAG')
CHAT_ID = os.getenv('CHAT_ID')


now = datetime.now()
mensaje = "[Telegram Test]" + now.strftime("%d/%m/%Y, %H:%M:%S")
dummy(now)
    

print("%s %s %s %s %s %s" % (USER, PASSW, BOT_TOKEN, COD_EMPLEADO, CHAT_FLAG, CHAT_ID))
# Lanzamos mensaje al bot
bot = botTelegram.BotTelegramRegistro(BOT_TOKEN, CHAT_ID)
print("Enviando mensaje: %s" % mensaje)
bot.send_to_telegram(mensaje)
