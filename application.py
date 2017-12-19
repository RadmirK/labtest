import os
import sqlite3

from flask import Flask, jsonify, g

app = Flask(__name__)
app.config.from_object('config')

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'lab_database.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin'
))

app.config.from_envvar('MY_SETTINGS', silent=True)


def init_db():
    """Создаем базу данных по скрипту database.sql. Чтоб создать, надо единожды запустить метод"""
    with app.app_context():
        db = get_db()
        with app.open_resource('database.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_db():
    def dict_factory(cursor, row):
        """Необходимо, чтоб любой запрос форматировал в формат json
        подробнее http://www.cdotson.com/2014/06/generating-json-documents-from-sqlite-databases-in-python/
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    rv = sqlite3.connect(app.config['DATABASE'])
    # rv.row_factory = sqlite3.Row
    rv.row_factory = dict_factory
    return rv


def get_db():
    """Если ещё нет соединения с базой данных, открыть новое - для текущего контекста приложения
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
        return g.sqlite_db
    else:
        return g.sqlite_db


@app.route('/')
def index():
    return jsonify(index="WELCOME!")


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
    pass


from views.patients import patients_app
from views.labtests import tests_app

app.register_blueprint(patients_app)
app.register_blueprint(tests_app)
