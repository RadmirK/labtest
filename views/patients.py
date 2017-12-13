from flask import Blueprint, g, request, render_template, flash, session, redirect, url_for
from application import get_db, app

patients_app = Blueprint('patients_app', __name__, url_prefix='/patients')

@patients_app.before_request
def before_request():
	"""Перед каждым запросом проверяет пользователя"""
	if  hasattr(g, 'username'):
		if g.username == None:
			return redirect(url_for('login'))
		
@patients_app.route('/')
def show_list():
	"""Отображает список пациентов"""
	db = get_db()
	cur = db.execute('SELECT * FROM patients')
	patients = cur.fetchall()
	return render_template('show_patients.html', patients=patients)
	
@patients_app.route('/<int:patient_id>')
def show_patient(patient_id):
	"""Отображает данные одного пациента"""
	db = get_db()
	cur = db.execute('SELECT * FROM PATIENTS WHERE id = %d' % patient_id)
	patient = cur.fetchall()
	return render_template('patient.html', patients=patient)
	
@patients_app.route('/del_patient/<int:patient_id>')
def del_patient(patient_id):
	"""Удаляет данные одного пациента"""
	mes = None 
	db = get_db()
	cur = db.execute('DELETE FROM PATIENTS WHERE id = %d' % patient_id)
	cur = db.execute('DELETE FROM OAK_results WHERE patient_id = %d' % patient_id)
	patient = cur.fetchall()
	db.commit()
	if patient:
		mes = 'Данного пациента в базе нет'
	else:
		mes = 'Данный пациент и все его анализы были удалены из базы'
	return redirect(url_for('patients_app.show_list'))
	
@patients_app.route('/add_patient', methods=['GET','POST'])
@patients_app.route('/add_patient/<int:edit_patient_id>', methods=['GET','POST'])
def add_patient(edit_patient_id=0):
	"""Добавить пациента"""
	db = get_db()
	error = None
	if request.method == 'POST':
		form_list = ['SNILS', 'fName', 'lName', 'mName', 'datebirth', 'gender'] #Список имен входных параметров
		req_form = [request.form[i] for i in form_list] #Значения входных параметров 
		def ind(str): #Возвращает индекс входного параметра по имени
			return form_list.index(str) 
		
		for r in req_form: 					#Проходим по формам
			if r != request.form['mName']:	#Отчество опционально
				if not r:	 				#Если остальные не пустые
					error = 'Заполните все поля (отчество не обязательно)'
		
		if len(request.form['SNILS']) != 11:#Длина СНИЛС должна быть 11 цифр
			for num in request.form['SNILS']:
				if not ('0' <= num <= '9'): #Проверяем чтоб были цифры
					error = 'Введите СНИЛС в правильном формате (состоит из 11 цифр) '
		#req_form[form_list.index('gender')] = (request.form['gender'] == '1') #Форматируем пол из строки в bool 
		

		if not error:
			insert = """INSERT into Patients (SNILS, fName, lName, mName, datebirth, gender) values (%r, %r, %r, %r, %r, %r)"""

			cur = db.execute(insert % tuple(req_form)) #подставляем входные данные в запрос
				
			patient = cur.fetchall() 
			db.commit()
			return redirect(url_for('patients_app.show_list'))
	
	cur = db.execute('SELECT * FROM PATIENTS WHERE id = %d' % edit_patient_id)
	edit_patient = cur.fetchone()

	return render_template('add_patient.html', error=error, patient=edit_patient)