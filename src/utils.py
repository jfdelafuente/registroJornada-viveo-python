import requests
import configD
import logging
import ViveOrange as viveOrange
from datetime import date, datetime, timedelta


def get_daily_horoscope(sign: str, day: str) -> dict:
    """Get daily horoscope for a zodiac sign.
    Keyword arguments:
    sign:str - Zodiac sign
    day:str - Date in format (YYYY-MM-DD) OR TODAY OR TOMORROW OR YESTERDAY
    Return:dict - JSON data
    """
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)

    return response.json()

def add_day(day: str) -> dict:
    params = {  "data":{
                        "date": day,
                        "horoscope_data": "campo con info"
                        },
                "status": 200,
                "success": True
            }
    return params

def get_info() -> dict:
    params = {  "data":{
                        "date": "day",
                        "horoscope_data": "campo con info"
                        },
                "status": 200,
                "success": True
            }
    return params

def validar_dia(day: str):
    dia = date.today()
    if day == 'HOY':
        return dia
    elif day == 'AYER':
        ayer = dia - timedelta(days=1)
        return ayer
    else:
        try:
            dia = datetime.strptime(day, "%Y%m%d").date()
        except ValueError:
            return datetime(2023, 1, 1)
    return dia

def dia_validate(dia):
    mensaje = ''
    registrar = True
    hoy = dia.strftime("%d/%m/%Y")
    hoy_fanual = dia.strftime("%d/%m")

    # Evaluamos Vacaciones y Festivos
    if hoy in configD.festivosOtros:
        mensaje += f'\n{configD.VACACIONES}'
        registrar = False
        logging.debug("Evaluamos día --> Vacaciones : %s : %s" %
                        (configD.VACACIONES, str(registrar)))
    elif hoy_fanual in configD.festivosAnuales:
        mensaje += f'\n{configD.FESTIVO}'
        registrar = False
        logging.debug("Evaluamos día --> Festivos : %s : %s" %
                        (configD.FESTIVO, str(registrar)))
    else:
        logging.debug("Evaluamos día --> Ni vacas ni festivo")

    # Evaluamos Días de Teletrabajo
    if dia.isoweekday() not in configD.diasTeletrabajo:
        registrar = hoy in configD.novoy
        logging.debug("Evaluamos dias de la semana: %s : %s" %
                        (configD.TELETRABAJO, str(registrar)))
        mensaje += f'\n{configD.TELETRABAJO}'
    else:
        logging.debug(
            "Registramos el '%s', ya que corresponde a un día de teletrabajo y no he indicado Teletrabajo Ocasional." % dia)

    return mensaje, registrar