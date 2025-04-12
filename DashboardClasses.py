from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date, timedelta
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QWidget

matplotlib.use("QtAgg")


@dataclass
class University:
    name: str
    street: str
    zip_code: int
    town: str
    students = []
    course_of_study = []

    def info(self):
        """Gibt vollständige Adresse der Universität wieder"""
        return f"""{self.name}\n{self.street}\n{self.zip_code} {self.town}"""

    def add_student(self, new_student):
        """Fügt einen Studenten zur Liste der studierenden der Universität hinzu und fügt diese Universität zum Studenten hinzu"""
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

@dataclass
class Student:
    name: str
    matrikelnummer: int
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
            return "Keine Lerndaten vorhanden"
        print(self.learning_streaks)
    def get_course_of_study(self):
        """Gibt den aktuellen Studiengang wieder, soweit vorhanden"""
        if self.course_of_study is None:
            return f"{self.name} ist in keinem Studiengang eingeschrieben"
        return self.course_of_study

class LearningTracker:
    def __init__(self, student_name):
        self._current_streak = 0
        self._best_streak = 0
        student_name.learning_streaks = self

    def __str__(self):
        return f"Calculated current streak: {self.current_streak}\nCalculated best streak: {self._best_streak}"

    def calculating_streak(self, learned: bool):
        """Berechnet die dauer des aktuellen Streaks, falls der Streak unterbrochen wird, wird der Counter wieder auf 0 gesetzt.
        Ist der aktuelle Streak größer als der beste Streak, wird der beste Streak entsprechend aktualisiert"""
        #Achtung! Variable "gelernt" noch nicht definiert!
        if learned == True:
            self._current_streak += 1
            if self._current_streak > self._best_streak:
                self._best_streak = self._current_streak
        else:
            self._current_streak = 0

    @property
    def current_streak(self):
        return self._current_streak
    @property
    def best_streak(self):
        return self._best_streak

class CourseOfStudy:
    def __init__(self, name, num_semesters, ects_points):
        self.name = name
        self.num_semesters = num_semesters
        self.ects_points = ects_points
        self.semesters = []
        self.students = []
        self.current_avg_grade = None
        self.last_avg_grade = None

    def get_average_grade(self, ):
        """Berechnet die Durchschnittsnote auf Basis aller bisher erhaltenen Noten"""
        pass

    def get_grade_difference(self, ):
        """Berechnet die Differenz zwischen alter Durchschnittsnote und neuer Durchschnittsnote"""
        pass

    def add_semester(self, semester):
        """Fügt dem Studiengang ein Semester hinzu"""
        if len(self.semesters) >= self.num_semesters:
           pass
        else:
            self.semesters.append(semester)

    def add_student(self, new_student):
        """Fügt einen Studenten zur Liste dieses Studiengangs hinzu und fügt diesen Studiengang zum Studenten hinzu"""
        if new_student.course_of_study is None:
            self.students.append(new_student)
            new_student.course_of_study = self
        else:
            print("Student ist schon in einem anderen Studiengang eingeschrieben")

class Semester:
    def __init__(self, semester_number, start_date):
        self.semester_number = semester_number
        self.start_date = datetime.strptime(start_date, "%Y.%m.%d")
        self.end_date = start_date + timedelta(months=6)
        self.modules = []

    def get_remaining_weeks(self):
        """Gibt die verbleibenden Wochen des Semesters wieder"""
        remaining_weeks = (self.end_date - date.today()).days // 7
        if remaining_weeks > 0:
            return remaining_weeks
        else:
            return 0

    def add_module(self, module):
        """Fügt ein Modul zu einem Semester hinzu"""
        if module not in self.modules:
            self.modules.append(module)
        else:
            return "Dieses Modul ist schon vorhanden"

    def __repr__(self):
        return f"Semester Number {self.semester_number}, Start date {self.start_date}, End date {self.end_date}, Modules {self.modules}"
    def __str__(self):
        return f"Semester Number {self.semester_number}, Start date {self.start_date}, End date {self.end_date}, Modules {self.modules}"

class Modul:
    def __init__(self, name, semester, ects_points, status, exam_type):
        self.name = name
        self.semester = semester
        self.ects_points = ects_points
        self.status = status
        self.exam_type = exam_type
        self.exams = []

    def add_exam(self, exam_performance):
        """Fügt eine Prüfungsleistung zu dem Modul hinzu"""
        if len(self.exams) < 3:
            self.exams.append(exam_performance)
        else:
            return "Maximal 3 Prüfungen erlaubt"

    def get_status(self):
        """Gibt den aktuellen Bearbeitungsstatus des Moduls zurück"""
        return self.status

    def __repr__(self):
        return f"Name: {self.name}, ECTS-Punkte: {self.ects_points}, Status: {self.status}, Exam Type: {self.exam_type}, Number of Exams: " + str(len(self.exams))

    def __str__(self):
        return f"Name: {self.name}, ECTS-Punkte: {self.ects_points}, Status: {self.status}, Exam Type: {self.exam_type}, Number of Exams: " + str(len(self.exams))

@dataclass
class ExamPerformance:
    modul: object
    passed: bool
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

class charts(FigureCanvasQTAgg):
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
        ax = self.axes
        ax.clear()
        #Total weeks = 70% from Pie-Charts
        remaining = self.remaining_weeks_semester or 0
        remaining_converted = 70 / self.total_weeks_semester * remaining
        passed_converted = 70 - remaining_converted

        size = 0.3
        #values outer ring - [invisible 15%, red-range, yello-range, green-range, invisible 15%]
        vals_o = [15, 3, 10, 57, 15]
        #values inner ring - [invisible 15%, green-range, grey-range, invisible 15%]
        #green-range + grey-range := 70%!
        vals_i = [15, remaining_converted, passed_converted, 15]

        #Specs and Style outer ring
        ax.pie(
            vals_o,
            radius=1,
            colors=["none", "red", "yellow", "#003B00", "none"],
            wedgeprops=dict(width=0.05, edgecolor='none'),
            startangle=270
        )
        #Specs and Style inner ring
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
        #Opacity für X-Achse und Y-Achse
        for spine in ["left", "bottom"]:
            ax.spines[spine].set_alpha(alpha)
        #Opacity für Y-Achsen-Werte
        for label in ax.get_yticklabels():
            label.set_alpha(alpha)
        #Opacity für Achsen-Striche "ticks"
        for tick in ax.xaxis.get_major_ticks():
            tick.tick1line.set_alpha(alpha)
        for tick in ax.yaxis.get_major_ticks():
            tick.tick1line.set_alpha(alpha)

        self.draw()