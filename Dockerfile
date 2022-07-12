FROM python:3.7.2-stretch

# Env & Arg variables
ARG USERNAME=pythonssh
ARG USERPASS=sshpass

# Apt update & apt install required packages
# whois: required for mkpasswd
RUN apt update && apt -y install openssh-server whois jq clamav clamav-daemon

# Clamd Antivirus scanner setup
RUN freshclam
RUN service clamav-daemon restart

# Add a non-root user & set password
RUN useradd -ms /bin/bash $USERNAME
# Save username on a file ¿?¿?¿?¿?¿?
#RUN echo "$USERNAME" > /.non-root-username

# Set password for non-root user
RUN usermod --password $(echo "$USERPASS" | mkpasswd -s) $USERNAME

# Remove no-needed packages
RUN apt purge -y whois && apt -y autoremove && apt -y autoclean && apt -y clean

# Change to non-root user
USER $USERNAME
WORKDIR /home/$USERNAME

# Create the ssh directory and authorized_keys file
USER $USERNAME
RUN mkdir /home/$USERNAME/.ssh && touch /home/$USERNAME/.ssh/authorized_keys
USER root

WORKDIR /app/
COPY requirements.txt   .

RUN pip install -r requirements.txt

# COPY ALL THE REST OF THE SOURCE CODE
COPY ./  ./

WORKDIR /app/

# SETUP FLASK APP TO RUN
WORKDIR /app/

# PRODUCTION
ENV PYTHONUNBUFFERED=1
CMD gunicorn --bind 0.0.0.0:4005 run:server_instance
EXPOSE 4005

# HEALTHCHECK CMD curl --fail http://0.0.0.0:4000/accounts/status || exit 1