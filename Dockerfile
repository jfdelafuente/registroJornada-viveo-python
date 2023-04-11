# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10.4-slim-buster

RUN pip install --upgrade pip

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install cron

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ADD ./src/crontab /etc/cron.d/my-cron-file
RUN chmod 0644 /etc/cron.d/my-cron-file
RUN touch /var/log/cron.log
RUN crontab /etc/cron.d/my-cron-file


RUN useradd -m viveorange
USER viveorange

WORKDIR /home/viveorange

COPY --chown=viveorange:viveorange ./src/*.py ./
COPY --chown=viveorange:viveorange ./src/* ./
RUN chmod 0700 ./lanzar_cron.sh


# Install pip requirements
COPY --chown=viveorange:viveoragen requirements.txt ./
RUN python -m pip install --user -r requirements.txt

ENV PATH="/home/viveorage/.local/bin:${PATH}"

# CMD [ "cron", "-f" ]
CMD (cron -f &) && tail -f /var/log/cron.log