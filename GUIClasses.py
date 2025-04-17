import json
from json import JSONDecodeError

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QDialog, QMessageBox
from PyQt6.QtCore import QDate
from matplotlib.figure import Figure

from MainWindow import Ui_MainWindow
from ui_widget_addcourse import Ui_AddCourse
from ui_widget_addgrade import Ui_AddGrade
from ui_widget_addsemester import Ui_AddSemester
from ui_widget_adduserdata import Ui_NewUserData
from DashboardClasses import charts, uni_data, student_data, semester_data, course_of_study_data
from DataManagingClasses import menu_data, exam_data, study_data, user_data
from datetime import date

#Course Status Pie-Chart
courses_in_progress = len(study_data.load().get("Courses", []))
all_data = exam_data.load()
courses_done = len([key for key, value in all_data.items() if "Passed" in value])
courses_open = (
        menu_data.load().get("Angewandte Künstliche Intelligenz", 99).get("courses_amount")
        -
        (courses_done + courses_in_progress)
)

pie_chart_course_status = charts("pie", pie_chart_values=[courses_done,courses_in_progress,courses_open])
pie_chart_course_status.fig.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.01)

#Größer AVG-Grade Line-Chart
line_chart_avg_grade_big = charts(
    "line",
    course_of_study_data.all_grades,
    average_grade=course_of_study_data.get_average_grade(exam_data),
    avg_grade_line=True
)
line_chart_avg_grade_big.fig.subplots_adjust(left=0.06, right=0.99, top=0.95, bottom=0.05)


#Kleiner AVG-Grade Line-Chart
line_chart_avg_grade_small = charts("line", course_of_study_data.all_grades)
#line_chart_avg_grade_small.fig = Figure(figsize=(0.1, 0.05), dpi=100)
line_chart_avg_grade_small.set_opacity(0.3)
line_chart_avg_grade_small.fig.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)

#Remaining Weeks Pie Chart
remaining_weeks_pie_chart = charts("pie70", remaining_weeks_semester=semester_data.get_passed_weeks())
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
        self.exam_data.update(
            self.comboBox_Modul.currentText(),
            [self.comboBox_Passed.currentText(),self.lineEdit_Grade.text()]
        )
        self.accept()

    def load_data(self):
        # Verfügbare eingeschriebene Kurse extrahieren (Die zuvor per Add Course hinzugefügt wurden)
        assigned_courses = study_data.load().get("Courses", [])
        loaded_exam_data = exam_data.load()
        passed_courses = [key for key, value in loaded_exam_data.items() if value[0] == "Passed"]
        available_courses = [course for course in assigned_courses if course not in passed_courses]

        self.comboBox_Modul.addItems(available_courses)


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
                course_data = all_data.get("Angewandte Künstliche Intelligenz", {})
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
                course_data = all_data.get("Angewandte Künstliche Intelligenz", {})
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
        data_for_menu = self.menu_data.load()
        universities = data_for_menu.get("universities", [])
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
        self.overlay_label = QtWidgets.QLabel(
            str(course_of_study_data.get_average_grade(exam_data)),
            parent=self.frame_avg_grades_chart_small)
        self.overlay_label.setStyleSheet("""
            font: 700 60pt \"Graduate\";\n
            color: rgba(49, 149, 43, 1);
            background-color: rgba(49, 149, 43, 0);
            """)
        self.overlay_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.overlay_label.resize(self.frame_avg_grades_chart_small.size())
        self.overlay_label.setAutoFillBackground(False)
        self.overlay_label.raise_()
        self.overlay_label.setGeometry(self.frame_avg_grades_chart_small.rect())

        self.frame_avg_grades_chart_small.resizeEvent = self.update_overlay_size

        #PushButtons Verknüpfung zu Dialogs
        self.pushButton_add_course.clicked.connect(self.open_add_course_dialog)
        self.pushButton_add_grade.clicked.connect(self.open_add_grade_dialog)
        self.pushButton_add_semester.clicked.connect(self.open_add_semester_dialog)
        self.pushButton_add_user_data.clicked.connect(self.open_add_user_data_dialog)

        #Lade User Data Studenname, Studentnummer in GUI
        self.label_input_student_name.setText(student_data.name)
        self.label_input_student_number.setText(student_data.student_number)

        #Lade User Data Universtitätsadresse in GUI
        self.label_university_name.setText(uni_data.name)
        self.label_university_street.setText(uni_data.street)
        self.label_university_address.setText(uni_data.town)

        #Lade aktuelles Semester in GUI
        self.label_semester_number_bottom_left.setText(semester_data.semester_number)

        #Lade Courses Completed Daten in GUI
        completed_exams = []
        all_data = self.exam_data.load()
        for key in all_data:
            if "Passed" in all_data.get(key):
                completed_exams.append(key)

        self.label_courses_completet_number_bottom_mid.setText(str(len(completed_exams)))

        #Lade Courses Open Daten in GUI
        open_courses = self.menu_data.load().get("Angewandte Künstliche Intelligenz", 99).get("courses_amount") - len(completed_exams)
        self.label_courses_open_number_bottom_right.setText(str(open_courses))

        #Lade Passed Weeks und Remaining Weeks in GUI (Label Top Right)
        self.label_semester_counter_number_right.setText(str(semester_data.get_remaining_weeks()))
        self.label_semester_counter_number_left.setText(str(semester_data.get_passed_weeks()))

    #Resizing Methode für Overlay-Widget AVG-Grade links oben
    def update_overlay_size(self, event):
        self.overlay_label.setGeometry(self.frame_avg_grades_chart_small.rect())
        event.accept()

    #Funktionen zum öffnen und arbeiten mit den Dialogs
    def open_add_grade_dialog(self):
        dialog = AddGradeDialog(self.study_data, self.exam_data)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            self.refresh_ui(grade_dialog=True)
    def open_add_course_dialog(self):
        dialog = AddCourseDialog(self.study_data)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            self.refresh_ui(course_dialog=True)
    def open_add_semester_dialog(self):
        dialog = AddSemesterDialog(self.study_data)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            self.refresh_ui(semester_dialog=True)
    def open_add_user_data_dialog(self):
        dialog = AddUserDataDialog(self.user_data, self.menu_data)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            self.refresh_ui(user_dialog=True)

    def refresh_ui(self, grade_dialog=False, course_dialog=False, semester_dialog=False, user_dialog=False):

        if grade_dialog == True:
            #Update Courses Completed
            new_completed_exams = []
            new_data = self.exam_data.load()
            for key in new_data:
                if "Passed" in new_data.get(key):
                    new_completed_exams.append(key)

            self.label_courses_completet_number_bottom_mid.setText(str(len(new_completed_exams)))

            #Update Courses Open
            new_open_courses = (self.menu_data.load().get(
                "Angewandte Künstliche Intelligenz", 99).get("courses_amount") - len(new_completed_exams)
                                )
            self.label_courses_open_number_bottom_right.setText(str(new_open_courses))

            #Update AVG-Grade Charts
            #Großer AVG-Grade Line-Chart
            line_chart_avg_grade_big.update_charts(
                y_values=course_of_study_data.all_grades,
                average_grade=course_of_study_data.get_average_grade(exam_data),
                avg_grade_line=True
            )

            #Kleiner AVG-Grade Line-Chart
            line_chart_avg_grade_small.update_charts(y_values=course_of_study_data.all_grades)

            #Update AVG-Grade Anzeige links oben
            self.overlay_label.setText(str(course_of_study_data.get_average_grade(exam_data)))

        if course_dialog == True:
            #Update Pie-Chart Course Status
            new_courses_in_progress = len(self.study_data.load().get("Courses", []))
            new_data = self.exam_data.load()
            new_courses_done = len([key for key, value in new_data.items() if "Passed" in value])
            new_courses_open = (
                    self.menu_data.load().get("Angewandte Künstliche Intelligenz", {}).get("courses_amount")
                    -
                    (new_courses_done + new_courses_in_progress)
            )

            pie_chart_course_status.update_charts(pie_chart_values=[new_courses_done, new_courses_in_progress, new_courses_open])


        if semester_dialog == True:
            updated_study_data = self.study_data.load()
            #Update aktuelles Semester in GUI
            self.label_semester_number_bottom_left.setText(updated_study_data.get("Semester", ""))
            #Update Remaining Weeks Pie Chart
            new_start_date_string = self.study_data.load().get("Start Date", str(date.today()))
            new_start_date = date.fromisoformat(new_start_date_string)
            today = date.today()

            delta = today - new_start_date  #
            new_remaining_weeks = delta.days / 7
            # Begrenzen auf maximale Semesterlänge, um Error-Code bei pie70 Chart erstellung zu verhindern
            if new_remaining_weeks > 26:
                new_remaining_weeks = 26
            new_passed_weeks = 26 - new_remaining_weeks
            remaining_weeks_pie_chart.update_charts(remaining_weeks_semester=new_passed_weeks)

            new_rounded_remaining_weeks = int(round(new_remaining_weeks, 0))
            new_rounded_passed_weeks = int(round(new_passed_weeks, 0))
            self.label_semester_counter_number_right.setText(str(new_rounded_remaining_weeks))
            self.label_semester_counter_number_left.setText(str(new_rounded_passed_weeks))

        if user_dialog == True:
            updated_user_data = self.user_data.load()
            #Update User Data Studenname, Studentnummer in GUI
            self.label_input_student_name.setText(updated_user_data.get("Student Name", ""))
            self.label_input_student_number.setText(updated_user_data.get("Student Number", ""))

            #Update User Data Universtitätsadresse in GUI
            university_data = updated_user_data.get("University", ["name", "street", "town"])
            self.label_university_name.setText(university_data[0])
            self.label_university_street.setText(university_data[1])
            self.label_university_address.setText(university_data[2])








