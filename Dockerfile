FROM python:3.9
RUN apt-get -y update && \
  apt-get install -y \
  python3-pip \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /root/.config/personal_project
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install -r rest_server/requirements.txt

EXPOSE 8080
