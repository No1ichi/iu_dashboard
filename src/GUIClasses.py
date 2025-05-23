from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QDialog, QMessageBox, QGraphicsOpacityEffect, QDialogButtonBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os
from ui.MainWindow import Ui_MainWindow
from ui.ui_widget_addcourse import Ui_AddCourse
from ui.ui_widget_addgrade import Ui_AddGrade
from ui.ui_widget_addsemester import Ui_AddSemester
from ui.ui_widget_adduserdata import Ui_NewUserData
from src.DashboardClasses import Charts, uni_data, student_data, semester_data, course_of_study_data, course_data, learning_tracker
from src.DataManagingClasses import menu_data, exam_data, study_data, user_data, input_handler
from datetime import date, datetime

# Daten Laden für Course Status Pie-Chart
course_data.update_data(study_data, exam_data, user_data)
amt_courses_done = len(course_data.get_courses_finished())
amt_courses_open = len(course_data.get_courses_in_progress())
amt_all_courses = (menu_data.load().get(course_of_study_data.name, {}).get("courses_amount", 34)
                   - (amt_courses_open + amt_courses_done))
# Erstellen von Course Status Pie-Chart
pie_chart_course_status = Charts("pie", pie_chart_values=[
    amt_courses_done,amt_courses_open,amt_all_courses])
pie_chart_course_status.fig.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.01)

# Lade Daten für AVG-Grade Line-Chart
course_of_study_data.get_all_grades(exam_data)
# Erstellen von AVG-Grade Line-Chart
line_chart_avg_grade_big = Charts(
    "line",
    y_values=course_of_study_data.all_grades,
    average_grade=course_of_study_data.get_average_grade(exam_data, user_data),
    avg_grade_line=True
)
line_chart_avg_grade_big.fig.subplots_adjust(left=0.06, right=0.99, top=0.95, bottom=0.05)

# Erstellen von kleinem AVG-Grade Line-Chart
line_chart_avg_grade_small = Charts("line", course_of_study_data.all_grades)
line_chart_avg_grade_small.set_opacity(0.5)
line_chart_avg_grade_small.fig.subplots_adjust(left=0.15, right=0.85, top=0.85, bottom=0.15)

#Erstellen von Weeks Pie Chart
remaining_weeks_pie_chart = Charts("pie70", remaining_weeks_semester=semester_data.get_remaining_weeks())
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

        # OK Button anfangs deaktivieren
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)

        # Überprüfen, ob passende Eingaben vorhanden sind und ggf. Button aktivieren
        self.lineEdit_Grade.textChanged.connect(self.check_input)
        self.comboBox_Modul.currentTextChanged.connect(self.check_input)

    def save_data(self):
        """Speichert übergebene Daten in exam_data.json"""
        self.exam_data.update(
            self.comboBox_Modul.currentText(),
            [self.comboBox_Passed.currentText(),self.lineEdit_Grade.text()]
            )
        self.accept()

    def load_data(self):
        """Extrahiert verfügbare, eingeschriebene Kurse. Kurse, die zuvor per Add Course hinzugefügt wurden"""
        assigned_courses = study_data.load().get("Courses", [])
        loaded_exam_data = exam_data.load()
        passed_courses = [key for key, value in loaded_exam_data.items() if value[0] == "Passed"]
        available_courses = [course for course in assigned_courses if course not in passed_courses]

        self.comboBox_Modul.addItems(available_courses)

    def check_input(self):
        """Überprüft Inhalt von lineEdit_Grade (Note), ob es type: float ist und ob es zwischen [0,6] liegt.
        Außerdem ob ein Modul ausgewählt wurde."""
        grade = self.lineEdit_Grade.text()
        course = self.comboBox_Modul.currentText()

        valid_grade = input_handler.validate_grade(grade)
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(valid_grade and bool(course))

# Dialogklasse Add Course
class AddCourseDialog(QDialog, Ui_AddCourse):
    def __init__(self, study_data):
        super().__init__()
        self.setupUi(self)
        self.load_data()
        self.study_data = study_data

        self.buttonBox.accepted.connect(self.save_data)
        self.buttonBox.rejected.connect(self.reject)

        # OK Button anfangs deaktivieren
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        # Überprüfen, ob passende Eingaben vorhanden sind und ggf. Button aktivieren
        self.lineEdit_ECTSPoints.textChanged.connect(self.check_input)
        self.comboBox_ExamType.currentTextChanged.connect(self.check_input)
        self.comboBox_CourseName.currentTextChanged.connect(self.check_input)

    def check_input(self):
        """Überprüft ob Eingabe in lineEdit_ECTSPoints (ECTS-Punkte) valide (Zahl) ist."""
        ects_input = self.lineEdit_ECTSPoints.text()
        course_name = self.comboBox_CourseName.currentText()
        exam_name = self.comboBox_ExamType.currentText()

        valid_ects_input = input_handler.validate_number(ects_input)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(valid_ects_input and bool(course_name) and bool(exam_name))

    def save_data(self):
        """Speichert Daten Courses, ECTS-Points und Exam-Type in study data"""
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
        """Lädt die aktuellen Daten aus und lädt sie in ComboBoxes ein."""
        course_data.update_data(study_data, exam_data, user_data)
        course_of_study_data.update_data(user_data, menu_data)
        # Alle Kurse des Studiengangs auslesen
        all_courses = (course_data.get_all_courses(course_of_study_data.name))
        # Kurse aus Kurs-Liste herausfiltern, die abgeschlossen oder in Bearbeitung sind
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
        # OK Button anfangs deaktivieren
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        # Überprüfen, ob passende Eingaben vorhanden sind und ggf. Button aktivieren
        self.dateEdit_StartDate.dateChanged.connect(self.check_input)
        self.comboBox_SemesterNumber.currentTextChanged.connect(self.check_input)

    def save_data(self):
        """Speichert Daten Semester und Start-Datum in study data"""
        self.study_data.update("Semester", self.comboBox_SemesterNumber.currentText())
        self.study_data.update("Start Date", self.dateEdit_StartDate.date().toString("yyyy-MM-dd"))
        self.accept()

    def load_data(self):
        """Lädt aus Stammdaten Kurs-Liste und Anzahl Semester"""
        course_of_study_data.update_data(user_data, menu_data)
        all_data = menu_data.load()
        # Semesteranzahl extrahieren
        cos_info = all_data.get(course_of_study_data.name, {})
        total_semester = cos_info.get("semester", 0)
        semesters_list = [str(nr) for nr in range(1, total_semester + 1)]

        self.comboBox_SemesterNumber.addItems(semesters_list)

    def check_input(self):
        sem_number = self.comboBox_SemesterNumber.currentText()
        date_input = self.dateEdit_StartDate.date().toString("yyyy-MM-dd")
        # Überprüfe Datumseingabe auch erwarteten Wert und keine Daten, die in der Zukunft liegen
        valid_date = input_handler.validate_date(date_input)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(valid_date and bool(sem_number))


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

        # OK Button anfangs deaktivieren
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        # Überprüfen, ob passende Eingaben vorhanden sind und ggf. Button aktivieren
        self.lineEdit_StudentName.textChanged.connect(self.check_input)
        self.lineEdit_StudentNumber.textChanged.connect(self.check_input)
        self.comboBox_University.currentTextChanged.connect(self.check_input)
        self.comboBox_CourseOfStudy.currentTextChanged.connect(self.check_input)

    def check_input(self):
        uni_name = self.comboBox_University.currentText()
        study_name = self.comboBox_CourseOfStudy.currentText()
        user_name = self.lineEdit_StudentName.text()
        user_student_nr = self.lineEdit_StudentNumber.text()
        valid_name = input_handler.validate_text(user_name)
        valid_number = input_handler.validate_text(user_student_nr)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(
            valid_name and
            valid_number and
            bool(uni_name) and
            bool(study_name)
        )

    def save_data(self):
        """Speichert Daten Universität, Student-Name, Student-Nummer und Studiumsnamen in user_data"""
        selected_university_name = self.comboBox_University.currentText()
        data_for_menu = self.menu_data.load()
        universities = data_for_menu.get("universities", [])
        selected_university = None
        #Überprüfe, ob University-Auswahl in Stammdaten ist, setzte selected_university = getroffene Auswahl
        for entry in universities:
            if entry[0] == selected_university_name:
                selected_university = entry
                break
        # Wenn selected_university == True bzw. nicht mehr None, update user_data mit Auswahl
        if selected_university:
            self.user_data.update("University", selected_university)
        else:
            ErrorMessage(self, "Universität wurde nicht gefunden.")
            return
        # Speichere Student-Name, Student-Nummer und Studiumsnamen in user_data
        self.user_data.update("Student Name", self.lineEdit_StudentName.text()),
        self.user_data.update("Student Number", self.lineEdit_StudentNumber.text()),
        self.user_data.update("Course of Study", self.comboBox_CourseOfStudy.currentText())

        self.accept()



    def load_data(self):
        """Lädt Daten aus Stammdaten für Dialog"""
        main_data = menu_data.load()
        # Universitätsnamen extrahieren
        universities = main_data.get("universities", [])
        university_names = [uni[0] for uni in universities]
        # Angebotene Kurse extrahieren
        all_courses = main_data.get("course_of_studies", [])

        self.comboBox_University.addItems(university_names)
        self.comboBox_CourseOfStudy.addItems(all_courses)


class ErrorMessage:
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
        self.opacity_up = None
        self.opacity_down = None
        self.setup_arrow_indicators()
        self.user_data = user_data
        self.study_data = study_data
        self.exam_data = exam_data
        self.menu_data = menu_data

        # Layout für Matplotlib-Insert AVG-Grades Line Chart Small
        layout = QtWidgets.QVBoxLayout(self.frame_avg_grades_chart_small)
        self.frame_avg_grades_chart_small.setLayout(layout)
        # Einbetten von MPL-Widget in frame_3
        layout.addWidget(line_chart_avg_grade_small)

        # Layout für MPL-Insert Weeks Left Pie-Chart
        layout = QtWidgets.QVBoxLayout(self.frame_3)
        self.frame_3.setLayout(layout)
        # Einbetten von MPL-Widget in frame_3
        layout.addWidget(remaining_weeks_pie_chart)

        # Layout für MPL-Insert Course Status Pie Chart
        layout = QtWidgets.QVBoxLayout(self.frame_pie_chart)
        self.frame_pie_chart.setLayout(layout)
        # Einbetten von MPL-Widget in frame_pie_chart
        layout.addWidget(pie_chart_course_status)

        # Layout für Matplotlib-Insert AVG-Grades Line Chart Big
        layout = QtWidgets.QVBoxLayout(self.frame_avg_grades_chart_big)
        self.frame_avg_grades_chart_big.setLayout(layout)
        # Einbetten von MPL-Widget in frame_avg_grades_chart_big
        layout.addWidget(line_chart_avg_grade_big)

        # Überlagerndes QLabel für Durchschnittsnote über AVG Grade Chart Small
        # => Lade Zahl "AVG-Grade" in Overlay Label
        self.overlay_label = QtWidgets.QLabel(
            str(course_of_study_data.get_average_grade(exam_data, user_data)),
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

        # Überlagerndes QLabel für "Verbleibende Woche"-Zahl über Weeks Left Frame
        # => Lade Zahl "Weeks Left" in Overlay Label
        self.overlay_label_right = QtWidgets.QLabel(
            str(semester_data.get_remaining_weeks()),
            parent=self.frame_3)
        self.overlay_label_right.setStyleSheet("""
                    font: 700 60pt \"Graduate\";\n
                    color: rgba(49, 149, 43, 1);
                    background-color: rgba(49, 149, 43, 0);
                    """)
        self.overlay_label_right.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.overlay_label_right.resize(self.frame_3.size())
        self.overlay_label_right.setAutoFillBackground(False)
        self.overlay_label_right.raise_()
        self.overlay_label_right.setGeometry(self.frame_3.rect())

        self.frame_3.resizeEvent = self.update_overlay_size_right

        # PushButtons Verknüpfung zu Dialogs
        self.pushButton_add_course.clicked.connect(self.open_add_course_dialog)
        self.pushButton_add_grade.clicked.connect(self.open_add_grade_dialog)
        self.pushButton_add_semester.clicked.connect(self.open_add_semester_dialog)
        self.pushButton_add_user_data.clicked.connect(self.open_add_user_data_dialog)

        # Lade AVG-Grade Differenz in GUI
        self.label_grade_move_pos.setText(str(course_of_study_data.get_grade_difference()))
        self.label_grade_move_neg.setText(str(course_of_study_data.get_grade_difference()))

        #course_of_study_data.get_average_grade(exam_data)
        #course_of_study_data.get_last_avg_grade(exam_data)

        grade_diff = course_of_study_data.get_grade_difference()
        if grade_diff < 0:
            self.set_arrow_visibility("down")
        elif grade_diff > 0:
            self.set_arrow_visibility("up")
        else:
            self.set_arrow_visibility("none")

        # Lade User Data Studen-Name und Student-Number in GUI
        self.label_input_student_name.setText(student_data.name)
        self.label_input_student_number.setText(student_data.student_number)

        # Lade User Data Universitätsadresse in GUI
        self.label_university_name.setText(uni_data.name)
        self.label_university_street.setText(uni_data.street)
        self.label_university_address.setText(uni_data.town)

        # Lade aktuelles Semester in GUI
        self.label_semester_number_bottom_left.setText(semester_data.semester_number)

        # Lade Courses Completed Daten in GUI
        self.label_courses_completet_number_bottom_mid.setText(str(len(course_data.get_courses_finished())))

        # Lade Courses Open Daten in GUI
        open_courses = (self.menu_data.load().get(course_of_study_data.name, {}).get("courses_amount", 0)
                        - len(course_data.get_courses_finished()))
        self.label_courses_open_number_bottom_right.setText(str(open_courses))

        # Lade Passed Weeks und Remaining Weeks in GUI (Label Top Right)
        self.label_semester_counter_number_right.setText(str(semester_data.get_passed_weeks()))
        self.label_semester_counter_number_left.setText(str(semester_data.get_remaining_weeks()))

        # Lade Learning-Streak Daten in GUI
        learning_tracker.load_data(self.user_data)

        current_streak = learning_tracker.current_streak(user_data=self.user_data)
        best_streak = learning_tracker.best_streak(user_data=self.user_data)
        self.label_current_streak_number.setText(str(current_streak))
        self.label_best_streak.setText("Best: "+str(best_streak)+" Days")


        # Speichere LearningStatus nach ButtonPush in userdata-File
        self.pushButton_learned_today.clicked.connect(lambda: self.learning_tracker_button_push(status=True))
        self.pushButton_not_learned_today.clicked.connect(lambda: self.learning_tracker_button_push(status=False))

    # Überprüfung, ob LearningStatus Buttons schon gedrückt wurde oder nicht
    def learning_tracker_button_push(self, status):
        """Reaktion auf Button Push Not Learned Today:( Learned Today:) / LearningStatus"""
        loaded_user_data = user_data.load()
        button_info = loaded_user_data.get("Learning Status Button", False)
        if button_info == False:
            user_data.update("Learning Status Button", True)
            user_data.update("Learning Status Date", str(date.today()))
            user_data.update("Learning Status", status)
            learning_tracker.calculating_streak(data=self.user_data)
        elif button_info == True:
            message = ("Achtung!\nEs wurden heute schon Learning-Daten gespeichert."
                       "\nResettet Counter auf 0 oder erhöht um 1\nDaten überschreiben? ")
            self.info_message(message, status)

    def info_message(self, message, new_status):
        """Info Dialog bei mehrfachem Learning Tracker Button Push """
        dialog_box = QMessageBox(self)
        dialog_box.setIcon(QMessageBox.Icon.Question)
        dialog_box.setWindowTitle("Info")
        dialog_box.setText(message)
        dialog_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        dialog_box.setStyleSheet("color: rgb(49, 149, 43);border-color: rgb(0, 0, 0);"
                                 "background-color: rgb(9, 20, 17);")
        button = dialog_box.exec()

        if button == QMessageBox.StandardButton.Yes:
            print("Overwrite exising data")
            user_data.update("Learning Status", new_status)
            learning_tracker.calculating_streak(data=self.user_data)
        else:
            print("Keep exising data")


    # Einfügen der Pixmap Pfeile in GUI
    def setup_arrow_indicators(self):
        """Initialisiert die Pfeilbilder und ihre Sichtbarkeit"""
        # Pfeile laden
        green_arrow = os.path.join(os.path.dirname(__file__), "..", "icons", "green_arrow.png")
        red_arrow = os.path.join(os.path.dirname(__file__), "..", "icons", "red_arrow.png")
        # Pfeileinstellungen
        arrow_size = 75
        pixmap_arrow_up = QPixmap(green_arrow).scaled(
            arrow_size, arrow_size,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )
        pixmap_arrow_down = QPixmap(red_arrow).scaled(
            arrow_size, arrow_size,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )
        # Alignment Setting - Zentriert
        self.label_arrow_up.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_arrow_down.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # In QLabel setzen
        self.label_arrow_up.setPixmap(pixmap_arrow_up)
        self.label_arrow_down.setPixmap(pixmap_arrow_down)

        # Opacity hinzufügen
        self.opacity_up = QGraphicsOpacityEffect()
        self.opacity_down = QGraphicsOpacityEffect()
        self.label_arrow_up.setGraphicsEffect(self.opacity_up)
        self.label_arrow_down.setGraphicsEffect(self.opacity_down)

    def set_arrow_visibility(self, direction: str):
        """Steuert Sichtbarkeit der Pfeile: 'up', 'down', 'none'"""
        if direction == 'up':
            self.opacity_up.setOpacity(1.0)
            self.opacity_down.setOpacity(0.2)
        elif direction == 'down':
            self.opacity_up.setOpacity(0.2)
            self.opacity_down.setOpacity(1.0)
        else:
            self.opacity_up.setOpacity(1.0)
            self.opacity_down.setOpacity(1.0)

    # Resizing Methode für Overlay-Widget AVG-Grade links oben
    def update_overlay_size(self, event):
        self.overlay_label.setGeometry(self.frame_avg_grades_chart_small.rect())
        event.accept()
    def update_overlay_size_right(self, event):
        self.overlay_label_right.setGeometry(self.frame_3.rect())
        event.accept()

    # Funktionen zum Öffnen und Arbeiten mit den Dialogs
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
        """Methode zum Aktualisieren der GUI, nach neuer Dateneingabe. Mit Abfrage auf Dialog-Fenster."""

        if grade_dialog:
            # Update Courses Completed
            course_data.update_data(study_data, exam_data, user_data)
            self.label_courses_completet_number_bottom_mid.setText(str(len(course_data.get_courses_finished())))

            # Update Courses Open
            new_open_courses = (self.menu_data.load().get(course_of_study_data.name, {}).get("courses_amount", 0)
                            - len(course_data.get_courses_finished()))
            self.label_courses_open_number_bottom_right.setText(str(new_open_courses))

            # Update AVG-Grade Difference
            course_of_study_data.get_average_grade(exam_data, user_data)
            course_of_study_data.get_last_avg_grade(exam_data, user_data)
            self.label_grade_move_pos.setText(str(course_of_study_data.get_grade_difference()))
            self.label_grade_move_neg.setText(str(course_of_study_data.get_grade_difference()))

            grade_diff = course_of_study_data.get_grade_difference()
            if grade_diff < 0:
                self.set_arrow_visibility("down")
            elif grade_diff > 0:
                self.set_arrow_visibility("up")
            else:
                self.set_arrow_visibility("none")

            # Update AVG-Grade Charts
            # Großer AVG-Grade Line-Chart
            line_chart_avg_grade_big.update_charts(
                y_values=course_of_study_data.all_grades,
                average_grade=course_of_study_data.get_average_grade(exam_data, user_data),
                avg_grade_line=True
            )

            # Kleiner AVG-Grade Line-Chart
            line_chart_avg_grade_small.update_charts(y_values=course_of_study_data.all_grades)

            # Update AVG-Grade Anzeige links oben
            self.overlay_label.setText(str(course_of_study_data.get_average_grade(exam_data, user_data)))

            # Update Pie-Chart Course Status
            course_data.update_data(study_data, exam_data, user_data)
            new_amt_courses_done = len(course_data.get_courses_finished())
            new_amt_courses_open = len(course_data.get_courses_in_progress())
            new_amt_all_courses = (self.menu_data.load().get(course_of_study_data.name, {}).get("courses_amount", 0)
                                   - (new_amt_courses_open + new_amt_courses_done))

            pie_chart_course_status.update_charts(pie_chart_values=[
                new_amt_courses_done,
                new_amt_courses_open,
                new_amt_all_courses
            ])

        if course_dialog:
            # Update Pie-Chart Course Status
            course_data.update_data(study_data, exam_data, user_data)
            new_amt_courses_done = len(course_data.get_courses_finished())
            new_amt_courses_open = len(course_data.get_courses_in_progress())
            new_amt_all_courses = (self.menu_data.load().get(course_of_study_data.name, {}).get("courses_amount")
                                   - (new_amt_courses_open + new_amt_courses_done))

            pie_chart_course_status.update_charts(pie_chart_values=[
                new_amt_courses_done,
                new_amt_courses_open,
                new_amt_all_courses
            ])


        if semester_dialog:
            semester_data.update_data()
            # Update aktuelles Semester in GUI
            self.label_semester_number_bottom_left.setText(semester_data.semester_number)
            # Update Remaining Weeks Pie Chart
            remaining_weeks_pie_chart.update_charts(remaining_weeks_semester=semester_data.get_remaining_weeks())

            # Update Weeks Left Anzeige rechts oben
            semester_data.update_data()
            self.overlay_label_right.setText(str(semester_data.get_remaining_weeks()))

            # Update Weeks Left (rechts oben) Anzeigen Done und Open
            self.label_semester_counter_number_right.setText(str(semester_data.get_passed_weeks()))
            self.label_semester_counter_number_left.setText(str(semester_data.get_remaining_weeks()))

        if user_dialog:
            updated_user_data = self.user_data.load()
            loaded_menu_data = self.menu_data.load()
            # Update User Data Studen-Name, Student-Number in GUI
            self.label_input_student_name.setText(updated_user_data.get("Student Name", ""))
            self.label_input_student_number.setText(updated_user_data.get("Student Number", ""))

            # Update User Data Universitätsadresse in GUI
            university_data = updated_user_data.get("University", ["name", "street", "town"])
            self.label_university_name.setText(university_data[0])
            self.label_university_street.setText(university_data[1])
            self.label_university_address.setText(university_data[2])

            # Update Courses Open
            course_of_study = updated_user_data.get("Course of Study", "")
            open_courses = loaded_menu_data.get(course_of_study, {}).get("courses_amount", 0)
            self.label_courses_open_number_bottom_right.setText(str(open_courses))




