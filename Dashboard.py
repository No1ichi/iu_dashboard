import sys
import os
import json
from PyQt6.QtWidgets import QApplication
from GUIClasses import MainWindow, AddUserDataDialog, AddSemesterDialog, AddCourseDialog, AddGradeDialog
from DataManagingClasses import user_data, exam_data, study_data,  menu_data

#Öffne JSON-File study_data und legt leere Kurs-Liste an, falls sie noch nicht vorhanden ist.
#Kurs-Liste speichert hinzugefügte Kurse mit ECTS-Punkten und Exam-Typ ab
if os.path.exists("studydata.json"):
    try:
        with open("studydata.json", "r") as file:
            all_data = json.load(file)
    except json.JSONDecodeError:
        all_data = {}
else:
    all_data = {}

if "Courses" not in all_data:
    study_data.update("Courses", [])
else:
    pass

dialog_user_data = AddUserDataDialog(user_data, menu_data)
dialog_add_semester = AddSemesterDialog(study_data)
dialog_add_course = AddCourseDialog(study_data)
dialog_add_grade = AddGradeDialog(study_data, exam_data)


app = QApplication(sys.argv)
window = MainWindow(user_data, study_data, exam_data, menu_data)
window.show()
app.exec()
