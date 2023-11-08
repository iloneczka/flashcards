# Changelog

All notable changes to this project will be documented in this file.

## Version 0.15 (2023.11.06)
### Changed
- MANUAL ACTION REQUIRED: migrations files renamed. Before running this version manual execute the following instructions:
1. Stop running application.
```linux
docker-compose -f <composefile> down
```
Example:
```linux
docker-compose -f docker-compose.dev.yml down
```
2. Verify application is not running.
```linux
docker-compose  -f <composefile> ps
```
Example:
```linux
docker-compose  -f docker-compose.dev.yml ps
```
3. Run database container only.
```linux
docker-compose -f <composefile> up -d db
```
Example:
```linux
docker-compose -f docker-compose.dev.yml up -d db
```
4. Verify database container is running.
```linux
docker-compose  -f <composefile> ps
```
Example:
```linux
docker-compose  -f docker-compose.dev.yml ps
```
5. Enter database container.
```linux
docker exec -it <containername /bin/bash
```
Example:
```linux
docker exec -it flashcards-db-1 /bin/bash
```
6. Enter Djnango database.
```
psql --username=<django_username> --dbname=<django_database>
```
Example:
```
psql --username=hello_django --dbname=hello_django_dev
```
7. List applied migrations on application website.
```sql
SELECT * FROM django_migrations;
```
8. Execute following update statements.
```sql
UPDATE django_migrations SET name='0002_create_box_of_existing_cards' WHERE name='0002_box_alter_card_box';
UPDATE django_migrations SET name='0003_combine_cards_and_remove_empty_boxes' WHERE name='0003_box_alter_card_box';
UPDATE django_migrations SET name='0004_fix_empty_boxes' WHERE name='0004_box_alter_card_box';

```
9. List applied migrations on application website and verify them.
```sql
SELECT * FROM django_migrations;
```
10. Exit the database and the container.
`q`, `ctrl + D`
11. Stop database container.
```linux
docker-compose -f <composefile> down db
```
Example:
```linux
docker-compose -f docker-compose.dev.yml down
```
12. Proceed with the installation of the new version.


## Version 0.14 (2023.10.31)
### Added
- Integrated Django Rest Framework into the project by adding it to INSTALLED_APPS in settings.
- Created a `serializers.py` file for data serialization.
- Initial version of the API has been implemented.
### Changed
- Implemented `CardView` and `BoxView` as a `ModelViewSet` to handle API operations for the `Card` and `Box` model.
- Integrated the API view with existing views in `views.py`.
- Updated the `urls.py` file to include new API endpoints.

## Version 0.13 (2023.10.17)
### Edited
- MOVE button
### Added
- Automated Box Creation in Case of No Existing Boxes When Creating the First Card

## Version 0.12 (2023.10.13)
### Edited
- `all_cards.html` changed to `user_panel.html`
### Added
- in `user_panel`: Scrollspy List group of all boxes and its cards

## Version 0.11 (2023.10.04)
### Added
- class Box in models
### Edited
- Updated `home.html` based on new `models.py`

## Version 0.10 (2023.09.23)
### Added

Added notifications for incorrect login and password attempts.
### Edited
Updated `home.html`, the main template for selecting boxes.

## version 0.9 (2023.09.21)
### Added
- Register, Login and Logout options
- Log Out button in main navbar
### Edited
- `home.html` - Login overview

## version 0.8 (2023.09.11)
### Edited
- README.md
### Added
- initial tests of adding, deleting and changing cards

## version 0.7 (2023.08.31)
### Added
- Initial Docker containerization
- Add file dedicated to production configuration

## version 0.6 (2023.08.25)
### Deleted
- `cards_by_box.html`
- `flashcard_program_box.html`
### Edited
- Edit of `models.py`: update_rating and get_random_card_based_on_rating addes
### Added
- New funcionality: program display card based on its weight


## version 0.5 (2023.08.24)
### Edited
- `home.html`: start_button.png changed to box_1.png, box_2.png, box_3.png and all_cards.png
- All Cards changed to Cards in main navbar
### Added 
- Edit of main navbar in `base.html`: navbarDropdown added to Cards (dropdown items: All Cards, Box <box.number> )
- `cards_by_box.html` 
- `flashcard_program_box.html`


## version 0.4 (2023.08.23)
### Added 
- Edit `home.html`: start_button.png starting the flashcards.program
- Folder static


## version 0.3 (2023.08.16)
### Added 
- Edit export_cards template: added: export to pdf, csv and excel
- Edit in all_cards: delete and edit buttons


## version 0.2 (2023.08.15)
### Added 
- Edit of create_new_card template 
- Edit of home template 


## version 0.1 (2023.08.10)
### Added
- class Card in models.py
- new templates: `all_cards.html`, `create_new_card.html`, `import_cards.html`
- basic structure for aplication



