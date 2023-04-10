import requests
import json
<<<<<<< HEAD
import logging
=======
>>>>>>> fbd7af0d17a25b123d1f261a167baa104d4bb6bc

class BotTelegramRegistro:
    token = ''
    chat_id = ''

    def __init__(self, token, chat_id):
<<<<<<< HEAD
      logging.debug("%s %s" % (token, chat_id))
      self.token = token
      if (chat_id is None):
        logging.info("Buscamos el chat_id")
        self.chat_id = self._get_chat_id()
      else:
        logging.debug("Chat id : %s" % chat_id)
=======
      self.token = token
      if (chat_id is None):
        # print("Buscamos el chat_id")
        self.chat_id = self._get_chat_id()
      else:
        # print("Chat id %s" % chat_id)
>>>>>>> fbd7af0d17a25b123d1f261a167baa104d4bb6bc
        self.chat_id=chat_id

    def _get_chat_id(self):
      url = f"https://api.telegram.org/bot{self.token}/getUpdates"
<<<<<<< HEAD
      logging.debug(url)
      try:
          response = requests.get(url)
          logging.debug(response)
=======
      # print(url)
      try:
          response = requests.get(url)
          # print(response)
>>>>>>> fbd7af0d17a25b123d1f261a167baa104d4bb6bc
      except Exception as e:
          print(e)
      final = json.loads(response.text)
      chat_id = final['result'][0]['message']['chat']['id']
<<<<<<< HEAD
      logging.debug("chat id --> %s" % chat_id)
=======
      # print("chat id -->", chat_id)
>>>>>>> fbd7af0d17a25b123d1f261a167baa104d4bb6bc
      return chat_id
    
    def send_to_telegram(self, message):
      apiURL = f'https://api.telegram.org/bot{self.token}/sendMessage'
      try:
<<<<<<< HEAD
          response = requests.post(apiURL, 
                        json={'chat_id': self.chat_id, 
                              'text': message}
                        )
          logging.debug(response.text)
=======
          requests.post(apiURL, 
                        json={'chat_id': self.chat_id, 
                              'text': message}
                        )
          # print(response.text)
>>>>>>> fbd7af0d17a25b123d1f261a167baa104d4bb6bc
      except Exception as e:
          print(e)