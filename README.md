# Flashcard Language Learning App

## Table of Contents

- [General Info](#general-info)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Running With Docker](#running-with-docker)
   - [Development](#development)
   - [Production](#production)
- [Running without Docker](#running-without-docker)
- [Testing](#testing)
- [Mechanism](#mechanism)
- [Future Plans](#future-plans)
- [Inspirations and Acknowledgments](#inspirations-and-acknowledgments)

## General Info

The Flashcard Language Learning App is a web application designed to help users learn languages through the use of digital flashcards. Users can create, edit, and organize flashcards into different boxes for effective learning.

## Features

- Create and manage flashcards
- Organize flashcards into different boxes
- Practice with flashcards using the flashcard program
- Export flashcards to various formats, including Excel, CSV, PDF, and HTML
- Edit and delete flashcards
- Print flashcards as a table

## Technologies Used

- Python

- Django

- HTML/CSS

- JavaScript

- Bootstrap (for styling)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)  ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)


## Running With Docker 

### __DEVELOPEMENT__

#### Prerequisites

Before running the app with Docker for developement, make sure you have Docker and Docker Compose installed on your system.

#### Usage

1. Build and start the Docker containers:

```
docker-compose -f docker-compose.dev.yml up -d --build
```
2. Apply migrations:

```
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate --noinput
```

3. Open your web browser and go to:

```
http://localhost:8000
```

### __PRODUCTION__

#### Prerequisites

Before running the app with Docker in production, make sure you have Docker and Docker Compose installed on your system.

#### Usage

1. Build and start the Docker containers:

```
docker-compose -f docker-compose.prod.yml up -d --build
```
2. Apply migrations:

```
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
```

3. Open your web browser and go to:

```
http://localhost:1337
```

## Running without Docker

### Prerequisites

Before running the app without Docker, make sure you have the following packages installed in your virtual environment:

```bash
asgiref==3.7.2
Django==4.2.4
Pillow==10.0.0
reportlab==4.0.4
sqlparse==0.4.4
XlsxWriter==3.1.2
psycopg2-binary==2.9.6
gunicorn==21.2.0
flake8==6.0.0
```
## Usage

1. Activate your virtual environment:

```
source virtual/bin/activate
```

2. Start the Django development server:

```
python manage.py runserver
```
3. Open your web browser and go to:
```
http://localhost:8000
```

## Testing

TODO

## Mechanism

### Flashcard Practice and Weighted Randomization

The Flashcard Language Learning App incorporates a practice feature that allows users to interact with flashcards in a more interactive manner. 
When practicing with a flashcard, users can click on one of the emoji icons – 🙁, 😐, or 🙂 – to rate their confidence in recalling the answer.

The app employs a weighted randomization technique that adjusts the frequency of flashcard appearances based on user ratings:

- 🙁 (Sad): Assigned a higher weight (e.g., 0.9) for more frequent practice.
- 😐 (Neutral): Given a moderate weight (e.g., 0.5) for average practice frequency.
- 🙂 (Happy): Allocated a lower weight (e.g., 0.1) for less frequent practice.

## Future Plans

- Implement user authentication at the beginning of the page (username and password) so that each user can have their own set of flashcards.
- Change the current boxes to be dynamic, allowing users to add and customize their names.
- Add the ability to import from CSV and Excel files, in addition to the existing export options.
- Make design enhancements, including the addition of graphics, and ensure the layout is responsive for both computers and mobile devices.


## Inspirations and Acknowledgments

I was inspired by my own need to learn Spanish, and flashcards have been a valuable tool for me in this process. That's why I decided to create my own program.

I drew inspiration from the following sources:

- [Dockerizing Django with Postgres, Gunicorn, and Nginx](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)

- The course "Learn Python Driven Web Development With Django and Python!" on Udemy by [John Elder](https://www.udemy.com/course/build-a-flashcard-website-with-python-and-django/learn/lecture/18296468#overview)

- [Real Python's Django Flashcards App Tutorial](https://realpython.com/django-flashcards-app/#demo-your-django-flashcards-app)




