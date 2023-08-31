# Flashcard Language Learning App

## Table of Contents

- [General Info](#general-info)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
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




## Prerequisites

TODO

## Setup

TODO

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

TOTO
## Inspirations and Acknowledgments

TODO



