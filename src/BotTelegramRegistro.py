import requests
import json
import logging

class BotTelegramRegistro:
    token = ''
    chat_id = ''

    def __init__(self, token, chat_id):
      #print("%s %s" % (token, chat_id))
      self.token = token
      if (chat_id is None):
        # print("Buscamos el chat_id")
        self.chat_id = self._get_chat_id()
      else:
        # print("Chat id : %s" % chat_id)
        self.chat_id=chat_id

    def _get_chat_id(self):
      url = f"https://api.telegram.org/bot{self.token}/getUpdates"
      try:
          response = requests.get(url)
          logging.debug("Bot get_chat_id --> %s " % response)
      except Exception as e:
          print(e)
      final = json.loads(response.text)
      chat_id = final['result'][0]['message']['chat']['id']
      logging.debug("chat id --> %s" % chat_id)
      return chat_id
    
    def send_to_telegram(self, message):
      url = f'https://api.telegram.org/bot{self.token}/sendMessage'
      try:
          response = requests.post(url, 
                        json={'chat_id': self.chat_id, 
                              'text': message}
                        )
          # print(response.text)
          logging.info("Bot send_to_telegram --> %s" % response.status_code)
      except Exception as e:
          print(e)