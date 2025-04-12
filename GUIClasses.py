import json
from json import JSONDecodeError

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QDialog, QMessageBox
from matplotlib.figure import Figure

from MainWindow import Ui_MainWindow
from ui_widget_addcourse import Ui_AddCourse
from ui_widget_addgrade import Ui_AddGrade
from ui_widget_addsemester import Ui_AddSemester
from ui_widget_adduserdata import Ui_NewUserData
from DashboardClasses import charts

#Größer AVG-Grade Line-Chart - Daten sind nur zu Testzwecken
line_chart_avg_grade_big = charts("line", [1,2,2,1.4,5,1.3,2.3,4,2.3,3.3], average_grade=2.4, avg_grade_line=True)
line_chart_avg_grade_big.fig.subplots_adjust(left=0.06, right=0.99, top=0.95, bottom=0.05)
#Course Status Pie-Chart - Daten sind nur zu Testzwecken
pie_chart_course_status = charts("pie", pie_chart_values=[5,5,40])
pie_chart_course_status.fig.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.01)
#Kleiner AVG-Grade Line-Chart - Daten sind nur zu Testzwecken
line_chart_avg_grade_small = charts("line", [1,2,2,1.4,5,1.3,2.3,4,2.3,3.3])
#line_chart_avg_grade_small.fig = Figure(figsize=(0.1, 0.05), dpi=100)
line_chart_avg_grade_small.set_opacity(0.3)
line_chart_avg_grade_small.fig.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)
#Remaining Weeks Pie Chart - Daten sind nur zu Testzwecken
remaining_weeks_pie_chart = charts("pie70", remaining_weeks_semester=22)
remaining_weeks_pie_chart.fig.subplots_adjust(left=0.001, right=0.999, top=0.999, bottom=0.001)

#Dialogklasse Add Grade
class AddGradeDialog(QDialog, Ui_AddGrade):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

#Dialogklasse Add Course
class AddCourseDialog(QDialog, Ui_AddCourse):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_data()

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
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_data()

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
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_data()

    def load_data(self):
        try:
            with open("menu_data.json", "r") as file:
                all_data = json.load(file)

                #Universitätennamen extrahieren
                university_data = all_data.get("universities", [])
                universities = [name["university_name"] for name in university_data]
                #Angebotene Kurse extrahieren
                courses = all_data.get("course_of_studies", [])

                self.comboBox_University.addItems(universities)
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

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
        overlay_label = QtWidgets.QLabel("1.5", parent=self.frame_avg_grades_chart_small)
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

    #Funktionen zum öffnen und arbeiten mit den Dialogs
    def open_add_course_dialog(self):
        dialog = AddCourseDialog()
        result = dialog.exec()
    def open_add_grade_dialog(self):
        dialog = AddGradeDialog()
        result = dialog.exec()
    def open_add_semester_dialog(self):
        dialog = AddSemesterDialog()
        result = dialog.exec()
    def open_add_user_data_dialog(self):
        dialog = AddUserDataDialog()
        result = dialog.exec()






