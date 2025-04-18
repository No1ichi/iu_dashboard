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
from DashboardClasses import charts, uni_data, student_data, semester_data, course_of_study_data, course_data
from DataManagingClasses import menu_data, exam_data, study_data, user_data
from datetime import date

# Course Status Pie-Chart
course_data.update_data(study_data, exam_data, user_data)
amt_courses_done = len(course_data.get_courses_finished())
amt_courses_open = len(course_data.get_courses_in_progress())
amt_all_courses = len(course_data.get_all_courses(course_of_study_data.name)) - (amt_courses_open + amt_courses_done)

pie_chart_course_status = charts("pie", pie_chart_values=[
    amt_courses_done,amt_courses_open,amt_all_courses])
pie_chart_course_status.fig.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.01)

# Großer AVG-Grade Line-Chart
line_chart_avg_grade_big = charts(
    "line",
    course_of_study_data.all_grades,
    average_grade=course_of_study_data.get_average_grade(exam_data),
    avg_grade_line=True
)
line_chart_avg_grade_big.fig.subplots_adjust(left=0.06, right=0.99, top=0.95, bottom=0.05)


# Kleiner AVG-Grade Line-Chart
line_chart_avg_grade_small = charts("line", course_of_study_data.all_grades)
line_chart_avg_grade_small.set_opacity(0.3)
line_chart_avg_grade_small.fig.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)

#Remaining Weeks Pie Chart
remaining_weeks_pie_chart = charts("pie70", remaining_weeks_semester=semester_data.get_remaining_weeks())
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


# Dialogklasse Add Course
class AddCourseDialog(QDialog, Ui_AddCourse):
    def __init__(self, study_data):
        super().__init__()
        self.setupUi(self)
        self.load_data()
        self.study_data = study_data

        self.buttonBox.accepted.connect(self.save_data)
        self.buttonBox.rejected.connect(self.reject)

    def save_data(self):
        course_list = study_data.load().get("Courses", [])
        if self.comboBox_CourseName.currentText() not in course_list:
            course_list.append(self.comboBox_CourseName.currentText())
            self.study_data.update("Courses", course_list)
            self.study_data.update("ECTS-Points_" + self.comboBox_CourseName.currentText(),
                                   self.lineEdit_ECTSPoints.text())
            self.study_data.update("Exam-Type_" + self.comboBox_CourseName.currentText(),
                                   self.comboBox_ExamType.currentText())
        else:
            pass

        self.accept()


    def load_data(self):
        course_data.update_data(study_data, exam_data, user_data)
        # Alle Kurse des Studiengangs auslesen
        all_courses = course_data.get_all_courses(course_of_study_data.name)
        # Kurse aus Kurs-Liste herausfiltern, die abgeschlossen oder in bearbeitung sind
        filtered_courses = [
            course for course in all_courses
            if course not in course_data.get_courses_in_progress()
               and course not in course_data.get_courses_finished()
        ]
        # Prüfungsarten extrahieren
        exam_types = course_data.get_exam_types()

        self.comboBox_CourseName.addItems(filtered_courses)
        self.comboBox_ExamType.addItems(exam_types)


# Dialogklasse Add Semester
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
        all_data = menu_data.load()
        # Semesteranzahl extrahieren
        course_data = all_data.get("Angewandte Künstliche Intelligenz", {})
        total_semester = course_data.get("semester", 0)
        semesters_list = [str(nr) for nr in range(1, total_semester + 1)]

        self.comboBox_SemesterNumber.addItems(semesters_list)

# Dialogklasse Add User Data
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
            if entry[0] == selected_university_name:
                selected_university_list = entry
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
        main_data = menu_data.load()
        # Universitätsnamen extrahieren
        universities = main_data.get("universities", [])
        university_names = [uni[0] for uni in universities]
        # Angebotene Kurse extrahieren
        all_courses = course_data.get_all_courses(course_of_study_data.name)

        self.comboBox_University.addItems(university_names)
        self.comboBox_CourseOfStudy.addItems(all_courses)


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

        #Lade AVG-Grade Differenz in GUI
        self.label_grade_move_pos.setText(str(course_of_study_data.get_grade_difference()))
        self.label_grade_move_neg.setText(str(course_of_study_data.get_grade_difference()))

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
        self.label_courses_completet_number_bottom_mid.setText(str(len(course_data.get_courses_finished())))

        #Lade Courses Open Daten in GUI
        open_courses = (self.menu_data.load().get(course_of_study_data.name, 99).get("courses_amount")
                        - len(course_data.get_courses_finished()))
        self.label_courses_open_number_bottom_right.setText(str(open_courses))

        #Lade Passed Weeks und Remaining Weeks in GUI (Label Top Right)
        self.label_semester_counter_number_right.setText(str(semester_data.get_passed_weeks()))
        self.label_semester_counter_number_left.setText(str(semester_data.get_remaining_weeks()))

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
            course_data.update_data(study_data, exam_data, user_data)
            self.label_courses_completet_number_bottom_mid.setText(str(len(course_data.get_courses_finished())))

            #Update Courses Open
            new_open_courses = (self.menu_data.load().get(course_of_study_data.name, 99).get("courses_amount")
                            - len(course_data.get_courses_finished()))
            self.label_courses_open_number_bottom_right.setText(str(new_open_courses))

            # Update AVG-Grade Difference
            course_of_study_data.get_average_grade(exam_data)
            course_of_study_data.get_last_avg_grade(exam_data)
            self.label_grade_move_pos.setText(str(course_of_study_data.get_grade_difference()))
            self.label_grade_move_neg.setText(str(course_of_study_data.get_grade_difference()))

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
            (course_data.update_data(study_data, exam_data, user_data))
            new_amt_courses_done = len(course_data.get_courses_finished())
            new_amt_courses_open = len(course_data.get_courses_in_progress())
            new_amt_all_courses = len(course_data.get_all_courses(course_of_study_data.name)) - (amt_courses_open + amt_courses_done)

            pie_chart_course_status.update_charts(pie_chart_values=[
                new_amt_courses_done,
                new_amt_courses_open,
                new_amt_all_courses
            ])


        if semester_dialog == True:
            semester_data.update_data()
            # Update aktuelles Semester in GUI
            self.label_semester_number_bottom_left.setText(semester_data.semester_number)
            # Update Remaining Weeks Pie Chart
            remaining_weeks_pie_chart.update_charts(remaining_weeks_semester=semester_data.get_remaining_weeks())

            self.label_semester_counter_number_right.setText(str(semester_data.get_passed_weeks()))
            self.label_semester_counter_number_left.setText(str(semester_data.get_remaining_weeks()))

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



