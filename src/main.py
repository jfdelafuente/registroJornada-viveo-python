import os
from datetime import date, datetime

import BotTelegramRegistro as botTelegram
import sys
import configD
import ViveOrange as viveOrange
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_FLAG =os.getenv('CHAT_FLAG')
CHAT_ID = os.getenv('CHAT_ID')


def evaluar_dia(dia):
  mensaje = ''
  hoy = dia.strftime("%d/%m/%Y")
  hoyFAnual = dia.strftime("%d/%m")

  print("Evaluamos dias:  %s %s" % (hoy, hoyFAnual))

  print(dia.isoweekday())


  if dia.isoweekday() not in configD.diasTeletrabajo:
    registrar = hoy in configD.novoy
    print("No es dia de teletrabajo, toca ofi, me quedo en casa?: " + str(registrar))
    mensaje += f'\nNo es dia de teletrabajo, toca ofi, me quedo en casa?:'

  if hoy in configD.festivosOtros:
    mensaje += f'\nHoy es festivo/vacaciones, no cargamos registro de Jornada'
    registrar = False
    print("Hoy es festivo/vacaciones, no cargamos registro de Jornada " + str(registrar))
  elif hoyFAnual in configD.festivosAnuales:
    mensaje += f'\nHoy es festivo anual, no cargamos registro de Jornada'
    registrar = False
    print("Hoy es festivo anual, no cargamos registro de Jornada")
    
  
  return mensaje, registrar



def main():
  info = False
  pasada = False
  diaForzado = False 
  mensaje = ""
  notificar = True
  registrar = True
  
  print(f'Argumentos recibidos: {len(sys.argv)}')
  
  if len(sys.argv) > 1:
    print("Argumento de entrada: %s" % sys.argv[1])
    if "INFO" == sys.argv[1]:
      info = True
      registrar = False
      print("Evaluamos INFO")
      print("%s %s %s" % (info, pasada, diaForzado))
      mensaje += "INFO "
    elif "INFOP" == sys.argv[1]:
      pasada = True
      info = True
      registrar = False
      print("Evaluamos INFOP")
      print("%s %s %s" % (info, pasada, diaForzado))
      mensaje += "INFOP "
    elif "DIA" == sys.argv[1]:
      if len(sys.argv) > 2:
        dia = datetime.strptime(sys.argv[2], "%Y%m%d").date()
        diaForzado = True
        registrar = True
        notificar = True
        print("Evaluamos DIA FORZADO " + str(dia))
        # print("%s %s %s" % (info, pasada, diaForzado))
        #  mensaje += "DIA FORZADO " + str(dia)
        mensaje, notificar = evaluar_dia(dia)
      else:
        dia = date.today()
        print("Evaluamos DIA ACTUAL " + str(dia))
        # mensaje += "DIA ACTUAL " + str(dia)
        mensaje, notificar = evaluar_dia(dia)
    else:
      print("Error: %s no es un argumento de entrada válido." % sys.argv[1])
      # exit(0)
      mensaje += ("Error: %s no es un argumento de entrada válido." % sys.argv[1])
      notificar = False
  else:
    print("Error: Debes incliuir un argumento válido: [INFO | INFOP | DIA [YYMMDD] ]")
    exit(0)
      
  
  if notificar != False:
    vOrange = viveOrange.ViveOrange(registrar, pasada)
    mensaje += vOrange.dummy()

  # Lanzamos mensaje al bot
  # bot = botTelegram.BotTelegramRegistro(BOT_TOKEN, CHAT_ID)
  # bot.send_to_telegram(mensaje)
  print("fin ... prueba : %s " % mensaje)


if __name__ == "__main__":
    main()