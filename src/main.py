import os
from datetime import date, datetime

import BotTelegramRegistro as botTelegram
import sys
import configD
import logging
import ViveOrange as viveOrange
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_FLAG =os.getenv('CHAT_FLAG')
CHAT_ID = os.getenv('CHAT_ID')

logging.basicConfig(filename='registroJ.log', 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    level=logging.DEBUG)

def evaluar_dia_forzado(dia):
  mensaje = ''
  registrar = True
  logging.debug("Evaluamos el día forzado %s" % str(dia))
  return mensaje, registrar
  
def evaluar_dia(dia):
  mensaje = ''
  registrar = True
  TELETRABAJO = "No es dia de teletrabajo, tengo teletrabajo ocasional ? "
  FESTIVO = "Hoy es festivo/vacaciones, no cargamos registro de Jornada."
  VACACIONES = "Hoy estás de vacaciones. Disfruta del día."
  hoy = dia.strftime("%d/%m/%Y")
  hoy_fanual = dia.strftime("%d/%m")

  # logging.debug("Evaluamos dias:  %s %s " % (hoy, hoy_fanual))
  # print(dia.isoweekday())

  # Evaluamos Vacaciones y Festivos
  if hoy in configD.festivosOtros:
    mensaje += f'\n{VACACIONES}'
    registrar = False
    logging.debug("Evaluamos día --> Vacaciones : %s : %s" % (VACACIONES, str(registrar)))
  elif hoy_fanual in configD.festivosAnuales:
    mensaje += f'\n{FESTIVO}'
    registrar = False
    logging.debug("Evaluamos día --> Festivos : %s : %s" % (FESTIVO, str(registrar)))
  else:
    logging.debug("Evaluamos día --> Ni vacas ni festivo")

  # Evaluamos Días de Teletrabajo
  if dia.isoweekday() not in configD.diasTeletrabajo:
    registrar = hoy in configD.novoy
    logging.debug("Evaluamos dias de la semana: %s : %s" % (TELETRABAJO, str(registrar)))
    mensaje += f'\n{TELETRABAJO} : {registrar}'
  else:
    logging.debug("Registramos el '%s', ya que corresponde a un día de teletrabajo y no he indicado Teletrabajo Ocasional." % dia)
    
  return mensaje, registrar



def main():
  info = False
  pasada = False
  dia_forzado = False 
  mensaje = "[REGISTRO JORNADA] "
  notificar = True
  registrar = True
  dia = date.today()
  logging.debug(f'Argumentos recibidos: {len(sys.argv)}')
  
  if len(sys.argv) > 1:
    logging.debug("Argumento de entrada: %s" % sys.argv[1])
    if "INFO" == sys.argv[1]:
      info = True
      registrar = False
      logging.debug(" INFO: Info:%s Pasada:%s DiaForzado:%s" % (info, pasada, dia_forzado))
      mensaje += "Información Semanal "
    elif "INFOP" == sys.argv[1]:
      pasada = True
      info = True
      registrar = False
      logging.debug(" INFOP: Info:%s Pasada:%s DiaForzado:%s" % (info, pasada, dia_forzado))
      mensaje += "Informacion Semana Anterior "
    elif "DIA" == sys.argv[1]:
      registrar = True
      notificar = True
      if len(sys.argv) > 2:
        dia = datetime.strptime(sys.argv[2], "%Y%m%d").date()
        dia_forzado = True
        logging.debug("DIA FORZADO: %s info:%s pasado:%s dia_forzado:%s" % (str(dia), info, pasada, dia_forzado))
        # evaluar_dia(dia) para probar, luego comentar
        mensaje, registrar = evaluar_dia(dia)
      else:
        dia_forzado = False
        logging.debug("DIA ACTUAL: %s info:%s pasado:%s dia_forzado:%s" % (str(dia), info, pasada, dia_forzado))
        mensaje, registrar = evaluar_dia(dia)
    else:
      print("Error: '%s' no es un argumento de entrada válido. Debes incluir un argumento válido: [INFO | INFOP | DIA [YYMMDD] ]" % sys.argv[1])
      logging.info("Error: '%s' no es un argumento de entrada válido. Debes incluir un argumento válido: [INFO | INFOP | DIA [YYMMDD] ]" % sys.argv[1])
      registrar = False
      exit(0)
      # mensaje += ("Error: '%s' no es un argumento de entrada válido." % sys.argv[1])
      # notificar = False
  else:
    logging.info("Error: Debes incluir un argumento válido: [INFO | INFOP | DIA [YYMMDD] ]")
    print("Error: Debes incluir un argumento válido: [INFO | INFOP | DIA [YYMMDD] ]")
    exit(0)
      
  logging.debug("Resumen: %s \nInfo: %s\nInfop : %s\nDia Forzado : %s\nNotificar : %s\nRegistrar : %s " % (dia, info, pasada, dia_forzado, notificar, registrar))
  # if registrar != True:
  #  logging.info("Causa : %s" % mensaje)

  
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