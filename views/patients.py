from flask import Blueprint, g, jsonify, abort, request, render_template, flash, session, redirect, url_for
from application import get_db, app

patients_app = Blueprint('patients_app', __name__, url_prefix='/patients')

@patients_app.route('/', methods=['GET'])
def show_list():
	"""Отображает список пациентов"""
	db = get_db()
	cur = db.execute('SELECT * FROM patients')
	patients = cur.fetchall()
	return jsonify(patients)
	
@patients_app.route('/<int:patient_id>', methods=['GET'])
def show_patient(patient_id):
	"""Отображает данные одного пациента"""
	db = get_db()
	cur = db.execute('SELECT * FROM PATIENTS WHERE id = %d' % patient_id)
	patient = cur.fetchall()
	if not patient:
		abort(404, "Patient not found")
	else:
		return jsonify(patient)
	
@patients_app.route('/<int:patient_id>', methods=['DELETE'])
def del_patient(patient_id):
	"""Удаляет данные одного пациента"""
	db = get_db()
	cur = db.execute('SELECT id FROM PATIENTS WHERE id = %d' % patient_id)
	patient = cur.fetchone() #Проверяем есть ли такой пациент
	if patient:
		cur = db.execute('DELETE FROM PATIENTS WHERE id = %d' % patient_id)
		cur = db.execute('DELETE FROM OAK_results WHERE patient_id = %d' % patient_id)
		db.commit()
		return jsonify(result=True)
	else:
		abort(404, "Patient id%d not found"%patient_id)

	
@patients_app.route('/', methods=['POST'])
@patients_app.route('/<int:edit_patient_id>', methods=['POST', 'PUT'])
def add_patient(edit_patient_id=0):
	"""Добавить пациента или изменить его данные"""
	db = get_db()
	error = ''
	#if request.method == 'POST' or request.method == 'PUT' :
	
	db_list = ['SNILS', 'fName', 'lName', 'mName', 'datebirth', 'gender'] #Список имен входных параметров
	form_list = []	#Параметры полученных данныъ
	req_form = []	#Полученные входные данные
	update = '' 	#Строка запроса
	for i in db_list:
		try:
			req_form.append(request.form[i])
			form_list.append(i)
			update += i + '= %r'+ ',' #формирование строки запроса UPDATE
		except:	None
		
	if update:
		update = update[0:-1] #Удаляем лишнюю последнюю запятую с запроса
	
	for r in req_form: 				#Проходим по формам
		if not r:	 				#Если остальные не пустые
			error += 'Заполните все пустые поля\n'
			
	if 'SNILS' in form_list:
		if len(request.form['SNILS']) != 11:
			error += 'Длина СНИЛС должна быть 11 цифр\n'
			for num in request.form['SNILS']:
				if not ('0' <= num <= '9'): #Проверяем чтоб были цифры
					error += 'Введите СНИЛС в правильном формате (состоит из 11 цифр) \n'
	
	print(error)	
	if not error:
		if request.method == 'POST':	
			insert = """INSERT into Patients (SNILS, fName, lName, mName, datebirth, gender) values (%r, %r, %r, %r, %r, %r)"""
			cur = db.execute(insert % tuple(req_form)) #подставляем входные данные в запрос
		
		if request.method == 'PUT':
			cur = db.execute("SELECT id FROM PATIENTS WHERE id = %d" % edit_patient_id)
			if cur.fetchone() is None:
				abort(404, "Данный пациент не найден")
			update = "UPDATE PATIENTS SET " + update + "WHERE id = %d" % edit_patient_id
			cur = db.execute (update % tuple(req_form)) #Выполняем запрос UPDATE table SET col1=val1, col2=val2, .. WHERE ..

		db.commit()
		return jsonify(result=True)
	else:
		abort(400, error) #Введенные данные не верны

