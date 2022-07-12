FROM python:3.7.2-stretch

# Apt update & apt install required packages
RUN apt update && apt -y install jq clamav clamav-daemon

WORKDIR /app/
COPY requirements.txt   .

RUN pip install -r requirements.txt

# COPY ALL THE REST OF THE SOURCE CODE
COPY ./  ./

# PRODUCTION
ENV PYTHONUNBUFFERED=1
CMD gunicorn --bind 0.0.0.0:4005 run:server_instance
EXPOSE 4005

# HEALTHCHECK CMD curl --fail http://0.0.0.0:4000/accounts/status || exit 1