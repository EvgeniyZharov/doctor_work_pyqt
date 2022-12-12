from PyQt5 import QtWidgets, QtCore
import sys

from add_reception_window import Ui_Dialog
from add_patient_window import Ui_add_patient_window
from add_treatment_window import Ui_add_treatment_window
from reception_window import Ui_reception_window
from patient_window import Ui_patient
from treatment_window import Ui_treatment_window
from update_patient import Ui_update_patient_window
from update_reception import Ui_update_reception
from update_treatment import Ui_update_treatment_window

from db_file import get_table
from db_file import add_appointment_in_table
from db_file import add_patient_in_table
from db_file import add_treatment_plan_in_table
from db_file import del_appointment_plan_from_table
from db_file import del_patient_from_table
from db_file import del_treatment_plan_from_table
from db_file import sql_procedure_appointment
from db_file import sql_function_conc
from db_file import update_appointment

from datetime import datetime


KEY_WORD_DICT = {
    "reception": "",
    "reception__treatment": "",
    "reception__disease": "",
    "reception__patient": "",
    "reception__doctor": "",
    "patient": "",
    "treatment": "",
    "treatment__medicine": "",
    "search_doctor": "",
    "search_disease": ""
}


def start():
    reception_w.comboBox.clear()
    timetable_info = get_table("appointment")
    reception_w.comboBox.addItem("")
    for elem in timetable_info:
        reception_w.comboBox.addItem(str(elem["appointment_id"]))

    reception_total = 0
    count_classroom_info = get_table("count_appointment")
    for elem in count_classroom_info:
        reception_total += elem["count"]

    reception_w.comboBox_3.clear()
    disease_info = get_table("desease")
    reception_w.comboBox_3.addItem("")
    for elem in disease_info:
        reception_w.comboBox_3.addItem(elem["desease_name"])

    reception_w.comboBox_2.clear()
    doctor_info = get_table("doctor")
    reception_w.comboBox_2.addItem("")
    for elem in doctor_info:
        reception_w.comboBox_2.addItem(elem["code"])

    text = f"Итого приемов: {reception_total}"
    reception_w.label_3.setText(text)

    reception_window.show()


# BUTTONS

def reception__add_reception():
    add_reception_w.comboBox.clear()
    treatment_info = get_table("treatment_plan")
    add_reception_w.comboBox.addItem("")
    for elem in treatment_info:
        add_reception_w.comboBox.addItem(elem["title"])

    add_reception_w.comboBox_2.clear()
    disease_info = get_table("desease")
    add_reception_w.comboBox_2.addItem("")
    for elem in disease_info:
        add_reception_w.comboBox_2.addItem(elem["desease_name"])

    add_reception_w.comboBox_3.clear()
    prtient_info = get_table("patient")
    add_reception_w.comboBox_3.addItem("")
    for elem in prtient_info:
        add_reception_w.comboBox_3.addItem(elem["polis"])

    add_reception_w.comboBox_4.clear()
    doctor_info = get_table("doctor")
    add_reception_w.comboBox_4.addItem("")
    for elem in doctor_info:
        add_reception_w.comboBox_4.addItem(elem["code"])

    reception_window.close()
    add_reception_window.show()


def add_reception__reception():
    reception_info = get_table("treatment_plan")
    *reception_info, = filter(lambda x: x["title"] == KEY_WORD_DICT["reception__treatment"], reception_info)
    treatment_plan_id = reception_info[0]["treatment_plan_id"]

    disease_info = get_table("desease")
    *disease_info, = filter(lambda x: x["desease_name"] == KEY_WORD_DICT["reception__disease"], disease_info)
    desease_id = disease_info[0]["desease_id"]

    doctor_info = get_table("doctor")
    *doctor_info, = filter(lambda x: x["code"] == KEY_WORD_DICT["reception__doctor"], doctor_info)
    doctor_id = doctor_info[0]["doctor_id"]

    polis = KEY_WORD_DICT["reception__patient"]

    date = str(datetime.now()).split()[0]

    result = add_appointment_in_table(treatment_plan_id,
                                    date,
                                    doctor_id,
                                    desease_id,
                                    polis)
    print(result)

    reception_w.comboBox.clear()
    timetable_info = get_table("appointment")
    reception_w.comboBox.addItem("")
    for elem in timetable_info:
        reception_w.comboBox.addItem(str(elem["appointment_id"]))

    reception_total = 0
    count_appointment = get_table("count_appointment")
    for elem in count_appointment:
        reception_total += elem["count"]

    text = f"Итого приемов: {reception_total}"
    reception_w.label_3.setText(text)

    KEY_WORD_DICT["reception__doctor"] = ""
    KEY_WORD_DICT["reception__treatment"] = ""
    KEY_WORD_DICT["reception__patient"] = ""
    KEY_WORD_DICT["reception__disease"] = ""


    add_reception_window.close()
    reception_window.show()


def add_reception__reception__cancel():
    add_reception_window.close()
    reception_window.show()


def reception__patient():
    patient_w.comboBox.clear()
    timetable_info = get_table("patient")
    patient_w.comboBox.addItem("")
    for elem in timetable_info:
        patient_w.comboBox.addItem(elem["polis"])

    reception_window.close()
    patient_window.show()


def patient__reception():
    reception_w.comboBox.clear()
    timetable_info = get_table("appointment")
    reception_w.comboBox.addItem("")
    for elem in timetable_info:
        reception_w.comboBox.addItem(str(elem["appointment_id"]))

    reception_total = 0
    count_classroom_info = get_table("count_appointment")
    for elem in count_classroom_info:
        reception_total += elem["count"]

    text = f"Итого приемов: {reception_total}"
    reception_w.label_3.setText(text)

    patient_window.close()
    reception_window.show()


def patient__treatment():
    treatment_w.comboBox.clear()
    timetable_info = get_table("treatment_plan")
    treatment_w.comboBox.addItem("")
    for elem in timetable_info:
        treatment_w.comboBox.addItem(elem["title"])

    patient_window.close()
    treatment_window.show()


def patient__add_patient():

    patient_window.close()
    add_patient_window.show()


def add_patient__patient():
    polis = add_patient_w.lineEdit.text()
    name = add_patient_w.lineEdit_3.text()
    birth = add_patient_w.lineEdit_4.text()
    address = add_patient_w.lineEdit_5.text()

    result = add_patient_in_table(polis, name, birth, address)
    print(result)

    patient_w.comboBox.clear()
    timetable_info = get_table("patient")
    patient_w.comboBox.addItem("")
    for elem in timetable_info:
        patient_w.comboBox.addItem(elem["polis"])

    add_patient_window.close()
    patient_window.show()


def add_patient__patient__cancel():
    patient_w.comboBox.clear()
    timetable_info = get_table("patient")
    patient_w.comboBox.addItem("")
    for elem in timetable_info:
        patient_w.comboBox.addItem(elem["polis"])

    add_patient_window.close()
    patient_window.show()


def reception__treatment():
    treatment_w.comboBox.clear()
    timetable_info = get_table("treatment_plan")
    treatment_w.comboBox.addItem("")
    for elem in timetable_info:
        treatment_w.comboBox.addItem(elem["title"])

    reception_window.close()
    treatment_window.show()


def treatment__reception():
    reception_w.comboBox.clear()
    timetable_info = get_table("appointment")
    reception_w.comboBox.addItem("")
    for elem in timetable_info:
        reception_w.comboBox.addItem(str(elem["appointment_id"]))

    reception_total = 0
    count_classroom_info = get_table("count_appointment")
    for elem in count_classroom_info:
        reception_total += elem["count"]

    text = f"Итого приемов: {reception_total}"
    reception_w.label_3.setText(text)

    treatment_window.close()
    reception_window.show()


def treatment__patient():
    patient_w.comboBox.clear()
    timetable_info = get_table("patient")
    patient_w.comboBox.addItem("")
    for elem in timetable_info:
        patient_w.comboBox.addItem(elem["polis"])

    treatment_window.close()
    patient_window.show()


def treatment__add_treatment():
    add_treatment_w.comboBox.clear()
    corpus_info = get_table("medecin")
    add_treatment_w.comboBox.addItem("")
    for elem in corpus_info:
        add_treatment_w.comboBox.addItem(elem["title"])

    treatment_window.close()
    add_treatment_window.show()


def add_treatment__treatment():
    title = add_treatment_w.lineEdit.text()
    treatment__medicine = KEY_WORD_DICT["treatment__medicine"]
    description = add_treatment_w.textEdit.toPlainText()

    medecin_info = get_table("medecin")
    *medecin_info, = filter(lambda x: x["title"] == treatment__medicine, medecin_info)
    medecin_id = medecin_info[0]["medecin_id"]

    result = add_treatment_plan_in_table(medecin_id, description, title)
    print(result)

    treatment_w.comboBox.clear()
    timetable_info = get_table("treatment_plan")
    treatment_w.comboBox.addItem("")
    for elem in timetable_info:
        treatment_w.comboBox.addItem(elem["title"])

    add_treatment_window.close()
    treatment_window.show()


def add_treatment__treatment__cancel():

    add_treatment_window.close()
    treatment_window.show()


# TO UPDATE

def reception_to_update():
    if KEY_WORD_DICT["reception"]:
        appointment = sql_procedure_appointment(KEY_WORD_DICT["reception"])

        update_reception_w.comboBox.clear()
        treatment_info = get_table("treatment_plan")
        update_reception_w.comboBox.addItem("")
        for elem in treatment_info:
            if elem["treatment_plan_id"] == appointment["treatment_plan_id"]:
                KEY_WORD_DICT["reception__treatment"] = elem["title"]
                treatment_plan = elem["title"]
            update_reception_w.comboBox.addItem(elem["title"])

        update_reception_w.comboBox_2.clear()
        disease_info = get_table("desease")
        update_reception_w.comboBox_2.addItem("")
        for elem in disease_info:
            if elem["desease_id"] == appointment["desease_id"]:
                KEY_WORD_DICT["reception__disease"] = elem["desease_name"]
                desease = elem["desease_name"]
            update_reception_w.comboBox_2.addItem(elem["desease_name"])

        update_reception_w.comboBox_3.clear()
        prtient_info = get_table("patient")
        update_reception_w.comboBox_3.addItem("")
        for elem in prtient_info:
            if elem["polis"] == appointment["polis"]:
                KEY_WORD_DICT["reception__patient"] = elem["polis"]
                polis = elem["polis"]
            update_reception_w.comboBox_3.addItem(elem["polis"])

        update_reception_w.comboBox_4.clear()
        doctor_info = get_table("doctor")
        update_reception_w.comboBox_4.addItem("")
        for elem in doctor_info:
            if elem["doctor_id"] == appointment["doctor_id"]:
                KEY_WORD_DICT["reception__doctor"] = elem["code"]
                code = elem["code"]
            update_reception_w.comboBox_4.addItem(elem["code"])

        index = update_reception_w.comboBox.findText(treatment_plan)
        update_reception_w.comboBox.setCurrentIndex(index)

        index = update_reception_w.comboBox_2.findText(desease)
        update_reception_w.comboBox_2.setCurrentIndex(index)

        index = update_reception_w.comboBox_3.findText(polis)
        update_reception_w.comboBox_3.setCurrentIndex(index)

        index = update_reception_w.comboBox_4.findText(code)
        update_reception_w.comboBox_4.setCurrentIndex(index)

        reception_window.close()
        update_reception_window.show()


def reception_from_update():
    reception_info = get_table("treatment_plan")
    *reception_info, = filter(lambda x: x["title"] == KEY_WORD_DICT["reception__treatment"], reception_info)
    treatment_plan_id = reception_info[0]["treatment_plan_id"]

    disease_info = get_table("desease")
    *disease_info, = filter(lambda x: x["desease_name"] == KEY_WORD_DICT["reception__disease"], disease_info)
    desease_id = disease_info[0]["desease_id"]

    doctor_info = get_table("doctor")
    *doctor_info, = filter(lambda x: x["code"] == KEY_WORD_DICT["reception__doctor"], doctor_info)
    doctor_id = doctor_info[0]["doctor_id"]

    polis = KEY_WORD_DICT["reception__patient"]

    date_info = get_table("appointment")
    *date_info, = filter(lambda x: x["appointment_id"] == KEY_WORD_DICT["reception"], date_info)
    date = date_info[0]["appointment_date"]

    result = update_appointment(treatment_plan_id,
                                      doctor_id,
                                      desease_id,
                                      polis,
                                      KEY_WORD_DICT["reception"])
    print(result)

    reception_w.comboBox.clear()
    timetable_info = get_table("appointment")
    reception_w.comboBox.addItem("")
    for elem in timetable_info:
        reception_w.comboBox.addItem(str(elem["appointment_id"]))

    reception_total = 0
    count_appointment = get_table("count_appointment")
    for elem in count_appointment:
        reception_total += elem["count"]

    text = sql_function_conc("Итого приемов:", "{reception_total}")
    reception_w.label_3.setText(text)

    KEY_WORD_DICT["reception__doctor"] = ""
    KEY_WORD_DICT["reception__treatment"] = ""
    KEY_WORD_DICT["reception__patient"] = ""
    KEY_WORD_DICT["reception__disease"] = ""

    update_reception_window.close()
    reception_window.show()


def reception_from_update_cancel():
    KEY_WORD_DICT["reception__doctor"] = ""
    KEY_WORD_DICT["reception__treatment"] = ""
    KEY_WORD_DICT["reception__patient"] = ""
    KEY_WORD_DICT["reception__disease"] = ""

    update_reception_window.close()
    reception_window.show()


def patient_to_update():
    if KEY_WORD_DICT["patient"]:
        patient_info = get_table("patient")
        *patient_info, = filter(lambda x: x["polis"] == KEY_WORD_DICT["patient"], patient_info)
        patient_name = patient_info[0]["patient_name"]
        date_birth = patient_info[0]["date_birth"]
        reg_address = patient_info[0]["reg_address"]

        update_patient_w.lineEdit.setText(KEY_WORD_DICT["patient"])
        update_patient_w.lineEdit_3.setText(patient_name)
        update_patient_w.lineEdit_4.setText(date_birth)
        update_patient_w.lineEdit_5.setText(reg_address)

        patient_window.close()
        update_patient_window.show()


def patient_from_update():
    polis = update_patient_w.lineEdit.text()
    name = update_patient_w.lineEdit_3.text()
    birth = update_patient_w.lineEdit_4.text()
    address = update_patient_w.lineEdit_5.text()

    result = del_patient_from_table(KEY_WORD_DICT["patient"])
    print(result)

    result = add_patient_in_table(polis, name, birth, address)
    print(result)

    patient_w.comboBox.clear()
    timetable_info = get_table("patient")
    patient_w.comboBox.addItem("")
    for elem in timetable_info:
        patient_w.comboBox.addItem(elem["polis"])

    update_patient_window.close()
    patient_window.show()


def patient_from_update_cancel():
    update_patient_window.close()
    patient_window.show()


def treatment_to_update():
    if KEY_WORD_DICT["treatment"]:
        title = KEY_WORD_DICT["treatment"]
        treatment_info = get_table("treatment_plan")
        *treatment_info, = filter(lambda x: x["title"] == title, treatment_info)
        medecin_id = treatment_info[0]["medecin_id"]
        treatment_description = treatment_info[0]["treatment_description"]

        update_treatment_w.lineEdit.setText(title)
        update_treatment_w.textEdit.setText(treatment_description)

        update_treatment_w.comboBox.clear()
        medecin_info = get_table("medecin")
        for elem in medecin_info:
            update_treatment_w.comboBox.addItem(elem["title"])
            if elem["medecin_id"] == medecin_id:
                medecin_title = elem["title"]


        treatment_window.close()
        update_treatment_window.show()


def treatment_from_update():
    title = update_treatment_w.lineEdit.text()
    treatment__medicine = KEY_WORD_DICT["treatment__medicine"]
    description = update_treatment_w.textEdit.toPlainText()

    medecin_info = get_table("medecin")
    *medecin_info, = filter(lambda x: x["title"] == treatment__medicine, medecin_info)
    medecin_id = medecin_info[0]["medecin_id"]

    print(title)
    print(medecin_id)
    print(description)

    result = del_treatment_plan_from_table(KEY_WORD_DICT["treatment"])
    print(result)

    result = add_treatment_plan_in_table(medecin_id, description, title)
    print(result)

    treatment_w.comboBox.clear()
    timetable_info = get_table("treatment_plan")
    treatment_w.comboBox.addItem("")
    for elem in timetable_info:
        treatment_w.comboBox.addItem(elem["title"])

    update_treatment_window.close()
    treatment_window.show()


def treatment_from_update_cancel():
    update_treatment_window.close()
    treatment_window.show()


# DELETE BUTTON

def delete_reception():
    appointment_id = int(KEY_WORD_DICT["reception"])
    result = del_appointment_plan_from_table(appointment_id)
    print(result)

    reception_w.comboBox.clear()
    timetable_info = get_table("appointment")
    reception_w.comboBox.addItem("")
    for elem in timetable_info:
        reception_w.comboBox.addItem(str(elem["appointment_id"]))

    reception_total = 0
    count_classroom_info = get_table("count_appointment")
    for elem in count_classroom_info:
        reception_total += elem["count"]

    text = f"Итого приемов: {reception_total}"
    reception_w.label_3.setText(text)


def delete_patient():
    polis = KEY_WORD_DICT["patient"]
    result = del_patient_from_table(polis)
    print(result)

    patient_w.comboBox.clear()
    timetable_info = get_table("patient")
    patient_w.comboBox.addItem("")
    for elem in timetable_info:
        patient_w.comboBox.addItem(elem["polis"])


def delete_treatment():
    title = KEY_WORD_DICT["treatment"]
    result = del_treatment_plan_from_table(title)
    print(result)

    treatment_w.comboBox.clear()
    timetable_info = get_table("treatment_plan")
    treatment_w.comboBox.addItem("")
    for elem in timetable_info:
        treatment_w.comboBox.addItem(elem["title"])


# SEARCH

def search():
    disease = KEY_WORD_DICT["search_disease"]
    doctor = KEY_WORD_DICT["search_doctor"]

    def search_for_doctor():
        doctor_info = get_table("doctor")
        *doctor_info, = filter(lambda x: x["code"] == doctor, doctor_info)
        doctor_id = doctor_info[0]["doctor_id"]

        appointment_list = list()

        appointment_info = get_table("appointment")
        *appointment_info, = filter(lambda x: x["doctor_id"] == doctor_id, appointment_info)
        for elem in appointment_info:
            appointment_list.append(elem["appointment_id"])

        return appointment_list

    def search_for_disease():
        desease_info = get_table("desease")
        *desease_info, = filter(lambda x: x["desease_name"] == disease, desease_info)
        desease_id = desease_info[0]["desease_id"]

        appointment_list = list()

        appointment_info = get_table("appointment")
        *appointment_info, = filter(lambda x: x["desease_id"] == desease_id, appointment_info)
        for elem in appointment_info:
            appointment_list.append(elem["appointment_id"])

        return appointment_list

    if disease and doctor:
        appointment_id_doctor = search_for_doctor()
        appointment_id_disease = search_for_disease()
        appointment_id = list(set(appointment_id_doctor) & set(appointment_id_disease))

    elif disease:
        appointment_id = search_for_disease()

    elif doctor:
        appointment_id = search_for_doctor()

    else:
        return

    appointment = get_table("appointment")
    reception_w.comboBox.clear()
    reception_w.comboBox.addItem("")
    for elem in appointment:
        if elem["appointment_id"] in appointment_id:
            reception_w.comboBox.addItem(str(elem["appointment_id"]))


# COMBOBOX

def reception__box(text):
    KEY_WORD_DICT["reception"] = int(text)
    if KEY_WORD_DICT["reception"]:

        reception_info = get_table("appointment")
        *reception_info, = filter(lambda x: x["appointment_id"] == KEY_WORD_DICT["reception"], reception_info)
        treatment_plan_id = reception_info[0]["treatment_plan_id"]
        appointment_date = reception_info[0]["appointment_date"]
        doctor_id = reception_info[0]["doctor_id"]
        desease_id = reception_info[0]["desease_id"]
        polis = reception_info[0]["polis"]

        doctor_info = get_table("doctor")
        *doctor_info, = filter(lambda x: x["doctor_id"] == doctor_id, doctor_info)
        doctor_name = doctor_info[0]["doctor_name"]
        grade = doctor_info[0]["grade"]

        treatment_info = get_table("treatment_plan")
        *treatment_info, = filter(lambda x: x["treatment_plan_id"] == treatment_plan_id, treatment_info)
        title = treatment_info[0]["title"]
        treatment_description = treatment_info[0]["treatment_description"]

        patient_info = get_table("patient")
        *patient_info, = filter(lambda x: x["polis"] == polis, patient_info)
        date_birth = patient_info[0]["date_birth"]
        patient_name = patient_info[0]["patient_name"]
        reg_address = patient_info[0]["reg_address"]

        desease_info = get_table("desease")
        *desease_info, = filter(lambda x: x["desease_id"] == desease_id, desease_info)
        desease_name = desease_info[0]["desease_name"]
        symptoms = desease_info[0]["symptoms"]
        desease_description = desease_info[0]["desease_description"]

        text = f"Запись номер: {text}\n\nДата: {appointment_date}\nВрач: {doctor_name}\n" \
               f"Стаж: {grade}\n\nБольной: {patient_name}\nПолис: {polis}\n" \
               f"Дата рождения: {date_birth}\nМесто регистрации: {reg_address}\n\n" \
               f"Болезнь: {desease_name}\nСимптомы: {symptoms}\n" \
               f"Описание болезни: {desease_description}\n\nЛечение: {title}\n" \
               f"Описание лечения: {treatment_description}"

        reception_w.textBrowser.setText(text)


def add_reception__treatment_box(text):
    KEY_WORD_DICT["reception__treatment"] = text


def add_reception__disease_box(text):
    KEY_WORD_DICT["reception__disease"] = text


def add_reception__patient_box(text):
    KEY_WORD_DICT["reception__patient"] = text


def add_reception__doctor_box(text):
    KEY_WORD_DICT["reception__doctor"] = text


def patient__box(text):
    KEY_WORD_DICT["patient"] = text
    if KEY_WORD_DICT["patient"]:

        patient_info = get_table("patient")
        *patient_info, = filter(lambda x: x["polis"] == text, patient_info)
        patient_name = patient_info[0]["patient_name"]
        date_birth = patient_info[0]["date_birth"]
        reg_address = patient_info[0]["reg_address"]

        text = f"Пациент: {patient_name}\n\nДата рождения: {date_birth}\nАдрес: {reg_address}\n\n"

        patient_w.textBrowser.setText(text)


def treatment__box(text):

    KEY_WORD_DICT["treatment"] = text
    if KEY_WORD_DICT["treatment"]:
        treatment_info = get_table("treatment_plan")
        *treatment_info, = filter(lambda x: x["title"] == text, treatment_info)
        medecin_id = treatment_info[0]["medecin_id"]
        treatment_description = treatment_info[0]["treatment_description"]

        medecin_info = get_table("medecin")
        *medecin_info, = filter(lambda x: x["medecin_id"] == medecin_id, medecin_info)
        title = medecin_info[0]["title"]
        medecin_description = medecin_info[0]["medecin_description"]
        medecin_recipe = medecin_info[0]["medecin_recipe"]

        text = f"Лечение: {text}\n\nОписание: {treatment_description}\n\n" \
               f"Лекарство: {title}\nОписание лекарства: {medecin_description}" \
               f"\nИнструкция: {medecin_recipe}"

        treatment_w.textBrowser.setText(text)


def add_treatment__medicine_box(text):
    KEY_WORD_DICT["treatment__medicine"] = text


def search_doctor(text):
    if text:
        KEY_WORD_DICT["search_doctor"] = text


def search_disease(text):
    if text:
        KEY_WORD_DICT["search_disease"] = text


app = QtWidgets.QApplication(sys.argv)


reception_window = QtWidgets.QMainWindow()
reception_w = Ui_reception_window()
reception_w.setupUi(reception_window)
reception_w.pushButton.clicked.connect(delete_reception)
reception_w.pushButton_2.clicked.connect(reception__add_reception)
reception_w.pushButton_3.clicked.connect(reception__patient)
reception_w.pushButton_4.clicked.connect(reception__treatment)
reception_w.pushButton_5.clicked.connect(search)
reception_w.pushButton_6.clicked.connect(reception_to_update)
reception_w.comboBox.activated[str].connect(reception__box)
reception_w.comboBox_2.activated[str].connect(search_doctor)
reception_w.comboBox_3.activated[str].connect(search_disease)

start()

add_reception_window = QtWidgets.QDialog()
add_reception_w = Ui_Dialog()
add_reception_w.setupUi(add_reception_window)
add_reception_w.pushButton_3.clicked.connect(add_reception__reception__cancel)
add_reception_w.pushButton_2.clicked.connect(add_reception__reception)
add_reception_w.comboBox.activated[str].connect(add_reception__treatment_box)
add_reception_w.comboBox_2.activated[str].connect(add_reception__disease_box)
add_reception_w.comboBox_3.activated[str].connect(add_reception__patient_box)
add_reception_w.comboBox_4.activated[str].connect(add_reception__doctor_box)
# add_reception_w.comboBox_5.activated[str].connect(add_timetable__group_box)

patient_window = QtWidgets.QDialog()
patient_w = Ui_patient()
patient_w.setupUi(patient_window)
patient_w.pushButton.clicked.connect(delete_patient)
patient_w.pushButton_2.clicked.connect(patient__add_patient)
patient_w.pushButton_3.clicked.connect(patient__reception)
patient_w.pushButton_4.clicked.connect(patient__treatment)
patient_w.pushButton_6.clicked.connect(patient_to_update)
patient_w.comboBox.activated[str].connect(patient__box)

add_patient_window = QtWidgets.QDialog()
add_patient_w = Ui_add_patient_window()
add_patient_w.setupUi(add_patient_window)
add_patient_w.pushButton_3.clicked.connect(add_patient__patient__cancel)
add_patient_w.pushButton_2.clicked.connect(add_patient__patient)


treatment_window = QtWidgets.QDialog()
treatment_w = Ui_treatment_window()
treatment_w.setupUi(treatment_window)
treatment_w.pushButton.clicked.connect(delete_treatment)
treatment_w.pushButton_2.clicked.connect(treatment__add_treatment)
treatment_w.pushButton_3.clicked.connect(treatment__reception)
treatment_w.pushButton_4.clicked.connect(treatment__patient)
treatment_w.pushButton_6.clicked.connect(treatment_to_update)
treatment_w.comboBox.activated[str].connect(treatment__box)

add_treatment_window = QtWidgets.QDialog()
add_treatment_w = Ui_add_treatment_window()
add_treatment_w.setupUi(add_treatment_window)
add_treatment_w.pushButton_3.clicked.connect(add_treatment__treatment__cancel)
add_treatment_w.pushButton_2.clicked.connect(add_treatment__treatment)
add_treatment_w.comboBox.activated[str].connect(add_treatment__medicine_box)


update_reception_window = QtWidgets.QDialog()
update_reception_w = Ui_update_reception()
update_reception_w.setupUi(update_reception_window)
update_reception_w.pushButton_3.clicked.connect(reception_from_update_cancel)
update_reception_w.pushButton_2.clicked.connect(reception_from_update)
update_reception_w.comboBox.activated[str].connect(add_reception__treatment_box)
update_reception_w.comboBox_2.activated[str].connect(add_reception__disease_box)
update_reception_w.comboBox_3.activated[str].connect(add_reception__patient_box)
update_reception_w.comboBox_4.activated[str].connect(add_reception__doctor_box)

update_patient_window = QtWidgets.QDialog()
update_patient_w = Ui_update_patient_window()
update_patient_w.setupUi(update_patient_window)
update_patient_w.pushButton_3.clicked.connect(patient_from_update_cancel)
update_patient_w.pushButton_2.clicked.connect(patient_from_update)

update_treatment_window = QtWidgets.QDialog()
update_treatment_w = Ui_update_treatment_window()
update_treatment_w.setupUi(update_treatment_window)
update_treatment_w.pushButton_3.clicked.connect(treatment_from_update_cancel)
update_treatment_w.pushButton_2.clicked.connect(treatment_from_update)
update_treatment_w.comboBox.activated[str].connect(add_treatment__medicine_box)

sys.exit(app.exec_())
