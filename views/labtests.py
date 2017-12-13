from flask import Blueprint, g, request, render_template, flash, session, redirect, url_for
from application import get_db
tests_app = Blueprint('tests_app', __name__, url_prefix='/tests')

@tests_app.before_request
def before_request():
	"""Перед каждым запросом проверяет пользователя"""
	if  hasattr(g, 'username'):
		if g.username == None:
			return redirect(url_for('login'))
			
@tests_app.route('/')
def show_list():
    db = get_db()
    cur = db.execute("""
		SELECT OAK_results.*, PATIENTS.lName 
		FROM OAK_results, Patients 
		WHERE OAK_results.patient_id = Patients.id""")
    tests = cur.fetchall()
    return render_template('show_tests.html', tests=tests, patient = 0)

@tests_app.route('/<int:patient_id>')
@tests_app.route('/<int:patient_id>/<int:test_id>')
def show_patient_tests(patient_id, test_id=0):
	db = get_db()
	if test_id: #Если необходимо отобразить один анализ
		cur = db.execute("""
			SELECT OAK_results.*, PATIENTS.lName 
			FROM OAK_results, Patients 
			WHERE patient_id = %d AND OAK_results.patient_id = Patients.id AND OAK_results.id = %d""" % (patient_id, test_id))
		tests = cur.fetchall()
		return render_template('test.html', tests = tests)
	else: #Иначе показать все анализы
		cur = db.execute("""
			SELECT OAK_results.*, PATIENTS.lName 
			FROM OAK_results, Patients 
			WHERE patient_id = %d AND OAK_results.patient_id = Patients.id""" % patient_id)
		tests = cur.fetchall()
		return render_template('show_tests.html', tests = tests, patient=patient_id)
	
@tests_app.route('/del_test/<int:patient_id>/<int:test_id>')
def del_test(patient_id, test_id=0):
	"""Удаляет один анализ одного пациента"""
	mes = None 
	db = get_db()
	if test_id: #Если задан номер анализа, то удаляем один
		cur = db.execute('DELETE FROM OAK_results WHERE patient_id = %d AND id = %d' % (patient_id, test_id))
	else: #Иначе удаляем все анализы пациента
		cur = db.execute('DELETE FROM OAK_results WHERE patient_id = %d AND id = %d' % (patient_id))
		
	delete = cur.fetchall()
	db.commit()
	if delete:
		mes = 'Данного пациента либо анализа в базе нет'
	else:
		mes = 'Данный анализ был удален из базы'
	return redirect(url_for('patients_app.show_patient', patient_id=patient_id))
	
@tests_app.route('/add_test/<int:patient_id>', methods=['GET','POST'])
@tests_app.route('/add_test/<int:patient_id>/<int:edit_test_id>', methods=['GET','POST'])
def add_test(patient_id , edit_test_id=0):
	"""Добавить анализ"""
	db = get_db()
	error = None
	if request.method == 'POST':
		form_list = ['testdate','hemoglobin','hematocrit', 'platelet_count', 'leukocyte_count', 'info'] #Список имен входных параметров
		req_form = [request.form[i] for i in form_list] #Значения входных параметров 
	
		for r in req_form: 					#Проходим по формам
			if r != request.form['info']:	#Доп. инфо опционально
				if not r:	 				#Если остальные не пустые
					error = 'Заполните все поля (Кроме дополнительной информации)'
		form_list.append('patient_id')
		req_form.append(patient_id)
		if not error:
			insert = """INSERT into OAK_results (testdate, hemoglobin,hematocrit, platelet_count, leukocyte_count, info, patient_id) values (%r, %r, %r, %r, %r, %r, %r)"""

			cur = db.execute(insert % tuple(req_form)) #подставляем входные данные в запрос
			patient = cur.fetchall() 
			db.commit()
			return redirect(url_for('tests_app.show_patient_tests', patient_id=patient_id))
	
	cur = db.execute('SELECT * FROM OAK_results WHERE id = %d' % edit_test_id)
	edit_test = cur.fetchone()	
	return render_template('add_test.html', patient_id=patient_id, test=edit_test, error=error)