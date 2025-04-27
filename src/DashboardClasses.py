from dataclasses import dataclass
from typing import Optional
from datetime import date, timedelta
import matplotlib

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QWidget
from src.DataManagingClasses import menu_data, exam_data, study_data, user_data

matplotlib.use("QtAgg")

@dataclass
class University:
    name: str
    street: str
    town: str
    students = []
    course_of_study = []

    def info(self):
        """Gibt vollständige Adresse der Universität wieder"""
        return f"""{self.name}\n{self.street}\n{self.town}"""

    def add_student(self, new_student):
        """Fügt einen Studenten zur Liste der Studierenden der Universität hinzu
         und fügt diese Universität zum Studenten hinzu"""
        if new_student.university is None:
            self.students.append(new_student)
            new_student.university = self
        else:
            print("Student ist schon in einer anderen Universität eingeschrieben")

    def add_course_of_study(self, course_of_study):
        """Fügt einen Studiengang zur Liste der angebotenen Studiengänge hinzu"""
        if course_of_study not in self.course_of_study:
            self.course_of_study.append(course_of_study)
        else:
            print("Studiengang wird schon angeboten")

    def remove_student(self, student):
        """Entfernt einen Studenten aus der Liste der Studierenden"""
        self.students.remove(student)

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

@dataclass
class Student:
    name: str
    student_number: str
    university: Optional[object] = None
    course_of_study: Optional[object] = None
    learning_streaks: Optional[object] = None

    def get_university(self):
        """Gibt den Namen der eingeschriebenen Universität wieder, soweit vorhanden"""
        if self.university is None:
            return f"{self.name} ist in keiner Universität eingeschrieben"
        return self.university

    def get_learning_streaks(self):
        """Gibt den aktuellen Lern-Streak und den besten Lern-Streak wieder, soweit vorhanden"""
        if self.learning_streaks is None:
            return print("Keine Lerndaten vorhanden")
        return self.learning_streaks
    def get_course_of_study(self):
        """Gibt den aktuellen Studiengang wieder, soweit vorhanden"""
        if self.course_of_study is None:
            return f"{self.name} ist in keinem Studiengang eingeschrieben"
        return self.course_of_study

    def __repr__(self):
        return f"Name: {self.name}\nStudent Number: {self.student_number}"
    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Student Number: {self.student_number}\n"
                f"University: {self.university}\n"
                f"Course of Study: {self.course_of_study}\n"
                f"Learning Streak: {self.learning_streaks}")

class LearningTracker:
    def __init__(self):
        self._current_streak = 0
        self._best_streak = 0
        self.student_name = None

    def __str__(self):
        return f"Calculated current streak: {self._current_streak}\nCalculated best streak: {self._best_streak}"

    def __repr__(self):
        return f"Calculated current streak: {self._current_streak}\nCalculated best streak: {self._best_streak}"

    def calculating_streak(self, data):
        """Berechnet die Dauer des aktuellen Streaks und speichert die Daten.
        Falls der Streak unterbrochen wird, wird der Counter wieder auf 0 gesetzt.
        Ist der aktuelle Streak größer als der beste Streak, wird der beste Streak entsprechend aktualisiert"""
        loaded_data = data.load()
        button_info = loaded_data.get("Learning Status Button")
        learning_date = loaded_data.get("Learning Status Date", "")

        # Nur zählen, wenn wirklich heute gelernt wurde.
        # Check Button Info = True und Learning Datum = Heute
        if button_info is True and learning_date == str(date.today()):
            learning_status = loaded_data.get("Learning Status")
            if learning_status == True:
                self._current_streak += 1
                if self._current_streak > self._best_streak:
                    self._best_streak = self._current_streak
                user_data.update("Current Streak", self._current_streak)
                user_data.update("Best Streak", self._best_streak)
                print("Updated Current Streak and Best Streak in Data")
            else:
                user_data.update("Current Streak", 0)
        else:
            # Heute noch nicht gelernt => nichts tun
            pass

    def load_data(self, user_data):
        """Updated current_streak und best_streak mit Daten aus user_data File"""
        loaded_data = user_data.load()
        self._current_streak = loaded_data.get("Current Streak")
        self._best_streak = loaded_data.get("Best Streak")

    def current_streak(self, user_data):
        """Gibt aktuellen current_streak wieder. Nutzt Methode load_data() für aktuelle Daten"""
        data = user_data
        self.load_data(data)
        return self._current_streak

    def best_streak(self, user_data):
        """Gibt aktuellen best_streak wieder. Nutzt Methode load_data() für aktuelle Daten"""
        data = user_data
        self.load_data(data)
        return self._best_streak


class CourseOfStudy:
    def __init__(self, name, num_semesters, ects_points):
        self.name = name
        self.num_semesters = num_semesters
        self.ects_points = ects_points
        self.semesters = []
        self.students = []
        self.all_grades = []
        self.current_avg_grade = 0
        self.last_avg_grade = 0

    def get_all_grades(self, data):
        """Gibt alle Noten zurück, gespeichert in self.all_grades, geladen aus exam_data.json"""
        grade_data = data.load()
        all_grades = [float(value[1]) for value in grade_data.values() if value[0] == "Passed"]
        self.all_grades = all_grades
        return self.all_grades

    def get_average_grade(self, exam_data, user_data):
        """Berechnet die Durchschnittsnote auf Basis aller bisher erhaltenen Noten"""
        grade_data = exam_data.load()
        all_grades = [float(value[1]) for value in grade_data.values() if value[0] == "Passed"]
        avg_grade = sum(all_grades) / (len(all_grades) if len(all_grades) > 0 else 1)
        self.all_grades = all_grades
        self.current_avg_grade = round(avg_grade, 2)
        self.save_avg_grades(user_data)
        return self.current_avg_grade

    def get_last_avg_grade(self, exam_data, user_data):
        """Gibt die letzte Durchschnittsnote zurück. Bezieht alle Noten, bis auf die letzte in Berechnung ein"""
        grade_data = exam_data.load()
        all_grades = [float(value[1]) for value in grade_data.values() if value[0] == "Passed"]
        all_grades_except_last = all_grades[:-1]
        last_avg_grade = (sum(all_grades_except_last)
                          / (len(all_grades_except_last)
                             if len(all_grades_except_last) > 0 else 1))
        self.last_avg_grade = round(last_avg_grade, 2)
        self.save_avg_grades(user_data)
        return self.last_avg_grade

    def get_grade_difference(self):
        """Berechnet die Differenz zwischen alter Durchschnittsnote und neuer Durchschnittsnote"""
        return round(self.last_avg_grade - self.current_avg_grade, 2)

    def save_avg_grades(self, data):
        """Speichert Average Grade:self.current_avg_grade und
        Last AVG Grade:self.last_avg_grade als dict in übergebene JSON-Datei"""
        data.update("Average Grade", self.current_avg_grade)
        data.update("Last AVG Grade", self.last_avg_grade)

    def add_semester(self, semester):
        """Fügt dem Studiengang ein Semester hinzu"""
        if len(self.semesters) >= self.num_semesters:
           pass
        else:
            self.semesters.append(semester)

    def add_student(self, new_student):
        """Fügt einen Studenten zur Liste dieses Studiengangs hinzu
        und fügt diesen Studiengang zum Studenten hinzu"""
        if new_student.course_of_study is None:
            self.students.append(new_student)
            new_student.course_of_study = self.name
        else:
            print("Student ist schon in einem anderen Studiengang eingeschrieben")

    def update_data(self, user_data, menu_data):
        """Setzt self.name, self.num_semesters und self.ects_points, falls vorhanden.
        Ansonsten werden Default-Werte gesetzt."""
        new_user_data = user_data.load()
        new_menu_data = menu_data.load()
        self.name = new_user_data.get("Course of Study", "")
        if self.name == "" or self.name not in new_menu_data:
            print("Studiengang nicht gefunden, lade default Werte")
            self.num_semesters = 0
            self.ects_points = 0
            return False
        else:
            self.num_semesters = new_menu_data[self.name].get("semester", 0)
            self.ects_points = new_menu_data[self.name].get("ects_points", 0)
            self.last_avg_grade = new_user_data.get("Last AVG Grade", 0)
            self.current_avg_grade = new_user_data.get("Average Grade", 0)
            return True

    def __repr__(self):
        return f"Course of Study Name: {self.name}"
    def __str__(self):
        return f"Course of Study Name: {self.name}\nSemesters: {self.num_semesters}\nECTS-Points: {self.ects_points}"


class Semester:
    def __init__(self, semester_number, start_date_string):
        self.semester_number = semester_number
        self.start_date = date.fromisoformat(start_date_string)
        self.end_date = self.start_date + timedelta(weeks=26)
        self.courses = []

    def get_remaining_weeks(self):
        """Gibt die verbleibenden Wochen des Semesters wieder"""
        remaining_weeks = round((self.end_date - date.today()).days / 7)
        if remaining_weeks > 0:
            return remaining_weeks
        else:
            return 0

    def get_passed_weeks(self):
        """Gibt die vergangenen Wochen des Semesters wieder"""
        passed_weeks = round((date.today() - self.start_date).days / 7)
        if passed_weeks < 26:
            return passed_weeks
        else:
            return 26

    def add_module(self, course):
        """Fügt ein Modul zu einem Semester hinzu"""
        if course not in self.courses:
            return self.courses.append(course)
        else:
            return print("Dieses Modul ist schon vorhanden")

    def update_data(self):
        """Aktualisiert Semesterdaten aus Study_Data.json.
        self.start_date, self.end_date, self.semester_number."""
        self.start_date = date.fromisoformat(study_data.load().get("Start Date", "2024-01-01"))
        self.semester_number = study_data.load().get("Semester", "0")
        self.end_date = self.start_date + timedelta(weeks=26)


    def __repr__(self):
        return f"Semester Number: {self.semester_number}\nStart date: {self.start_date}\nEnd date: {self.end_date}\nModules: {self.courses}"
    def __str__(self):
        return f"Semester Number: {self.semester_number}\nStart date: {self.start_date}\nEnd date: {self.end_date}\nModules: {self.courses}"

class Course:
    def __init__(self, menu_data):
        self.menu_data = menu_data
        self.study_data = None
        self.exam_data = None
        self.user_data = None
        self.all_courses = []
        self.courses_in_progress = []
        self.courses_finished = []
        self.exam_types = []

    def get_all_courses(self, course_of_study):
        """Gibt für übergebenen Studiengang alle in menu_data enthaltenen Kurse wieder """
        main_data = self.menu_data.load()
        all_available_courses = main_data.get(course_of_study, {}).get("courses", [])
        self.all_courses = all_available_courses
        return self.all_courses

    def get_courses_in_progress(self):
        """Gibt alle Kurse wieder, die in Bearbeitung sind. Also via Add Course dialog hinzugefügt wurden
        aber noch nicht abgeschlossen sind (exam data, status = passed).
        update_data Methode vorher aufrufen."""
        load_exam_data = self.exam_data.load()
        load_study_data = self.study_data.load()
        open_course_data = load_study_data.get("Courses", [])
        passed_courses = [key for key, value in load_exam_data.items() if value[0] == "Passed"]
        self.courses_in_progress = []
        for course in open_course_data:
            if course not in passed_courses:
                self.courses_in_progress.append(course)
        return self.courses_in_progress

    def get_courses_finished(self):
        """Gibt alle erfolgreich abgeschlossenen Kurse wieder.
        update_data Methode vorher aufrufen."""
        load_exam_data = self.exam_data.load()
        passed_courses = [key for key, value in load_exam_data.items() if value[0] == "Passed"]
        return passed_courses

    def update_data(self, new_study_data, new_exam_data, new_user_data):
        """Übergibt Files an self.study_data, self.exam_data und self.user_data.
        Ohne Ausführung sind Default-Werte dafür None!"""
        self.study_data = new_study_data
        self.exam_data = new_exam_data
        self.user_data = new_user_data

    def get_exam_types(self):
        """Gibt für ausgewähltes Studium Liste an Examtypen wieder, die in menu_data hinterlegt sind."""
        if not self.user_data:
            return []
        user_info = self.user_data.load()
        course_name = user_info.get("Course of Study", "").strip()
        cos_data = self.menu_data.load().get(course_name)
        if cos_data is None:
            return []
        return cos_data.get("exam_type", [])


@dataclass
class ExamPerformance:
    modul: str
    passed: str
    grade: float

    def check_status(self):
        """Gibt den Status der Prüfung zurück, ob bestanden oder nicht"""
        return self.passed

    def get_grade(self):
        """Gibt die Note der Prüfung zurück als Float"""
        if self.grade is not None:
            return self.grade
        else:
            return "No Grade Available"

class Charts(FigureCanvasQTAgg):
    def __init__(self,
                 chart_type="line",
                 y_values=None,
                 average_grade=0,
                 avg_grade_line=False,
                 pie_chart_values=None,
                 remaining_weeks_semester=None,
                 parent: QWidget = None
                 ):
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)

        # Attribute
        self.chart_type = chart_type
        self.y_values = y_values or []
        self.x_values = list(range(len(self.y_values)))
        self.chart_color = "#003B00"
        self.chart_title = ""
        self.y_ticks = [1, 2, 3, 4, 5, 6]
        self.avg_grade_line = avg_grade_line
        self.average_grade = average_grade
        self.pie_chart_values = pie_chart_values
        self.total_weeks_semester = 26
        self.remaining_weeks_semester = remaining_weeks_semester

        # Background + Styling
        self.fig.patch.set_alpha(0)
        self.axes.set_facecolor("none")

        # Chart-Auswahl
        if self.chart_type == "line":
            self.plot_line_chart()

        elif self.chart_type == "pie":
            self.plot_pie_chart()

        elif self.chart_type == "pie70":
            self.plot_pie70_chart()

    def plot_line_chart(self):
        """Erstellt ein Line Chart mit angepasstem Styling und Werten."""
        ax = self.axes
        ax.clear()
        ax.plot(self.x_values, self.y_values, self.chart_color)

        # Achsen-Styling
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_color(self.chart_color)
        ax.spines["left"].set_color(self.chart_color)
        ax.spines["bottom"].set_linewidth(2)
        ax.spines["left"].set_linewidth(2)
        ax.set_xticks(self.x_values)
        ax.set_yticks(self.y_ticks)
        ax.tick_params(axis="both", colors=self.chart_color, labelsize=14, length=10, width=2)
        ax.set_xticklabels([])  # Optional: X-Achsenbeschriftungen leer
        ax.set_title(self.chart_title, fontsize=18, color=self.chart_color)
        # Durchschnittslinie (optional)
        if self.avg_grade_line == True:
            ax.axhline(self.average_grade, color="blue", linestyle="--", linewidth=2)

    def plot_pie_chart(self):
        """Erstellt ein Pie Chart mit angepasstem Styling und Werten."""
        ax = self.axes
        ax.clear()
        labels = ("Done", "In Progress", "Open")
        sizes = self.pie_chart_values or [0, 0, 0]

        ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            colors=["#008F11", "#92e5a1", "#A5FFFF"],
            pctdistance=0.4,
            labeldistance=0.6,
            explode=(0.1, 0, 0),
            shadow=True,
            startangle=90,
            radius=1.2,
            textprops={'fontsize': 8}
        )

    def plot_pie70_chart(self):
        """Erstellt zwei spezielle Pie Charts (ein äußerer und ein innerer)
        mit angepasstem Styling und Werten."""
        ax = self.axes
        ax.clear()
        #Total weeks = 70% von Pie-Chart
        remaining = self.remaining_weeks_semester or 0
        remaining_converted = 70 / self.total_weeks_semester * remaining
        passed_converted = 70 - remaining_converted

        size = 0.3
        #Werte äußerer Ring - [invisible 15%, red-range, yellow-range, green-range, invisible 15%]
        vals_o = [15, 3, 10, 57, 15]
        #Werte innerer Ring - [invisible 15%, green-range, grey-range, invisible 15%]
        #green-range + grey-range := 70%!
        vals_i = [15, remaining_converted, passed_converted, 15]

        #Specs und Style äußerer Ring
        ax.pie(
            vals_o,
            radius=1,
            colors=["none", "red", "yellow", "#003B00", "none"],
            wedgeprops=dict(width=0.05, edgecolor='none'),
            startangle=270
        )
        #Specs und Style innerer Ring
        ax.pie(
            vals_i,
            radius=0.92,
            colors=["none", "0.2", "#003B00", "none"],
            wedgeprops=dict(width=size, edgecolor='none'),
            startangle=270
        )

        ax.set(aspect="equal")

    def set_opacity(self, alpha=0.5):
        """Einstellung der Transparenz von Chart und Achsen"""
        ax = self.axes
        #Opacity für Chart-Linie/Graph
        for line in ax.get_lines():
            line.set_alpha(alpha)
        #Opacity für x-Achse und y-Achse
        for spine in ["left", "bottom"]:
            ax.spines[spine].set_alpha(alpha)
        #Opacity für y-Achsen-Werte
        for label in ax.get_yticklabels():
            label.set_alpha(alpha)
        #Opacity für Achsen-Striche "ticks"
        for tick in ax.xaxis.get_major_ticks():
            tick.tick1line.set_alpha(alpha)
        for tick in ax.yaxis.get_major_ticks():
            tick.tick1line.set_alpha(alpha)

        self.draw()

    def update_charts(self, **kwargs):
        """Methode zum Updaten und neuen Zeichnen der Charts."""
        if self.chart_type == "line":
            self.y_values = kwargs.get("y_values", [])
            self.average_grade = kwargs.get("average_grade", 0)
            self.avg_grade_line = kwargs.get("avg_grade_line", False)
            self.x_values = list(range(len(self.y_values)))
            self.plot_line_chart()
        elif self.chart_type == "pie":
            self.pie_chart_values = kwargs.get("pie_chart_values", [0, 0, 0])
            self.plot_pie_chart()
        elif self.chart_type == "pie70":
            self.remaining_weeks_semester = kwargs.get("remaining_weeks_semester", 0)
            self.plot_pie70_chart()

        self.draw()


loaded_user_data = user_data.load()
loaded_study_data = study_data.load()
loaded_menu_data = menu_data.load()

# Erstellen der University-Instanz aus vorhandenen Daten oder Standard-Daten falls keine Daten vorhanden sind
if loaded_user_data != {}:
    loaded_uni_data = loaded_user_data.get("University", ["name", "street", "town"])
    uni_data = University(loaded_uni_data[0], loaded_uni_data[1], loaded_uni_data[2])
else:
    uni_data = University("N/A", "N/A", "N/A")

# Erstellen der Student-Instanz aus vorhandenen Daten oder Standard-Daten falls keine Daten vorhanden sind
if loaded_user_data != {}:
    loaded_student_name = loaded_user_data.get("Student Name", "N/A")
    loaded_student_number = loaded_user_data.get("Student Number", "N/A")
    student_data = Student(loaded_student_name, loaded_student_number)
else: student_data = Student("N/A", "N/A")

# Erstellen der Semester-Instanz aus vorhandenen Daten oder Standrad-Daten falls keine Daten vorhanden sind
if loaded_study_data != {}:
    loaded_semester_number = loaded_study_data.get("Semester", "0")
    loaded_semester_start_date = loaded_study_data.get("Start Date", "2024-01-01")
    semester_data = Semester(loaded_semester_number, loaded_semester_start_date)
else:
    semester_data = Semester("N/A", "2024-01-01")

# Erstellen der CourseOfStudy-Instanz aus vorhandenen Daten oder Standard-Daten falls keine Daten vorhanden sind
loaded_CoS_name = loaded_user_data.get("Course of Study")

if loaded_CoS_name and loaded_CoS_name in loaded_menu_data:
    loaded_num_semesters = loaded_menu_data[loaded_CoS_name].get("semester", 0)
    loaded_ects_points = loaded_menu_data[loaded_CoS_name].get("ects_points", 0)
    course_of_study_data = CourseOfStudy(loaded_CoS_name, loaded_num_semesters, loaded_ects_points)
    course_of_study_data.update_data(user_data, menu_data)
else:
    print("Keine gültigen Studiengangdaten gefunden – Default-Werte werden verwendet.")
    course_of_study_data = CourseOfStudy("N/A", 0, 0)

# Erstellen der Course-Instanz aus vorhandenen Daten oder Standard-Daten falls keine Daten vorhanden sind
course_data = Course(menu_data)

# Erstellen der Learning-Tracker instanz
learning_tracker = LearningTracker()

# Erstelle ExamPerformance Instanzen
all_exam_data = exam_data.load()
exam_instances = {}
for key, value in all_exam_data.items():
    class_name = key.replace(" ", "_")
    exam_instances[class_name] = ExamPerformance(class_name, value[0], value[1])


course_of_study_data.add_student(student_data)
learning_tracker.student_name = student_data.name
uni_data.add_student(student_data)
uni_data.add_course_of_study(course_of_study_data)
student_data.course = course_of_study_data
student_data.learning_streaks = learning_tracker

print(uni_data)
print(course_of_study_data)
print(student_data)



#ALS NÄCHSTES

# Fehlerüberprüfung / Debugging
# - Learned Today Counter kann manipuliert werden durch mehrmaliges drücken von learned today

# In Windows 11 neue venv ohne irgendwas erstellen. Programm über GitHub runterladen und in der venv starten.
# Ausprobieren, ob es direkt läuft bzw. was ich dazu brauche (müssen die ganzen bibliotheken vorhanden sein?)
# exe-Datei erstellen (PyQT6 Buch eintrag nachlesen)

# Readme-Datei erstellen "Anleitung"

