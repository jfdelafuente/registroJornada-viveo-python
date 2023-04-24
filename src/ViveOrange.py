from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import logging
import requests
import re
import configD
from dotenv import load_dotenv
import os

class ViveOrange:
  pasada = False
  registrar = True
  USER = ''
  PASSW = ''
  COD_EMPLEADO = ''

  def __init__(self, registrar, pasada):
    load_dotenv()
    self.pasada = pasada
    self.registrar = registrar
    self.USER = os.environ['USUARIO']
    self.PASSW = os.environ['PASS']
    self.COD_EMPLEADO = os.environ['COD_EMPLEADO']

  def dummy(self, dia):
    mensaje = "Dummy " + str(dia)
    logging.info("ViveOrange Dummy -->  '%s'" % mensaje)
    return mensaje

  def connectar(self, dia):
    hoy = dia.strftime("%d/%m/%Y")
    hinicio = configD.hinicio
    hfin = configD.hfin
    mensaje = ''

    peticionCMD = "{\"/vo_autologin.autologin/get-registra-tu-jornada\":{\"employeeNumber\":" + self.COD_EMPLEADO + "}}"
    
    #Nos tenemos que logar en Vive Orange para sacar la autorizacion del registro de jornada
    sHeaders = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'}
    s = requests.Session()
    s.headers.update(sHeaders)

    logging.info("Nos vamos a Vive Orange...")
    r = s.get(configD.urlVO)
    logging.info(r.status_code)

    soup = BeautifulSoup(r.text, 'lxml')
    soup1 = soup.select('body form')

    urlOAM = ''
    cabecerasOAM = {}
    
    for f in soup1:
        urlOAM = f.get('action')
        hidden_tags = f.find_all("input", type="hidden")
        for tag in hidden_tags:
            cabecerasOAM[tag.get("name")] = tag.get("value")
    
    logging.info("Nos vamos a OAM...")
    r = s.post(urlOAM, data=cabecerasOAM)
    
    soup = BeautifulSoup(r.text, 'lxml')
    soup1 = soup.select('form#loginData')
    
    urlOAM = configD.urlOAMBase
    cabecerasOAM = {}
    
    for f in soup1:
        urlOAM = urlOAM + f.get('action')
        hidden_tags = f.find_all("input", type="hidden")
        for tag in hidden_tags:
            if tag.get("name") == "username":
                cabecerasOAM["username"] = self.USER
            elif tag.get("name") == "password":
                cabecerasOAM["password"] = self.PASSW
            else:
                cabecerasOAM[tag.get("name")] = tag.get("value")
    cabecerasOAM["temp-username"] = self.USER
    cabecerasOAM["password"] = self.PASSW
    
    logging.info("Nos logamos en OAM...")
    r = s.post(urlOAM, data=cabecerasOAM)
    
    # Volvemos a Vive Orange
    soup = BeautifulSoup(r.text, 'lxml')
    soup1 = soup.select('body form')
    
    urlOAM = ''
    cabecerasOAM = {}
    
    for f in soup1:
        urlOAM = f.get('action')
        hidden_tags = f.find_all("input", type="hidden")
        for tag in hidden_tags:
            cabecerasOAM[tag.get("name")] = tag.get("value")
    
    logging.info("Volvemos a Vive Orange...")
    r = s.post(urlOAM, data=cabecerasOAM)
    
    
    r = s.get(configD.urlRegistroJ)
    
    authToken = re.findall(r".*Liferay.authToken\s?\=\s?'(.*)';",r.text)
    
    
    peticion = {}
    peticion["cmd"] = peticionCMD
    peticion["p_auth"] = authToken[0]
    logging.info("Buscamos la autenticacion para el registro de jornada...")
    r = s.post(configD.urlRegistroJC, data=peticion)
    
    # Nos logamos en la web del registro de jornada
    url = r.text.replace("\"","").replace("\\","")
    s = requests.Session()
    r = s.get(url)
    
    if self.registrar == True:
        logging.info("Cargamos registro jornada (ko valor normal) para " + hoy + 
                     " de " + hinicio + " a " + hfin)
        r = s.post(configD.urlRJAccion, data = {"tipoAccion":"horaRegistroCargada", 
                                                "motivo":"1", 
                                                "fechaini":hoy+" "+hinicio, 
                                                "fechafin":hoy+" "+hfin, 
                                                "sede":"","horaEfectiva":""
                                               })
        html_text = r.text
        mensaje += f'\nCargado registro de jornada {hoy} de {hinicio} a {hfin}'
    
    
    finD = date.today()
    #hoy5d = date.today() - timedelta(days=5)
    #hoy5 = hoy5d.strftime("%d/%m/%Y")
    lunesD = datetime.today() - timedelta(days=datetime.today().weekday() % 7)
    
    if self.pasada:
        lunesD = lunesD - timedelta(days=7)
        finD = lunesD + timedelta(days=4)
    
    lunes = lunesD.strftime("%d/%m/%Y")
    fin = finD.strftime("%d/%m/%Y")
    
    logging.info("Consultamos registro jornada desde " + lunes + " hasta " + fin)
    r = s.post(configD.urlRJInforme, data = {"tipoInforme":"1",
                                             "checkcodigo":"1", 
                                             "seleccionIdEmpleado":"", 
                                             "movil":"0",
                                             "seleccionFechaInicio":lunes+"", 
                                             "seleccionFechaFin":fin+""
                                            })
    html_text = r.text
    
    soup = BeautifulSoup(html_text, 'lxml')
    soup1 = soup.select('#tblEventos > tbody > tr')
    
    dias = 0 
    diasT = 0 
    diasF = 0 
    totalSegundos = 0 
    
    for i in soup1:
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
    return mensaje