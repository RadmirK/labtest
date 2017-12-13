import os, sys, sqlite3

from flask import Flask, Blueprint, render_template, request, session, g, redirect, url_for, abort, flash

app = Flask(__name__)
app.config.from_object('config')

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'lab_database.db'),
	DEBUG = True,
	SECRET_KEY = 'development key',
	USERNAME = 'admin',
	PASSWORD = 'admin'
))

app.config.from_envvar('MY_SETTINGS', silent = True)


def init_db():
	"""Создаем базу данных по скрипту database.sql. Чтоб создать, надо единожды запустить метод"""
	with app.app_context():
		db = get_db()
		with app.open_resource('database.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv	
	
def get_db():
	"""Если ещё нет соединения с базой данных, открыть новое - для текущего контекста приложения
	"""
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.before_request
def before_request():
	"""pull user's profile from the database before every request are treated"""
	g.username = None
	if 'username' in session:
		g.username = session['username'] #User.query.get(session['username'])
			
@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			session['username'] = request.form['username']
			flash('You were logged in')
			return redirect(url_for('index'))
	
	return render_template('login.html', error=error)

	
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	session.pop('username', None)
	flash('You were logged out')
	return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404		

		
@app.teardown_appcontext
def close_db(error):
	"""Closes the database again at the end of the request."""
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()
	
from views.patients import patients_app
#from views.users import users_app
from views.labtests import tests_app

app.register_blueprint(patients_app)
#app.register_blueprint(users_app)
app.register_blueprint(tests_app)

