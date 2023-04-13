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

  if hoy in configD.festivosOtros:
    mensaje += f'\nHoy es festivo/vacaciones, no cargamos registro de Jornada'
    registrar = False
    print("Hoy es festivo/vacaciones, no cargamos registro de Jornada " + str(registrar))
  elif hoyFAnual in configD.festivosAnuales:
    mensaje += f'\nHoy es festivo anual, no cargamos registro de Jornada'
    registrar = False
    print("Hoy es festivo anual, no cargamos registro de Jornada")
    
  if datetime.today().isoweekday() not in configD.diasTeletrabajo:
    registrar = hoy in configD.novoy
    print("No es dia de teletrabajo, toca ofi, me quedo en casa?: " + str(registrar))
    mensaje += f'\nNo es dia de teletrabajo, toca ofi, me quedo en casa?:'
  
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
        # diaForzado = True
        registrar = True
        print("Evaluamos DIA FORZADO")
        print("%s %s %s" % (info, pasada, diaForzado))
        mensaje += "DIA FORZADO " + str(dia)
        mensaje, notificar = evaluar_dia(dia)
      else:
        print("Evaluamos DIA ACTUAL")
        dia = date.today()
        mensaje += "DIA ACTUAL " + str(dia)
        mensaje, notificar = evaluar_dia(dia)
    else:
      print("Error: %s no es un argumento de entrada válido." % sys.argv[1])
      # exit(0)
      notificar = False
  else:
    print("Error: Debes incliuir un argumento válido")
    exit(0)
      
  
  if notificar == False:
    mensaje += ("Error: %s no es un argumento de entrada válido." % sys.argv[1])
  else:
    vOrange = viveOrange.ViveOrange(registrar, pasada)
    mensaje += vOrange.dummy()

  # Lanzamos mensaje al bot
  bot = botTelegram.BotTelegramRegistro(BOT_TOKEN, CHAT_ID)
  bot.send_to_telegram(mensaje)
  print("fin ... prueba")


if __name__ == "__main__":
    main()