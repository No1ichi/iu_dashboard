import json
from json import JSONDecodeError

import debugpy.server.cli
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QDialog, QMessageBox
from PyQt6.QtCore import QDate
from matplotlib.figure import Figure

from MainWindow import Ui_MainWindow
from ui_widget_addcourse import Ui_AddCourse
from ui_widget_addgrade import Ui_AddGrade
from ui_widget_addsemester import Ui_AddSemester
from ui_widget_adduserdata import Ui_NewUserData
from DashboardClasses import charts
from DataManagingClasses import menu_data, exam_data, study_data, user_data
from datetime import date

#Course Status Pie-Chart
courses_in_progress = len(study_data.load().get("Courses", []))
all_data = exam_data.load()
courses_done = len([key for key, value in all_data.items() if "Passed" in value])
courses_open = (
        menu_data.load().get("angewandte_kuenstliche_intelligenz", 99).get("courses_amount")
        -
        (courses_done + courses_in_progress)
)

pie_chart_course_status = charts("pie", pie_chart_values=[courses_done,courses_in_progress,courses_open])
pie_chart_course_status.fig.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.01)

#Größer AVG-Grade Line-Chart
all_grades = [float(value[1]) for value in all_data.values() if value[0] == "Passed"]
avg_grade = sum(all_grades) / (len(all_grades) if len(all_grades) > 0 else 1)
avg_grade = round(avg_grade, 2)
#Maximale Anzahl an Noten in all_grades zulassen? Letzten 10 Noten?
line_chart_avg_grade_big = charts("line", all_grades, average_grade=avg_grade, avg_grade_line=True)
line_chart_avg_grade_big.fig.subplots_adjust(left=0.06, right=0.99, top=0.95, bottom=0.05)


#Kleiner AVG-Grade Line-Chart
line_chart_avg_grade_small = charts("line", all_grades)
#line_chart_avg_grade_small.fig = Figure(figsize=(0.1, 0.05), dpi=100)
line_chart_avg_grade_small.set_opacity(0.3)
line_chart_avg_grade_small.fig.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)

#Remaining Weeks Pie Chart
start_date_string = study_data.load().get("Start Date", "2000-01-01")
start_date = date.fromisoformat(start_date_string)
today = date.today()

delta = today - start_date#
remaining_weeks = delta.days / 7
#Begrenzen auf maximale Semesterlänge, um Error-Code bei pie70 Chart erstellung zu verhindern
if remaining_weeks > 26:
    remaining_weeks = 26
passed_weeks = 26 - remaining_weeks

remaining_weeks_pie_chart = charts("pie70", remaining_weeks_semester=passed_weeks)
remaining_weeks_pie_chart.fig.subplots_adjust(left=0.001, right=0.999, top=0.999, bottom=0.001)

#Dialogklasse Add Grade
class AddGradeDialog(QDialog, Ui_AddGrade):
    def __init__(self, study_data, exam_data):
        super().__init__()
        self.setupUi(self)
        self.load_data()
        self.study_data = study_data
        self.exam_data = exam_data

        self.comboBox_Passed.addItems(["Passed", "Failed"])

        self.buttonBox.accepted.connect(self.save_data)
        self.buttonBox.rejected.connect(self.reject)

    def save_data(self):
        self.exam_data.update(self.comboBox_Modul.currentText(), [self.comboBox_Passed.currentText(), self.lineEdit_Grade.text()])
        self.accept()

    def load_data(self):
        try:
            with open("studydata.json", "r") as file:
                all_data = json.load(file)

                #Verfügbare eingeschriebene Kurse extrahieren (Die zuvor per Add Course hinzugefügt wurden)
                assigned_courses = all_data.get("Courses", [])
                course_list = [course for course in assigned_courses]

                self.comboBox_Modul.addItems(course_list)

        except FileNotFoundError:
            ErrorMessage(self, "File not Fount")
        except json.JSONDecodeError:
            ErrorMessage(self, "File-Decoding Error")


#Dialogklasse Add Course
class AddCourseDialog(QDialog, Ui_AddCourse):
    def __init__(self, study_data):
        super().__init__()
        self.setupUi(self)
        self.load_data()
        self.study_data = study_data

        self.buttonBox.accepted.connect(self.save_data)
        self.buttonBox.rejected.connect(self.reject)

    def save_data(self):
        try:
            with open("studydata.json", "r") as file:
                all_data = json.load(file)
                course_list = all_data.get("Courses", [])
                course_list.append(self.comboBox_CourseName.currentText())

            self.study_data.update("Courses", course_list)
            self.study_data.update("ECTS-Points_"+self.comboBox_CourseName.currentText(), self.lineEdit_ECTSPoints.text())
            self.study_data.update("Exam-Type_"+self.comboBox_CourseName.currentText(), self.comboBox_ExamType.currentText())

            self.accept()

        except FileNotFoundError:
            ErrorMessage(self, "File not found")
        except json.JSONDecodeError:
            ErrorMessage(self, "File decoding error")

    def load_data(self):
        try:
            with open("menu_data.json", "r") as file:
                all_data = json.load(file)

                #Verfügbare Kurse extrahieren
                course_data = all_data.get("angewandte_kuenstliche_intelligenz", [])
                available_courses = course_data.get("courses", [])
                course_list = [course for course in available_courses]

                #Prüfungsarten extrahieren
                available_exam_types = course_data.get("exam_type", [])
                exam_type_list = [examtype for examtype in available_exam_types]

                self.comboBox_CourseName.addItems(course_list)
                self.comboBox_ExamType.addItems(exam_type_list)

        except FileNotFoundError:
            ErrorMessage(self, "File not Fount")
        except json.JSONDecodeError:
            ErrorMessage(self, "File-Decoding Error")

#Dialogklasse Add Semester
class AddSemesterDialog(QDialog, Ui_AddSemester):
    def __init__(self, study_data):
        super().__init__()
        self.setupUi(self)
        self.load_data()
        self.study_data = study_data

        self.buttonBox.accepted.connect(self.save_data)
        self.buttonBox.rejected.connect(self.reject)

    def save_data(self):
        self.study_data.update("Semester", self.comboBox_SemesterNumber.currentText())
        self.study_data.update("Start Date", self.dateEdit_StartDate.date().toString("yyyy-MM-dd"))
        self.accept()

    def load_data(self):
        try:
            with open("menu_data.json", "r") as file:
                all_data = json.load(file)

                #Semesteranzahl extrahieren
                course_data = all_data.get("angewandte_kuenstliche_intelligenz", [])
                total_semester = course_data.get("semester", 0)
                semesters_list = [str(nr) for nr in range(1, total_semester+1)]

                self.comboBox_SemesterNumber.addItems(semesters_list)

        except FileNotFoundError:
            ErrorMessage(self, "File not Fount")
        except json.JSONDecodeError:
            ErrorMessage(self, "File-Decoding Error")

#Dialogklasse Add User Data
class AddUserDataDialog(QDialog, Ui_NewUserData):
    def __init__(self, user_data, menu_data):
        super().__init__()
        self.setupUi(self)
        self.load_data()
        self.user_data = user_data
        self.menu_data = menu_data

        self.buttonBox.accepted.connect(self.save_data)
        self.buttonBox.rejected.connect(self.reject)

    def save_data(self):
        selected_university_name = self.comboBox_University.currentText()
        data = self.menu_data.load()
        universities = data.get("universities", [])
        selected_university_list = None

        for entry in universities:
            university = entry.get("university", [])
            if university and university[0] == selected_university_name:
                selected_university_list = university
                break

        if selected_university_list:
            self.user_data.update("University", selected_university_list)
        else:
            ErrorMessage(self, "Universität wurde nicht gefunden.")
            return

        #self.user_data.update("Universiti", self.comboBox_University.currentText()),
        self.user_data.update("Student Name", self.lineEdit_StudentName.text()),
        self.user_data.update("Student Number", self.lineEdit_StudentNumber.text()),
        self.user_data.update("Course of Study", self.comboBox_CourseOfStudy.currentText())
        self.accept()


    def load_data(self):
        try:
            with open("menu_data.json", "r") as file:
                all_data = json.load(file)

                #Universitätennamen extrahieren
                university_data = all_data.get("universities", [])
                universities = [name["university"] for name in university_data]
                university_names = [uni[0] for uni in universities]
                #Angebotene Kurse extrahieren
                courses = all_data.get("course_of_studies", [])

                self.comboBox_University.addItems(university_names)
                self.comboBox_CourseOfStudy.addItems(courses)

        except FileNotFoundError:
            ErrorMessage(self, "File not Fount")
        except json.JSONDecodeError:
            ErrorMessage(self, "File-Decoding Error")



class ErrorMessage():
    def __init__(self, parent, warning):
        self.warning = warning
        self.show_error(parent)
    def show_error(self, parent):
        QMessageBox.critical(
            parent,
            "Fehler",
            self.warning,
            QMessageBox.StandardButton.Ok,
            )


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, user_data, study_data, exam_data, menu_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.user_data = user_data
        self.study_data = study_data
        self.exam_data = exam_data
        self.menu_data = menu_data

        #Layout für MPL-Insert AVG-Grades Line Chart Big
        layout = QtWidgets.QVBoxLayout(self.frame_avg_grades_chart_big)
        self.frame_avg_grades_chart_big.setLayout(layout)
        #Einbetten von MPL-Widget in frame_avg_grades_chart_big
        layout.addWidget(line_chart_avg_grade_big)

        #Layout für MPL-Insert Course Status Pie Chart
        layout = QtWidgets.QVBoxLayout(self.frame_pie_chart)
        self.frame_pie_chart.setLayout(layout)
        #Einbetten von MPL-Widget in frame_pie_chart
        layout.addWidget(pie_chart_course_status)

        #Layout für MPL-Insert Weeks Left Pie-Chart
        layout = QtWidgets.QVBoxLayout(self.frame_3)
        self.frame_3.setLayout(layout)
        #Einbetten von MPL-Widget in frame_3
        layout.addWidget(remaining_weeks_pie_chart)

        #Layout für MPL-Insert AVG-Grades Line Chart Small
        layout = QtWidgets.QVBoxLayout(self.frame_avg_grades_chart_small)
        self.frame_avg_grades_chart_small.setLayout(layout)
        #Einbetten von MPL-Widget in frame_3
        layout.addWidget(line_chart_avg_grade_small)

        #Überlagerndes QLabel für Durchschnittsnote über AVG Grade Chart Small
        #Lade AVG-Grade in GUI
        overlay_label = QtWidgets.QLabel(str(avg_grade), parent=self.frame_avg_grades_chart_small)
        overlay_label.setStyleSheet("""
            font: 700 60pt \"Graduate\";\n
            color: rgba(49, 149, 43, 1);
            background-color: rgba(49, 149, 43, 0);
            """)
        overlay_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        overlay_label.resize(self.frame_avg_grades_chart_small.size())
        overlay_label.setAutoFillBackground(False)
        overlay_label.raise_()
        overlay_label.setGeometry(self.frame_avg_grades_chart_small.rect())
        def update_overlay_size(event):
            overlay_label.setGeometry(self.frame_avg_grades_chart_small.rect())
            event.accept()
        self.frame_avg_grades_chart_small.resizeEvent = update_overlay_size

        #PushButtons Verknüpfung zu Dialogs
        self.pushButton_add_course.clicked.connect(self.open_add_course_dialog)
        self.pushButton_add_grade.clicked.connect(self.open_add_grade_dialog)
        self.pushButton_add_semester.clicked.connect(self.open_add_semester_dialog)
        self.pushButton_add_user_data.clicked.connect(self.open_add_user_data_dialog)

        #Lade User Data Studenname, Studentnummer in GUI
        self.label_input_student_name.setText(user_data.load().get("Student Name", ""))
        self.label_input_student_number.setText(user_data.load().get("Student Number", ""))

        #Lade User Data Universtitätsadresse in GUI
        university_data = user_data.load().get("University", ["name", "street", "town"])
        self.label_university_name.setText(university_data[0])
        self.label_university_street.setText(university_data[1])
        self.label_university_address.setText(university_data[2])

        #Lade aktuelles Semester in GUI
        self.label_semester_number_bottom_left.setText(study_data.load().get("Semester", ""))

        #Lade Courses Completed Daten in GUI
        completed_exams = []
        all_data = self.exam_data.load()
        for key in all_data:
            if "Passed" in all_data.get(key):
                completed_exams.append(key)

        self.label_courses_completet_number_bottom_mid.setText(str(len(completed_exams)))

        #Lade Courses Open Daten in GUI
        open_courses = self.menu_data.load().get("angewandte_kuenstliche_intelligenz", 99).get("courses_amount") - len(completed_exams)
        self.label_courses_open_number_bottom_right.setText(str(open_courses))

        #Lade Passed Weeks und Remaining Weeks in GUI (Label Top Right)
        rounded_remaining_weeks = int(round(remaining_weeks, 0))
        rounded_passed_weeks = int(round(passed_weeks, 0))
        self.label_semester_counter_number_right.setText(str(rounded_remaining_weeks))
        self.label_semester_counter_number_left.setText(str(rounded_passed_weeks))

    #Funktionen zum öffnen und arbeiten mit den Dialogs
    def open_add_grade_dialog(self):
        dialog = AddGradeDialog(self.study_data, self.exam_data)
        result = dialog.exec()
    def open_add_course_dialog(self):
        dialog = AddCourseDialog(self.study_data)
        result = dialog.exec()
    def open_add_semester_dialog(self):
        dialog = AddSemesterDialog(self.study_data)
        result = dialog.exec()
    def open_add_user_data_dialog(self):
        dialog = AddUserDataDialog(self.user_data, self.menu_data)
        result = dialog.exec()






