# registroJornada-viveo-python
## Creamos un entorno virtual

El entorno virtual es muy útil y sobretodo cómodo para poder instalar librerías, y despreocuparnos de estropear la instalación Python que viene por defecto en los S.O. (en Mac o Linux). Ayuda a que luego se pueda trasportar el proyecto rápidamente a un contenedor, por ejemplo, conociendo con un comando las librerías que hemos usado, e instalándolas rápidamente con otro comando.

$>python -m venv venv
$>source venv/bin/activate
$>pip install -r requirements.txt

Siempre que instalemos o desinstalemos alguna dependencia, será necesario registrar estos cambios en el archivo requirements.txt:

$>pip freeze > requirements.txt

## Git

Para evitar que archivos innecesarios se alojen en el repositorio, debemos configurar el archivo .gitignore.

## Crear fichero de entorno (.env)

Necesitamos crear un archivo con el nombre .env para poder alojar datos privados como claves API, contraseñas, así como todo lo que relacionado con el proyecto. Agrega la siguiente información allí:

BOT_TOKEN=<token telegram> -> Token del bot de Telegram
CHAT_ID=<chat id telegram> -> Id del chat telegram al que enviar el mensaje
USUARIO=<usuario vive orange> --> ViveOrange
PASS=<password viver orange> --> ViveOrange
COD_EMPLEADO=<código empleado 800xxx> --> ViveOrange

Para usar esta información del archivo .env, debemos instalar otro módulo llamado python-decouple así:

$ pip install python-decouple


## Crear fichero configuracion (configD.py)

Poner el fichero configD.py en la misma ruta de una máquina que tenga acceso a internet (no es necesaria vpn) y python 3

Modificar el fichero configD.py indicando los siguientes datos

# Dias teletrabajo

Los códigos son los siguientes: (Lunes=1, Martes=2, Miercoles=3, Jueves=4, Viernes=5)
diasTeletrabajo = [1,2]

# Horas

hinicio = "8:00" -> Hora inicio de un día "normal"
hfin = "18:00" -> Hora fin de un día "normal"
hinicioV = "7:30" -> Hora inicio de un viernes
hfinV = "15:00" -> Hora fin de un viernes

En el mismo fichero puedes indicar los festivos en los que no habrí­a que cargar el registro de jornada

- Anuales (todos los años es festivo): se indican con el formato DD/MM
  festivosAnuales.append("08/12")
- Específicos (cambia segÃºn el año): se indican con el formato DD/MM/YYYY
  festivosOtros.append("20/03/2023")
  También puedes indicar los días en los que aunque tocaba ir a la oficina te has quedado teletrabajando
  novoy.append("20/12/2022")

Según los comandos con los que lo ejecutes:

- DIA -> Cargar el registro de jornada para el día actual
- DIA YYYYMMDD -> Carga el registro de jornada del día pasado por parámetro
  ./main.py DIA 20230119
- INFO -> Saca el informe con el registro de jornada de la semana en curso
  ./main.py INFO
- INFOP -> Saca el informe con el registro de jornada de la semana pasada
  ./main.py INFOP

Planificación en crontab

# Registro Jornada Orange

07 18 \* \* 1-5 cd /internet/regJornada/ ; /usr/bin/python3 registroJ.py >> /internet/regJornada/salida.txt

# Informe del registro de Jornada (semana pasada)

0 8 \* \* 1 cd /internet/regJornada/ ; /usr/bin/python3 registroJ.py INFOP >> /internet/regJornada/salida.txt


# docker

docker image build --tag viveorange .
docker run --name registrojornada -it --env-file=.env viveorange bash

ephemeral container que no salva la info localmente y delete despues de la ejecucion
docker run --rm -it --env-file=.env viveorange sh lanzar_cron.sh

