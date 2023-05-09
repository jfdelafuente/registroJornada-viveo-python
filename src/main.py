import os
from datetime import date, datetime

import BotTelegramRegistro as botTelegram
import sys
import logging
import ViveOrange as viveOrange
from DiaValidator import dia_validate
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.getenv('CHAT_ID')

logging.basicConfig(filename='registroJ.log', 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    level=logging.DEBUG)


def main():
  info = False
  pasada = False
  dia_forzado = False
  registrar = False
  notificar = True
  mensaje = "[REGISTRO JORNADA] "
  dia = date.today()
  logging.debug(f'Argumentos recibidos: {len(sys.argv)}')
  
  if len(sys.argv) > 1:
    logging.debug("Argumento de entrada: %s" % sys.argv[1])
    if "INFO" == sys.argv[1]:
      info = True
      logging.debug(" INFO: Info:%s Pasada:%s DiaForzado:%s" % (info, pasada, dia_forzado))
      mensaje += "Información Semanal "
    elif "INFOP" == sys.argv[1]:
      pasada = True
      logging.debug(" INFOP: Info:%s Pasada:%s DiaForzado:%s" % (info, pasada, dia_forzado))
      mensaje += "Informacion Semana Anterior "
    elif "DIA" == sys.argv[1]:
      registrar = True
      if len(sys.argv) > 2:
        dia = datetime.strptime(sys.argv[2], "%Y%m%d").date()
        dia_forzado = True
        logging.debug("DIA FORZADO: %s info:%s pasado:%s dia_forzado:%s" % (str(dia), info, pasada, dia_forzado))
        # evaluar_dia(dia) para probar, luego comentar
        mensaje, registrar = dia_validate(dia)
      else:
        dia_forzado = False
        logging.debug("DIA ACTUAL: %s info:%s pasado:%s dia_forzado:%s" % (str(dia), info, pasada, dia_forzado))
        mensaje, registrar = dia_validate(dia)
    else:
      print("Error: '%s' no es un argumento de entrada válido. Debes incluir un argumento válido: [INFO | INFOP | DIA [YYMMDD] ]" % sys.argv[1])
      logging.info("Error: '%s' no es un argumento de entrada válido. Debes incluir un argumento válido: [INFO | INFOP | DIA [YYMMDD] ]" % sys.argv[1])
      registrar = False
      exit(0)
  else:
    logging.info("Error: Debes incluir un argumento válido: [INFO | INFOP | DIA [YYMMDD] ]")
    print("Error: Debes incluir un argumento válido: [INFO | INFOP | DIA [YYMMDD] ]")
    exit(0)
      
  logging.debug("Resumen: %s \nInfo: %s\nInfop : %s\nDia Forzado : %s\nNotificar : %s\nRegistrar : %s " % (dia, info, pasada, dia_forzado, notificar, registrar))

  if notificar == True:
    vive_orange = viveOrange.ViveOrange(registrar, pasada)
    logging.info("Vive Orange connect")
    # mensaje += vive_orange.connectar(dia)
    mensaje += vive_orange.dummy(dia)

    # Lanzamos mensaje al bot
    logging.info("Enviamos el mensaje: '%s' al Bot" % mensaje)
    bot = botTelegram.BotTelegramRegistro(BOT_TOKEN, CHAT_ID)
    bot.send_to_telegram(mensaje)

  logging.debug("------------------- \n")


if __name__ == "__main__":
    main()