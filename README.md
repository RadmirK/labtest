# labtest
Тестовое задание веб-сервис "Лаборатория"

## Установлены
* Flask 0.12.2
* jinja2 2.10
* Flask WTForms 2.1
* SQLAlchemy 2.3.2 (однако применялся SQLite)

## Help
### Для запуска набрать 
python run.py

### Для инициализации/сброса базы данных SQLite
Макет базы данных находится в файле database.sql

python
 from application import init_db
 init_db()

## Процесс выполнения

####  13.12.2017: Выполнен первый набросок
1. Отображение списка пациентов
1. Отображение списка лабораторных анализов
1. Отображение данных пациента
1. Добавление данных пациента
1. Добавление данных анализов
1. Редактирование данных пациента
1. Редактирование данных анализов
1. Удаление пациента и всех его анализов
1. Удаление анализа пациента

####  18.12.2017: Переделан под API
Метод http | URL | Действие
-----------|------|----------
GET | http://[hostname]/patients | Получить список пациентов
GET | http://[hostname]/patients/<patient_id> | Получить данные одного пациента
POST | http://[hostname]/patients | Добавить нового пациента
PUT |  http://[hostname]/patients/<patient_id> | Редактировать данные пациента
DELETE | http://[hostname]/patients/<patient_id> | Удалить пациента
GET | http://[hostname]/tests/ | Получить список всех анализов
GET | http://[hostname]/tests/<test_id> | Получить данные одного анализа
GET | http://[hostname]/tests?patient_id=<patient_id> | Получить список анализов пациента
GET | http://[hostname]/tests/<test_id>?patient_id=<patient_id> | Получить данные одного анализа 
PUT | http://[hostname]/tests/<test_id> | Редактировать данные одного анализа
POST | http://[hostname]/tests/ | Добавить новый анализ
DELETE | http://[hostname]/tests/<test_id> | Удалить один анализ

#### Добавил файл запросов Postman labtest .postman_collection.json
#### 19.12.2017: Refactoring

