# registroJornada-viveo-python

Poner los ficheros configD.py y registroJ.py en la misma ruta de una mÃ¡quina que tenga acceso a internet (no es necesaria vpn) y python 3
Es probable que no tengas todas las librerÃ­as de python instaladas. Es probable que falte algo o la instrucción no sea correcta pero serí­an:

pip install beautifulsoup4
pip install requests
pip install python-telegram-bot

Modificar el fichero configD.py indicando los siguientes datos

# Personales

username = "XXXXXX" -> Usuario con el que te logas en Vive Orange
password = "YYYYYY" -> Password con la que te logas en Vive Orange
codigoEmpleado = "000000" -> Tu código de empleado, 6 dígitos, sin los ceros

# Telegram
tgenviar = True -> Indica si quieres enviarte una notificación a Telegram (True | False)
tgtoken = '0000000000:AAAAAAA_sadfajsdfXXXXXX' -> Token del bot de Telegram
tgchatId = '00000000' -> Id del chat al que enviar el mensaje

# Dias teletrabajo (Lunes=1, Martes=2, Miercoles=3, Jueves=4, Viernes=5)
diasTeletrabajo = [1,2]

# Horas
hinicio = "8:00" -> Hora inicio de un día "normal"
hfin = "18:00" -> Hora fin de un día "normal"
hinicioV = "7:30" -> Hora inicio de un viernes
hfinV = "15:00" -> Hora fin de un viernes

En el mismo fichero puedes indicar los festivos en los que no habrÃ­a que cargar el registro de jornada

- Anuales (todos los años es festivo): se indican con el formato DD/MM
  festivosAnuales.append("08/12")
- Específicos (cambia segÃºn el año): se indican con el formato DD/MM/YYYY
  festivosOtros.append("20/03/2023")
  También puedes indicar los días en los que aunque tocaba ir a la oficina te has quedado teletrabajando
  novoy.append("20/12/2022")

Según los comandos con los que lo ejecutes:

- Vací­o -> Cargar el registro de jornada para el día actual
  ./registroJ.py
- DIA YYYYMMDD -> Carga el registro de jornada del día pasado por parÃ¡metro
  ./registroJ.py DIA 20230119
- INFO -> Saca el informe con el registro de jornada de la semana en curso
  ./registroJ.py INFO
- INFOP -> Saca el informe con el registro de jornada de la semana pasada
  ./registroJ.py INFOP

PlanificaciÃ³n en crontab

# Registro Jornada Orange

07 18 \* \* 1-5 cd /internet/regJornada/ ; /usr/bin/python3 registroJ.py >> /internet/regJornada/salida.txt

# Informe del registro de Jornada (semana pasada)

0 8 \* \* 1 cd /internet/regJornada/ ; /usr/bin/python3 registroJ.py INFOP >> /internet/regJornada/salida.txt
