#Код для тестирования БД и API SQLite

import sqlite3


#Соединяемся к БД
conn = sqlite3.connect('lab_database.db')

#Создаем курсор - специальный объект, который делает запросы и получает их результаты
cursor = conn.cursor()

# Делаем INSERT запрос к базе данных, используя обычный SQL-синтаксис
# Позволяет делать лишь один запрос за раз!!!
# Чтоб использовать несколько запросов можно применять метод executescript()
cur = cursor.execute("""
	insert into Patients values (
		Null, 
		'12345678900', 
		'Ivan', 
		'Ivanov', 
		'Ivanovich', 
		'1999-01-01', 
		'Мужской'
	) 
""")
cursor.executescript("""
	INSERT INTO OAK_results VALUES (
		Null,
		strftime('2017-12-12'),
		2,
		1.4,
		10,
		120,
		140,
		'Сдох'
	);
""")
cur = cursor.execute("SELECT * FROM Patients")

rr=cur.fetchall()
print(type(rr))
print(rr)
cursor.execute("DELETE FROM Patients WHERE id = 59")
# Если мы не просто читаем, но и вносим изменения в базу данных - необходимо сохранить транзакцию
#conn.commit()

# Либо отменить изменения
conn.rollback()



"""
# Делаем SELECT запрос к базе данных, используя обычный SQL-синтаксис
cursor.execute("SELECT * FROM Patients")
# Получаем результат сделанного запроса
results = cursor.fetchall()

cursor.execute("SELECT * FROM OAK_results")
results2 = cursor.fetchall()

cursor.execute("SELECT * FROM Users")
results3 = cursor.fetchall()

print(results)  
print(results2) 
print(results3)

cursor.execute("SELECT id FROM Patients")
print(cursor.fetchone())
print(cursor.fetchone())

cursor.execute("SELECT * FROM Patients WHERE strftime('%Y', strftime(Patients.datebirth)) = '1999'")
print(cursor.fetchall())
"""





#Обязательно отключаемся от БД
conn.close()
