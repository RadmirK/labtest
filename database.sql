DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Patients;
DROP TABLE IF EXISTS OAK_results;

create table Users (
	id INTEGER PRIMARY KEY autoincrement,
	username varchar(10) not null,
	password varchar(10) not null 
);

INSERT INTO Users values ( Null, 'admin', 'admin'); -- пользователь админ по-умолчанию

create table Patients (
	id integer primary key autoincrement,
	snils char(11) not null, -- номер снилс
	fName varchar(50) not null, -- имя пациента
	lName varchar(50) not null, -- фамилия пациента 
	mName varchar(50), -- отчество пациента 
	datebirth date not null, -- дата рождения 
	gender bit not null -- пол =  1-male, 0-female
);

create table OAK_results (
	id integer primary key autoincrement,
	testdate date not null, --дата
	patient_id integer not null, -- id пациента
	hemoglobin float(4, 2), -- гемоглобин г/л
	hematocrit float(3, 1), -- гематокрит %
	platelet_count int, --количество трамбоцитов, ед/мкл ~10^3
	leukocyte_count int, --кол-во лейкоцитов, ед/мкл ~10^3
	info varchar(100) -- kjkj
);

