#!/usr/bin/python3

from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import logging
import json
import requests
import re
import telegram
from telegram.error import NetworkError, Unauthorized
import time
import sys
#Importamos el fichero con la configuracion
import configD

logging.basicConfig(filename='registroJ.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

info = False
pasada = False
dia = date.today()
diaForzado = False

# Si llega INFO solo se saca el informe de horas (no se registra jornada)
# en el caso de INFOP ademas es para la semana anterior
logging.info(f'Argumentos recibidos: {len(sys.argv)}')
if len(sys.argv) > 1:
   logging.info(sys.argv[1])
   info = "INFO" in sys.argv[1]
   if "INFOP" == sys.argv[1]:
      pasada = True
   elif "DIA" == sys.argv[1]:
      if len(sys.argv) > 2:
         dia = datetime.strptime(sys.argv[2], "%Y%m%d").date()
         diaForzado = True


hoy = dia.strftime("%d/%m/%Y")
hoyFAnual = dia.strftime("%d/%m")
hinicio = configD.hinicio
hfin = configD.hfin

mensaje = '[Registro Jornada]'
notificar = True
registrar = True

if info:
   logging.info("Solo obtenemos informacion, no cargamos nuevo registro")
   registrar = False
else:
    if datetime.today().isoweekday() == 5:
        hinicio = configD.hinicioV
        hfin = configD.hfinV
    if hoy in configD.festivosOtros:
        mensaje += f'\nHoy es festivo/vacaciones, no cargamos registro de Jornada'
        registrar = False
    elif hoyFAnual in configD.festivosAnuales:
        mensaje += f'\nHoy es festivo anual, no cargamos registro de Jornada'
        registrar = False
    
    if datetime.today().isoweekday() not in configD.diasTeletrabajo:
        registrar = hoy in configD.novoy
        logging.info("No es dia de teletrabajo, toca ofi, me quedo en casa?: " + str(registrar))
        notificar = registrar

    if diaForzado:
        logging.info("Dia forzado, registramos")
        notificar = True
        registrar = True
        mensaje = '[Registro Jornada]'


if notificar == False:
    exit(0)

#Nos tenemos que logar en Vive Orange para sacar la autorizacion del registro de jornada
sHeaders = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'}
s = requests.Session()
s.headers.update(sHeaders)
logging.info("Nos vamos a Vive Orange...")
logging.debug("Cookies 1: " + str(s.cookies.get_dict()))
logging.debug("Headers 1: " + str(s.headers))
r = s.get(configD.urlVO)
logging.debug(r.headers)
logging.info(r.status_code)
logging.debug(r.cookies)
logging.debug(r.text)
logging.debug("Cookies 2: " + str(s.cookies.get_dict()))
logging.debug("Headers 2: " + str(s.headers))

soup = BeautifulSoup(r.text, 'lxml')
soup1 = soup.select('body form')

urlOAM = ''
cabecerasOAM = {}

for f in soup1:
    logging.debug(f.get('action'))
    urlOAM = f.get('action')
    hidden_tags = f.find_all("input", type="hidden")
    for tag in hidden_tags:
        logging.debug(tag)
        cabecerasOAM[tag.get("name")] = tag.get("value")

logging.info(urlOAM)
logging.info(cabecerasOAM)
logging.info("Nos vamos a OAM...")
r = s.post(urlOAM, data=cabecerasOAM)
logging.debug(r.headers)
logging.info(r.status_code)
logging.debug(r.cookies)
logging.debug(r.text)
logging.debug("Cookies 3: " + str(s.cookies.get_dict()))
logging.debug("Headers 3: " + str(s.headers))

soup = BeautifulSoup(r.text, 'lxml')
soup1 = soup.select('form#loginData')

urlOAM = configD.urlOAMBase
cabecerasOAM = {}

for f in soup1:
    logging.debug(f.get('action'))
    urlOAM = urlOAM + f.get('action')
    hidden_tags = f.find_all("input", type="hidden")
    for tag in hidden_tags:
        logging.debug(tag)
        if tag.get("name") == "username":
            cabecerasOAM["username"] = configD.username
        elif tag.get("name") == "password":
            cabecerasOAM["password"] = configD.password
        else:
            cabecerasOAM[tag.get("name")] = tag.get("value")
cabecerasOAM["temp-username"] = configD.username
cabecerasOAM["password"] = configD.password

logging.info(urlOAM)
logging.info(cabecerasOAM)
logging.info("Nos logamos en OAM...")
r = s.post(urlOAM, data=cabecerasOAM)
logging.debug(r.headers)
logging.info(r.status_code)
logging.debug(r.cookies)
logging.debug(r.text)
logging.debug("Cookies 4: " + str(s.cookies.get_dict()))
logging.debug("Headers 4: " + str(s.headers))

# Volvemos a Vive Orange
soup = BeautifulSoup(r.text, 'lxml')
soup1 = soup.select('body form')

urlOAM = ''
cabecerasOAM = {}

for f in soup1:
    logging.debug(f.get('action'))
    urlOAM = f.get('action')
    hidden_tags = f.find_all("input", type="hidden")
    for tag in hidden_tags:
        cabecerasOAM[tag.get("name")] = tag.get("value")

logging.info(urlOAM)
logging.info(cabecerasOAM)
logging.info("Volvemos a Vive Orange...")
r = s.post(urlOAM, data=cabecerasOAM)
logging.debug(r.headers)
logging.info(r.status_code)
logging.debug(r.cookies)
logging.debug(r.text)
logging.debug("Cookies 5: " + str(s.cookies.get_dict()))
logging.debug("Headers 5: " + str(s.headers))


r = s.get(configD.urlRegistroJ)
logging.debug(r.headers)
logging.info(r.status_code)
logging.debug(r.cookies)
logging.debug(r.text)
logging.debug("Cookies 6: " + str(s.cookies.get_dict()))
logging.debug("Headers 6: " + str(s.headers))

authToken = re.findall(r".*Liferay.authToken\s?\=\s?'(.*)';",r.text)
logging.debug(authToken)

peticion = {}
peticion["cmd"] = configD.peticionCMD
peticion["p_auth"] = authToken[0]
logging.debug(peticion)
logging.info("Buscamos la autenticacion para el registro de jornada...")
r = s.post(configD.urlRegistroJC, data=peticion)
logging.debug(r.headers)
logging.info(r.status_code)
logging.debug(r.cookies)
logging.info(r.text)
logging.debug("Cookies 7: " + str(s.cookies.get_dict()))
logging.debug("Headers 7: " + str(s.headers))

# Nos logamos en la web del registro de jornada
url = r.text.replace("\"","").replace("\\","")
s = requests.Session()
logging.info("Obtenemos jsessionid")
r = s.get(url)
logging.info(s.cookies.get("JSESSIONID"))
logging.info(r.headers)
logging.info(r.status_code)
logging.info(r.cookies)

if registrar == True:
    logging.info("Cargamos registro jornada (ko valor normal) para " + hoy + " de " + hinicio + " a " + hfin)
    r = s.post(configD.urlRJAccion, data = {"tipoAccion":"horaRegistroCargada","motivo":"1","fechaini":hoy+" "+hinicio,"fechafin":hoy+" "+hfin,"sede":"","horaEfectiva":""})
    html_text = r.text
    logging.info(html_text)
    logging.info(r.status_code)
    mensaje += f'\nCargado registro de jornada {hoy} de {hinicio} a {hfin}'


finD = date.today()
#hoy5d = date.today() - timedelta(days=5)
#hoy5 = hoy5d.strftime("%d/%m/%Y")
lunesD = datetime.today() - timedelta(days=datetime.today().weekday() % 7)

if pasada:
    lunesD = lunesD - timedelta(days=7)
    finD = lunesD + timedelta(days=4)

lunes = lunesD.strftime("%d/%m/%Y")
fin = finD.strftime("%d/%m/%Y")

logging.info("Consultamos registro jornada desde " + lunes + " hasta " + fin)
r = s.post(configD.urlRJInforme, data = {"tipoInforme":"1","checkcodigo":"1","seleccionIdEmpleado":"","movil":"0","seleccionFechaInicio":lunes+"","seleccionFechaFin":fin+""})
html_text = r.text
logging.info(html_text)
logging.info(r.status_code)

soup = BeautifulSoup(html_text, 'lxml')
soup1 = soup.select('#tblEventos > tbody > tr')

dias = 0 
diasT = 0 
diasF = 0 
totalSegundos = 0 

for i in soup1:
   logging.info(i.select_one('td:nth-child(1)').text)
   logging.info(i.select_one('td:nth-child(2)').text)
   logging.info(i.select_one('td:nth-child(3)').text)
   logging.info(i.select_one('td:nth-child(4)').text)
   logging.info(i.select_one('td:nth-child(5)').text)
   dInicio = datetime.strptime(i.select_one('td:nth-child(3)').text, '%d/%m/%Y %H:%M')
   dFin = datetime.strptime(i.select_one('td:nth-child(5)').text, '%d/%m/%Y %H:%M')
   totalSegundos += (dFin - dInicio).total_seconds()
   dias += 1
   if "TELETRABAJO" in i.select_one('td:nth-child(4)').text:
      diasT += 1
   if "FINCA" in i.select_one('td:nth-child(4)').text:
      diasF += 1

totalHoras = totalSegundos/3600
mensaje += f'\nInforme desde {lunes} hasta el {fin}:\n - {dias} dias trabajados ({diasT} teletrabajo, {diasF} La Finca)\n - Total horas: {totalHoras:.2f}'
logging.info(mensaje)

if configD.tgenviar == True:
      bot = telegram.Bot(configD.tgtoken)
  try:
    async def main():
      await bot.sendMessage(configD.tgchatId, text=mensaje)
  except Exception as e:
    print("Se ha producido un error en el envío por ID de Chat: %s" % .format(e));
