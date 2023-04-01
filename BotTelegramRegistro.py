import requests
import json


class BotTelegramRegistro:
    token = ''
    chat_id = ''

    def __init__(self, token):
        self.token = token
        url = f"https://api.telegram.org/bot{self.token}/getUpdates"
        try:
            response = requests.get(url)
            # print(response)
        except Exception as e:
            print(e)
        final = json.loads(response.text)
        chat_id = final['result'][0]['message']['chat']['id']
        # print("chat id -->", chat_id)
        self.chat_id=chat_id
    
    def send_to_telegram(self, message):
        apiURL = f'https://api.telegram.org/bot{self.token}/sendMessage'

        try:
            response = requests.post(
                apiURL, json={'chat_id': self.chat_id, 'text': message})
            # print(response.text)
        except Exception as e:
            print(e)