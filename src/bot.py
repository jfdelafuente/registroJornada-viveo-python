import  telebot
from dotenv import load_dotenv
from datetime import date
import os
import telebot
import logging
import ViveOrange as viveOrange
from utils import get_daily_horoscope, add_day, get_info


load_dotenv()
token = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(token)

dic_user = {}

## logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# /start
@bot.message_handler(commands=['start'])
def _start(message):
    ## reset
    dic_user["id"] = str(message.chat.id)
    logging.info(str(message.chat.username)+" - "+str(message.chat.id)+" --- START")

    ## send first msg
    msg = "Hola "+str(message.chat.username)+\
          ", Soy el Registro de Jornadas de Orange. Para conocer los comandos, use \n/help"
    bot.send_message(message.chat.id, msg)


# /help
@bot.message_handler(commands=['help'])
def _help(message):
    msg = "Utilice los siguients comandos:\n\
        /dia - Realizar un registro de jornada\n\
        /info - Ver Registro semanal\n\
        /infop - Ver Registro semana pasada\n\
        /horoscope - Ver el Horoscopo "
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['dia'])
def dia_handler(message):
    logging.info(str(message.chat.username)+" - "+str(message.chat.id)+" --- DIA")
    text = "What day do you want to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)

def day_handler(message):
    day = message.text
    logging.info(str(message.text)+" --- DAY HANDLER")
    vive_orange = viveOrange.ViveOrange(True, False)
    # mensaje = vive_orange.connectar(dia)
    mensaje = vive_orange.dummy(day)
    # horoscope = add_day(day)
    # data = horoscope["data"]
    # horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id, "Here's your info!")
    # bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")
    bot.send_message(message.chat.id, mensaje, parse_mode="Markdown")

@bot.message_handler(commands=['info'])
def info_handler(message):
    logging.info(str(message.text)+" --- INFO REGISTRO SEMANA")
    dia = date.today()
    vive_orange = viveOrange.ViveOrange(False, False)
    mensaje = vive_orange.connectar(dia)
    # mensaje = vive_orange.dummy(dia)
    # horoscope = get_info()
    # data = horoscope["data"]
    # horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id, "Here's your info!")
    bot.send_message(message.chat.id, mensaje, parse_mode="Markdown")

@bot.message_handler(commands=['infop'])
def info_handler(message):
    logging.info(str(message.text)+" --- INFO REGISTRO SEMANA ANTERIOR")
    dia = date.today()
    vive_orange = viveOrange.ViveOrange(False, True)
    mensaje = vive_orange.connectar(dia)
    # mensaje = vive_orange.dummy(dia)
    # horoscope = get_info()
    # data = horoscope["data"]
    # horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id, "Here's your info!")
    # bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")
    bot.send_message(message.chat.id, mensaje, parse_mode="Markdown")

@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler2)


def day_handler2(message):
    sign = message.text
    text = "What day do you want to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg, fetch_horoscope, sign.capitalize())


def fetch_horoscope(message, sign):
    day = message.text
    horoscope = get_daily_horoscope(sign, day)
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id, "Here's your horoscope!")
    bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")

# non-command message
@bot.message_handler(func=lambda m: True)
def chat(message):
    txt = message.text
    if any(x in txt.lower() for x in ["thank","thx","cool"]):
        msg = "anytime"
    elif any(x in txt.lower() for x in ["hi","hello","yo","hey"]):
        msg = "yo" if str(message.chat.username) == "none" else "yo "+str(message.chat.username)
    else:
        msg = "obten ayuda  \n/help"
    bot.send_message(message.chat.id, msg)


def main():
    bot.polling()

if __name__ == '__main__':
    main()