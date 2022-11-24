FROM clamav/clamav:latest


# INSTALL ADDITIONAL COMMANDS
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add --update --no-cache jq python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools


# INSTALL REQUIREMENTS
WORKDIR /app/
COPY requirements.txt   .
RUN pip install -r requirements.txt


# COPY THE SOURCE CODE
COPY ./  ./


# PRODUCTION
EXPOSE 4004
CMD gunicorn --bind 0.0.0.0:4004 run:server_instance


# HEALTHCHECK TO CHECK APP STATUS
HEALTHCHECK CMD curl --fail http://0.0.0.0:4004/accounts/status || exit 1