# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/flash/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# run flake8
COPY . /usr/src/flash/
RUN flake8 --ignore=E501,F401 /usr/src/flash/

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/flash/entrypoint.sh
RUN chmod +x /usr/src/flash/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/flash/entrypoint.sh"]