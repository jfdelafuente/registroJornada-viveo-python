import requests


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