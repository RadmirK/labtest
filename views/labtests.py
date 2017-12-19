from flask import Blueprint, jsonify, abort, request
from application import get_db
from views.patients import check_id
tests_app = Blueprint('tests_app', __name__, url_prefix='/tests')


@tests_app.route('/', methods=['GET'], defaults={'test_id': 0})
@tests_app.route('/<int:test_id>', methods=['GET'])
def show_tests(test_id=0):
    patient_id = check_id(request.args.get('patient_id'))
    db = get_db()
    select = """
            SELECT OAK_results.*, PATIENTS.lName 
            FROM OAK_results, Patients 
            WHERE OAK_results.patient_id = Patients.id
            """
    if patient_id:  # Если необходимо отобразить анализы одного пациента
        select += " AND OAK_results.patient_id = %d" % patient_id
    if test_id:  # Отобразить данные одного анализа
        select += " AND OAK_results.id = %d" % test_id

    cur = db.execute(select)
    test = cur.fetchall()

    if test:
        return jsonify(test)
    else:
        abort(404, "Patient or test not found")


@tests_app.route('/<int:test_id>', methods=['DELETE'])
def del_test(test_id=0):
    """Удаляет один анализ"""

    """
    try:
        patient_id = int(request.args.get('patient_id'))
    except ValueError:
        abort(400, "Параметр patient_id введен не верно. Введите целое число")
    except:
        patient_id = 0
    """

    db = get_db()
    if test_id:  # Если задан номер анализа, то удаляем один
        cur = db.execute('SELECT id FROM OAK_results WHERE id = %d' % test_id)
        if cur.fetchone():  # Если есть такой, то удаляем
            db.execute('DELETE FROM OAK_results WHERE id = %d' % test_id)
        else:
            abort(404, "Анализы не найдены")
        """
    elif patient_id: #Иначе удаляем все анализы пациента
        cur = db.execute('SELECT id FROM Patients WHERE id = %d' % patient_id)
        if cur.fetchone(): #Если есть такой пациент, то удаляем
            cur = db.execute('DELETE FROM OAK_results WHERE patient_id = %d AND id = %d' % (patient_id))
        else:
            abort(404, "Данный пациент не найден")
        """
    else:
        abort(400, "Введите номер анализа для удаления")

    db.commit()
    return jsonify(result=True)


@tests_app.route('/', methods=['POST'], defaults={'edit_test_id': 0})
@tests_app.route('/<int:edit_test_id>', methods=['PUT', 'POST'])
def add_test(edit_test_id=0):
    """Добавить или редактировать данные анализа"""

    db = get_db()

    db_list = ['testdate', 'patient_id', 'hemoglobin', 'hematocrit', 'platelet_count', 'leukocyte_count',
               'info']  # Список всех имен входных параметров
    form_list = []  # Список имен принятых параметров
    req_form = []  # Значения входных параметров
    update = ''

    for i in db_list:  # Формируем входные формы
        try:
            req_form.append(request.form[i])
            form_list.append(i)
            update += i + '=%r' + ','  # Строка запроса UPDATE
        except:
            if request.method == 'POST':
                abort(400, "Заполните все поля")
    if update:
        update = update[0:-1]  # Удаляем лишнюю запятую

    for r in req_form:  # Проходим по формам
        if 'info' == form_list[req_form.index(r)]:
            # Доп. инфо опционально
            continue
        if not r:
            # Если форма пустая
            abort(400, 'Заполните все пустые поля (Кроме дополнительной информации)')

    if 'patient_id' in form_list:
        patient_id = check_id(req_form[form_list.index('patient_id')])

        cur = db.execute('SELECT id FROM Patients WHERE id = %d' % patient_id)
        if not cur.fetchone():
            abort(404,
                  """Данный пациент не найден. 
                  Необходимо ввести номер существующего пациента в формате ?edit_patient_id=<int>""")

    if request.method == 'POST':
        insert = """
        INSERT into OAK_results (testdate,  patient_id, hemoglobin, hematocrit, platelet_count, leukocyte_count, info) 
        values (%r, %r, %r, %r, %r, %r, %r)"""
        # подставляем входные данные в запрос
        db.execute(insert % tuple(req_form))

    if request.method == 'PUT':
        cur = db.execute('SELECT id FROM OAK_results WHERE id = %d' % edit_test_id)
        if not cur.fetchone():
            abort(404, "Laboratory test not found")
        update = "UPDATE OAK_results SET " + update + "WHERE id = %d" % edit_test_id
        db.execute(update % tuple(req_form))

    db.commit()
    return jsonify(result=True)
