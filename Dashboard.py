import sys
import os
import json
from PyQt6.QtWidgets import QApplication
from GUIClasses import MainWindow, AddUserDataDialog, AddSemesterDialog, AddCourseDialog, AddGradeDialog
from DataManagingClasses import user_data, exam_data, study_data, menu_data

#Öffne JSON-File study_data und legt leere Kurs-Liste an, falls sie noch nicht vorhanden ist.
#Kurs-Liste speichert hinzugefügte Kurse mit ECTS-Punkten und Exam-Typ ab
def initialize_defaults():
    # Initialisiere Default-Werte für studydata JSON-File
    if os.path.exists("data/studydata.json"):
        study_data_file = study_data.load()
        if "Courses" not in study_data_file:
            study_data.update("Courses", [])
        if "Semester" not in study_data_file:
            study_data.update("Semester", "1")
        if "Start Date" not in study_data_file:
            study_data.update("Start Date", "2024-01-01")
        else:
            pass
    # Initialisiere Default-Werte für userdata JSON-File
    if os.path.exists("data/userdata.json"):
        user_data_file = user_data.load()
        if "University" not in user_data_file:
            user_data.update("University", ["Name", "Street", "Town"])
        if "Student Name" not in user_data_file:
            user_data.update("Student Name", "")
        if "Student Number" not in user_data_file:
            user_data.update("Student Number", "")
        if "Course of Study" not in user_data_file:
            user_data.update("Course of Study", "")
        else:
            pass
    # Initialisiere Default-Werte für examdata JSON-File
    if os.path.exists("data/examdata.json"):
        exam_data_file = exam_data.load()
        if exam_data_file == {}:
            exam_data.update("", ["Status", 0])
        else:
            pass


initialize_defaults()


dialog_user_data = AddUserDataDialog(user_data, menu_data)
dialog_add_semester = AddSemesterDialog(study_data)
dialog_add_course = AddCourseDialog(study_data)
dialog_add_grade = AddGradeDialog(study_data, exam_data)


app = QApplication(sys.argv)
window = MainWindow(user_data, study_data, exam_data, menu_data)
window.show()
app.exec()
