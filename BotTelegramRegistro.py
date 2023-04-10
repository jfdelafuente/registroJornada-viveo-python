import requests
import json
import logging

class BotTelegramRegistro:
    token = ''
    chat_id = ''

    def __init__(self, token, chat_id):
      self.token = token
      if (chat_id is None):
        # print("Buscamos el chat_id")
        self.chat_id = self._get_chat_id()
      else:
        # print("Chat id %s" % chat_id)
        self.chat_id=chat_id

    def _get_chat_id(self):
      url = f"https://api.telegram.org/bot{self.token}/getUpdates"
      # print(url)
      try:
          response = requests.get(url)
          # print(response)
      except Exception as e:
          print(e)
      final = json.loads(response.text)
      chat_id = final['result'][0]['message']['chat']['id']
      # print("chat id -->", chat_id)
      return chat_id
    
    def send_to_telegram(self, message):
      apiURL = f'https://api.telegram.org/bot{self.token}/sendMessage'
      try:
          requests.post(apiURL, 
                        json={'chat_id': self.chat_id, 
                              'text': message}
                        )
          # print(response.text)
      except Exception as e:
          print(e)