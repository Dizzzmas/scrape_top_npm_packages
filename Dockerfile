# docker image that provides python dependencies and headless chrome

# https://hub.docker.com/r/justinribeiro/chrome-headless/dockerfile
FROM justinribeiro/chrome-headless
MAINTAINER dmytro@jetbridge.com

USER root

# deps
RUN apt update && apt upgrade -y
RUN apt install -yq --no-install-recommends unzip python3-pip python3-setuptools wget curl
# install chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
# clean up
RUN apt clean autoclean && apt autoremove --yes && rm -rf /var/lib/{apt,dpkg,cache,log}/

# create /app dir
COPY . /app
WORKDIR /app
RUN chown -R chrome:chrome /app
USER chrome

# deps
RUN pip3 install -r requirements.txt

# set display port to avoid crash
ENV DISPLAY=:99

ENTRYPOINT ["python3", "./main.py"]
