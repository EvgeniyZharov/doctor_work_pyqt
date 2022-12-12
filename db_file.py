import pymysql
from config import host, user, password

con = pymysql.connect(
    host=host,
    port=3306,
    user=user,
    password=password,
    cursorclass=pymysql.cursors.DictCursor
)

DATABASE_NAME = "project_database_2"

TABLES = ["specialization", "doctor", "desease", "patient", "desease_history", "medecin", "treatment_plan",
          "appointment", "count_appointment"]


"""

drop function if exists project_database_2.price_coef;

delimiter $$
create function project_database_2.price_coef(a char(20), b char(20)) returns char(20)
deterministic
begin
	DECLARE c char(20);
	SET c = concat(a, b);
	return c;
END;
$$
delimiter ;

"""

"""

DELIMITER //
CREATE PROCEDURE project_database_2.proc (a int)
BEGIN

    select * 
    from project_database_2.appointment
    where appointment_id = a;
END //
DELIMITER ;

"""


def sql_procedure_appointment(appointment_id):
    request = f"CALL project_database_2.proc({appointment_id});"
    with con.cursor() as cur:
        cur.execute(request)
        return cur.fetchall()[0]


# print(sql_procedure_appointment(10))


def sql_function_conc(value_one, value_two):
    request = f"SELECT project_database_2.func({value_one}, {value_two});"
    with con.cursor() as cur:
        cur.execute(request)
        return cur.fetchone()[f'project_database_2.func({value_one}, {value_two})']


# print(sql_function_conc("123", "234"))


def create_main_db(title):
    try:
        request = f"CREATE DATABASE IF NOT EXISTS {title};"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def create_specialization_table():
    try:
        request = """CREATE TABLE IF NOT EXISTS project_database_2.specialization (course_id int AUTO_INCREMENT,
								 group_name VARCHAR(20) UNIQUE,
                                 category VARCHAR(20),
								 experience int,
                                 PRIMARY KEY(course_id));"""
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def create_doctor_table():
    try:
        request = """CREATE TABLE IF NOT EXISTS project_database_2.doctor (doctor_id int AUTO_INCREMENT,
								 doctor_name VARCHAR(20),
								 code VARCHAR(20) UNIQUE,
                                 grade VARCHAR(20),
                                 course_id int,
                                 FOREIGN KEY(course_id) REFERENCES specialization(course_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
                                 PRIMARY KEY(doctor_id));"""
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def create_desease_table():
    try:
        request = """CREATE TABLE IF NOT EXISTS project_database_2.desease (desease_id int AUTO_INCREMENT,
								 desease_name VARCHAR(20) UNIQUE,
                                 symptoms VARCHAR(200),
								 desease_description VARCHAR(500),
                                 PRIMARY KEY(desease_id));"""
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def create_patient_table():
    try:
        request = """CREATE TABLE IF NOT EXISTS project_database_2.patient (polis VARCHAR(50) NOT NULL,
								 patient_name VARCHAR(20),
                                 date_birth VARCHAR(20),
                                 reg_address VARCHAR(100),
                                 PRIMARY KEY(polis));"""
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def create_desease_history_table():
    try:
        request = """CREATE TABLE IF NOT EXISTS project_database_2.desease_history (polis VARCHAR(50),
								 predisposition VARCHAR(500),
                                 FOREIGN KEY(polis) REFERENCES patient(polis) ON DELETE NO ACTION ON UPDATE NO ACTION,
                                 PRIMARY KEY(polis));"""
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def create_medecin_table():
    try:
        request = """CREATE TABLE IF NOT EXISTS project_database_2.medecin (medecin_id int AUTO_INCREMENT,
								 title VARCHAR(20) UNIQUE,
                                 medecin_description VARCHAR(200),
                                 medecin_recipe VARCHAR(200),
                                 PRIMARY KEY(medecin_id));"""
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def create_treatment_plan_table():
    try:
        request = """CREATE TABLE IF NOT EXISTS project_database_2.treatment_plan (treatment_plan_id int AUTO_INCREMENT,
                                 title VARCHAR(20) UNIQUE,
								 medecin_id int,
                                 treatment_description VARCHAR(200),
                                 FOREIGN KEY(medecin_id) REFERENCES medecin(medecin_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
                                 PRIMARY KEY(treatment_plan_id));"""
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def create_appointment_plan_table():
    try:
        request = """CREATE TABLE IF NOT EXISTS project_database_2.appointment (appointment_id int AUTO_INCREMENT,
								 treatment_plan_id int,
                                 appointment_date VARCHAR(20),
                                 doctor_id int,
                                 desease_id int,
                                 polis VARCHAR(50),
                                 FOREIGN KEY(desease_id) REFERENCES desease(desease_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
                                 FOREIGN KEY(polis) REFERENCES desease_history(polis) ON DELETE NO ACTION ON UPDATE NO ACTION,
                                 FOREIGN KEY(treatment_plan_id) REFERENCES treatment_plan(treatment_plan_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
                                 FOREIGN KEY(doctor_id) REFERENCES doctor(doctor_id) ON DELETE CASCADE ON UPDATE CASCADE,
                                 PRIMARY KEY(appointment_id));"""
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def create_count_appointment_table():
    try:
        request = """CREATE TABLE IF NOT EXISTS project_database_2.count_appointment (doctor_id int,
								 count int,
                                 PRIMARY KEY(doctor_id));"""
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


print("*"*100)
print(create_main_db(DATABASE_NAME))
print(create_specialization_table())
print(create_doctor_table())
print(create_desease_table())
print(create_patient_table())
print(create_desease_history_table())
print(create_medecin_table())
print(create_treatment_plan_table())
print(create_appointment_plan_table())
print(create_count_appointment_table())
print("*"*100)


# DESCRIBE


def describe_table(table):
    if table in TABLES:
        show_table_query = f"DESCRIBE {DATABASE_NAME}.{table}"
        with con.cursor() as cur:
            cur.execute(show_table_query)
            # Fetch rows from last executed query
            result = cur.fetchall()
            for row in result:
                print(row)


# print("*"*100)
# for ii in range(len(TABLES)):
#     describe_table(TABLES[ii])
#     print()
# print("*"*100)


# INSERT

def add_specialization_in_table(group_name, category, experience):
    try:
        request = "INSERT INTO project_database_2.specialization (group_name, category, experience) VALUES (%s, %s, %s);"
        # request = "INSERT INTO users (name) VALUES (%s)"
        record = [(group_name, category, experience)]
        with con.cursor() as cur:
            cur.executemany(request, record)
            con.commit()
        return True
    except Exception:
        return False


def add_desease_in_table(desease_name, symptoms, desease_description):
    try:
        request = "INSERT INTO project_database_2.desease (desease_name, symptoms, desease_description) VALUES (%s, %s, %s);"
        # request = "INSERT INTO users (name) VALUES (%s)"
        record = [(desease_name, symptoms, desease_description)]
        with con.cursor() as cur:
            cur.executemany(request, record)
            con.commit()
        return True
    except Exception:
        return False


def add_count_appointment_in_table(doctor_id):
    try:
        request = "INSERT INTO project_database_2.count_appointment (doctor_id, count) VALUES (%s, %s);"
        # request = "INSERT INTO users (name) VALUES (%s)"
        record = [(doctor_id, 1)]
        with con.cursor() as cur:
            cur.executemany(request, record)
            con.commit()
        return True
    except Exception:
        return False


def add_doctor_in_table(doctor_name, code, grade, course_id):
    try:
        request = "INSERT INTO project_database_2.doctor (doctor_name, code, grade, course_id) VALUES (%s, %s, %s, %s);"
        # request = "INSERT INTO users (name) VALUES (%s)"
        record = [(doctor_name, code, grade, course_id)]
        with con.cursor() as cur:
            cur.executemany(request, record)
            con.commit()

            request = "SELECT doctor_id FROM project_database_2.doctor WHERE code = (%s)"
            cur.execute(request, (code,))
            doctor_id = cur.fetchall()[0]["doctor_id"]
            print(add_count_appointment_in_table(doctor_id))

        return True
    except Exception:
        return False


def add_patient_in_table(polis, patient_name, date_birth, reg_address):
    try:
        request = "INSERT INTO project_database_2.patient (polis, patient_name, date_birth, reg_address) VALUES (%s, %s, %s, %s);"
        # request = "INSERT INTO users (name) VALUES (%s)"
        record = [(polis, patient_name, date_birth, reg_address)]
        with con.cursor() as cur:
            cur.executemany(request, record)
            con.commit()
        return True
    except Exception:
        return False


def add_desease_history_in_table(polis, predisposition):
    try:
        request = "INSERT INTO project_database_2.desease_history (polis, predisposition) VALUES (%s, %s);"
        # request = "INSERT INTO users (name) VALUES (%s)"
        record = [(polis, predisposition)]
        with con.cursor() as cur:
            cur.executemany(request, record)
            con.commit()
        return True
    except Exception:
        return False


def add_medecin_in_table(title, medecin_description, medecin_recipe):
    try:
        request = "INSERT INTO project_database_2.medecin (title, medecin_description, medecin_recipe) VALUES (%s, %s, %s);"
        # request = "INSERT INTO users (name) VALUES (%s)"
        record = [(title, medecin_description, medecin_recipe)]
        with con.cursor() as cur:
            cur.executemany(request, record)
            con.commit()
        return True
    except Exception:
        return False


def add_treatment_plan_in_table(medecin_id, treatment_description, title):
    try:
        request = "INSERT INTO project_database_2.treatment_plan (medecin_id, treatment_description, title) VALUES (%s, %s, %s);"
        # request = "INSERT INTO users (name) VALUES (%s)"
        record = [(medecin_id, treatment_description, title)]
        with con.cursor() as cur:
            cur.executemany(request, record)
            con.commit()
        return True
    except Exception:
        return False


def add_appointment_in_table(treatment_plan_id, appointment_date, doctor_id, desease_id, polis):
    try:
        request = "INSERT INTO project_database_2.appointment (treatment_plan_id, appointment_date, doctor_id, desease_id, polis) VALUES (%s, %s, %s, %s, %s);"
        # request = "INSERT INTO users (name) VALUES (%s)"
        record = [(treatment_plan_id, appointment_date, doctor_id, desease_id, polis)]
        with con.cursor() as cur:
            cur.executemany(request, record)
            con.commit()
        return True
    except Exception:
        return False


print("*"*100)
print(add_specialization_in_table("alpha", "A", 2))
print(add_doctor_in_table("Vova", "123qwe", "dr", 1))
print(add_patient_in_table("1234567", "John", "01.02.2003", "Novaya Street"))
print(add_desease_history_in_table("1234567", "strong"))
print(add_desease_in_table("new desease", "pain", "makes felling pain"))
print(add_medecin_in_table("New medecin", "good pill", "Only with temperature more 38"))
print(add_treatment_plan_in_table(55, "only one time for day", "treatment two"))
print(add_appointment_in_table(7, "22.22.2222", 1, 1, "1234567"))

print("*"*100)


# UPDATE

def update_appointment(treatment_plan_id, doctor_id, desease_id, polis, appointment_id):
    try:
        request = f"UPDATE project_database_2.appointment SET treatment_plan_id = '{treatment_plan_id}' WHERE appointment_id = {appointment_id}"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
        request = f"UPDATE project_database_2.appointment SET doctor_id = '{doctor_id}' WHERE appointment_id = {appointment_id}"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
        request = f"UPDATE project_database_2.appointment SET desease_id = '{desease_id}' WHERE appointment_id = {appointment_id}"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
        request = f"UPDATE project_database_2.appointment SET polis = '{polis}' WHERE appointment_id = {appointment_id}"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()

        return True
    except Exception:
        return False

# print(update_appointment(57, 10))

# SELECT


def get_table(table_title):
    if table_title in TABLES:
        request = f"SELECT * FROM {DATABASE_NAME}.{table_title}"
        with con.cursor() as cur:
            cur.execute(request)
        return cur.fetchall()


print("*"*100)
for ii in range(len(TABLES)):
    print(get_table(TABLES[ii]))
print("*"*100)


# DELETE


def del_specialization_from_table(group_name):
    try:
        request = f"DELETE FROM {DATABASE_NAME}.specialization WHERE group_name = '{group_name}'"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def del_doctor_from_table(code):
    try:
        request = f"DELETE FROM {DATABASE_NAME}.doctor WHERE code = '{code}'"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def del_desease_from_table(desease_name):
    try:
        request = f"DELETE FROM {DATABASE_NAME}.desease WHERE desease_name = '{desease_name}'"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def del_patient_from_table(polis):
    try:
        request = f"DELETE FROM {DATABASE_NAME}.patient WHERE polis = '{polis}'"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def del_desease_history_from_table(polis):
    try:
        request = f"DELETE FROM {DATABASE_NAME}.desease_history WHERE polis = '{polis}'"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def del_medecin_from_table(medecin_id):
    try:
        request = f"DELETE FROM {DATABASE_NAME}.medecin WHERE medecin_id = '{medecin_id}'"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def del_treatment_plan_from_table(title):
    try:
        request = f"DELETE FROM {DATABASE_NAME}.treatment_plan WHERE title = '{title}'"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def del_appointment_plan_from_table(appointment_id):
    try:
        request = f"DELETE FROM {DATABASE_NAME}.appointment WHERE appointment_id = '{appointment_id}'"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False


def del_treatment_count_appointment_from_table(doctor_id):
    try:
        request = f"DELETE FROM {DATABASE_NAME}.count_appointment WHERE doctor_id = '{doctor_id}'"
        with con.cursor() as cur:
            cur.execute(request)
            con.commit()
            return True
    except Exception:
        return False
