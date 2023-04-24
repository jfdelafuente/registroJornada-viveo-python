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

def evaluar_dia_forzado(dia):
  mensaje = ''
  registrar = True
  print("Evaluamos el día forzado %s" % str(dia))
  return mensaje, registrar
  
def evaluar_dia(dia):
  mensaje = ''
  registrar = True
  TELETRABAJO = "No es dia de teletrabajo, tengo teletrabajo ocasional ? "
  FESTIVO = "Hoy es festivo/vacaciones, no cargamos registro de Jornada."
  hoy = dia.strftime("%d/%m/%Y")
  hoyFAnual = dia.strftime("%d/%m")

  print("Evaluamos dias:  %s %s " % (hoy, hoyFAnual))
  # print(dia.isoweekday())

  # Evaluamos Vacaciones y Festivos
  if hoy in configD.festivosOtros:
    mensaje += f'\n{FESTIVO}'
    registrar = False
    print("Evaluamos Vacaciones : %s : %s" % (FESTIVO, str(registrar)))
  elif hoyFAnual in configD.festivosAnuales:
    mensaje += f'\n{FESTIVO}'
    registrar = False
    print("Evaluamos Festivos : %s : %s" % (FESTIVO, str(registrar)))
  else:
    print("Ni vacas ni festivo")

  # Evaluamos Días de Teletrabajo
  if dia.isoweekday() not in configD.diasTeletrabajo:
    # print("isoweekday")
    registrar = hoy in configD.novoy
    print("Evaluamos dias de la semana: %s : %s" % (TELETRABAJO, str(registrar)))
    mensaje += f'\n{TELETRABAJO} : {registrar}'
  else:
    print("Corresponde a un día de teletrabajo y no he indicado Teletrabajo Ocasional.")
    
  return mensaje, registrar



def main():
  info = False
  pasada = False
  diaForzado = False 
  mensaje = "[REGISTRO JORNADA] "
  notificar = True
  registrar = True
  dia = date.today()
  # print(f'Argumentos recibidos: {len(sys.argv)}')
  
  if len(sys.argv) > 1:
    # print("Argumento de entrada: %s" % sys.argv[1])
    if "INFO" == sys.argv[1]:
      info = True
      registrar = False
      # print("Evaluamos INFO")
      # print("%s %s %s" % (info, pasada, diaForzado))
      mensaje += "Información Semanal "
    elif "INFOP" == sys.argv[1]:
      pasada = True
      info = True
      registrar = False
      # print("Evaluamos INFOP")
      # print("%s %s %s" % (info, pasada, diaForzado))
      mensaje += "Informacion Semana Anterior "
    elif "DIA" == sys.argv[1]:
      registrar = True
      notificar = True
      if len(sys.argv) > 2:
        dia = datetime.strptime(sys.argv[2], "%Y%m%d").date()
        diaForzado = True
        print("Evaluamos DIA FORZADO " + str(dia))
        # print("%s %s %s" % (info, pasada, diaForzado))
        #  mensaje += "DIA FORZADO " + str(dia)
        # evaluar_dia(dia) para probar, luego comentar
        # mensaje, registrar = evaluar_dia(dia)
      else:
        diaForzado = False
        print("Evaluamos DIA ACTUAL " + str(dia))
        # mensaje += "DIA ACTUAL " + str(dia)
        mensaje, registrar = evaluar_dia(dia)
    else:
      print("Error: %s no es un argumento de entrada válido." % sys.argv[1])
      registrar = False
      # exit(0)
      mensaje += ("Error: %s no es un argumento de entrada válido." % sys.argv[1])
      notificar = False
  else:
    print("Error: Debes incliuir un argumento válido: [INFO | INFOP | DIA [YYMMDD] ]")
    exit(0)
      
  print("Info : %s \nInfop : %s\nDia Forzado : %s\nNotificar : %s\nRegistrar : %s\nDia : %s " % (info, pasada, diaForzado, notificar, registrar, dia))
  if registrar != True:
    print("Causa : %s" % mensaje)

  
  if notificar == True:
    vOrange = viveOrange.ViveOrange(registrar, pasada)
    mensaje += vOrange.consultar(dia)
    # mensaje += vOrange.dummy(dia)

  # Lanzamos mensaje al bot
  bot = botTelegram.BotTelegramRegistro(BOT_TOKEN, CHAT_ID)
  bot.send_to_telegram(mensaje)
  # print("fin ... prueba : %s " % mensaje)


if __name__ == "__main__":
    main()