import json
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt


class JSONFile:
    def __init__(self, filename: str, default_type: str = "dict"):
        """Erstellt eine JSON-Datei, falls sie nicht existiert.
        default_type kann 'dict' (Dictionary) oder 'list' (Liste) sein.
        """
        self.filename = filename
        self.default_type = default_type
        self.new_file()

    def new_file(self):
        """Erstellt eine leere JSON-Datei mit {} oder [] je nach default_type."""
        default_data = {} if self.default_type == "dict" else []
        self.save(default_data)

    def save(self, data):
        """Speichert Daten in die JSON-Datei."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load(self):
        """Lädt die JSON-Daten aus der Datei und gibt sie zurück."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            # Falls die Datei beschädigt oder leer ist, wird sie neu erstellt
            self.new_file()
            return {} if self.default_type == "dict" else []

    def update(self, key, value):
        """Fügt ein Schlüssel-Wert-Paar zu einem Dictionary hinzu (nur für dict-Modus)."""
        if self.default_type != "dict":
            raise ValueError("Update funktioniert nur mit Dictionary-basierten JSON-Dateien!")

        data = self.load()
        data[key] = value
        self.save(data)

    def append(self, item):
        """Fügt ein Element zu einer Liste hinzu (nur für list-Modus)."""
        if self.default_type != "list":
            raise ValueError("Append funktioniert nur mit Listen-basierten JSON-Dateien!")

        data = self.load()
        data.append(item)
        self.save(data)

    def clear(self):
        """Löscht den Inhalt der JSON-Datei und setzt sie zurück."""
        self.new_file()

@dataclass
class University:
    name: str
    street: str
    zip_code: str
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

#Optional könnte ich noch town: str = " " machen, damit town ein optionales argument wird
#und dann durch gegebene PLZ automatisch die town heraussuchen und ausgeben?

#nutzung von dataclass, da einfache Klasse die vorrangig nur Daten speichert und wenige Methoden hat. dataclass ist
#kompakter, normale Klasse wird nicht unbedingt benötigt
#keine speziellen Methoden für get_university_name und get_university_location, da jetziger Zugriff durch zum Beispiel
#university.name einfacher ist und durch direkten zugriff wird klar, auf welches Attribut man zugreift
#Methoden add_student und remove_student ergänzt, um Aggregation zu Klasse Student zu verdeutlichen/einzubauen

@dataclass
class Student:
    name: str
    matrikelnummer: int
    university: Optional[str] = None
    course_of_study: Optional[str] = None
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

#auch wieder dataclass, da nur ein paar Daten gespeichert werden sollen und sonst fast keine Methoden gebraucht werden
#Optional eingesetzt, da sonst None nicht funktioniert. Erklärung:
#Normale Klasse mit None-Werten         Nein, Python erlaubt None standardmäßig.
#dataclass mit None als Standardwert	Ja, weil Typ-annotationen in dataclass geprüft werden.

class Lernstatistik:
    def __init__(self, student_name):
        self._current_streak = 0
        self._best_streak = 0
        student_name.learning_streaks = self

    def __str__(self):
        return f"Calculated current streak: {self.current_streak}\nCalculated best streak: {self._best_streak}"

    def calculating_streak(self, gelernt: bool):
        """Berechnet die dauer des aktuellen Streaks, falls der Streak unterbrochen wird, wird der Counter wieder auf 0 gesetzt.
        Ist der aktuelle Streak größer als der beste Streak, wird der beste Streak entsprechend aktualisiert"""
        #Achtung! Variable "gelernt" noch nicht definiert!
        if gelernt == True:
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

#Ich werde Wahrscheinlich noch eine Klasse brauchen für die GUI bzw. für den Kalender auf dem ich auswählen kann an welchen Tagen ich gelernt habe und wann nicht.
#Aus dieser JSON Datei lese ich dann meine daten aus dem Dictionary ab. Das Dictionary wird folgendes Format haben KEY:Timestamp VALUE:True oder False

#Altenativer Plan! Nachteil, ich muss jeden Tag in das Dashboard rein schauen und angeben, ob ich gelernt habe oder nicht. If gelernt then lerncounter +1, wenn nicht, dann wird lerncounter
#wieder auf null gesetzt. Dabei wird der Counter noch verglichen mit best_streak und ersetzt diesen, falls er größer ist als best_streak

#Verwendung von property um current_streak und best_streak zu privatisieren bzw vor direktem Zugriff zu schützen, aber trotzdem die Möglichkeit schnell darauf zuzugreifen
#und es sieht aus wie ein direkter zugriff
#umbenennung von winning_streak zu best_streak für besseres verständlichkeit

class CourseOfStudy:
    def __init__(self, name, num_semesters, ects_points):
        self.name = name
        self.num_semesters = num_semesters
        self.ects_points = ects_points
        self.semesters = []
        self.students = []

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

#Lieber dataclass verwenden da nicht komplex und nur zwei Methoden?
#arg status umbenannt in passed für bessere verständnis

class charts:
    def __init__(self, chart_type="line", y_values=None, average_grade=0, pie_chart_values=None, remaining_weeks_semester=None):
        self.chart_type = chart_type
        self.x_values = 10
        self.y_values = y_values
        self.chart_color = "#003B00"
        self.chart_title = ""
        self.y_ticks = range(0, 7)
        self.avg_grade_line = False
        self.average_grade = average_grade
        self.pie_chart_values = pie_chart_values
        self.total_weeks_semester = 26
        self.remaining_weeks_semester = remaining_weeks_semester

        if self.chart_type == "line":
            fig, ax = plt.subplots(figsize=(10, 5), layout="constrained")
            ax.plot(self.x_values, self.y_values, self.chart_color)
            #Background invisible
            fig.patch.set_alpha(0)
            ax.set_facecolor("none")
            #Right Axis and Top Axis invisible
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            #Style of Bottom and Left Axis
            ax.spines["bottom"].set_color(self.chart_color)
            ax.spines["left"].set_color(self.chart_color)
            ax.spines["bottom"].set_linewidth(2)
            ax.spines["left"].set_linewidth(2)
            ax.set_xticks(self.x_values)
            ax.set_yticks(self.y_ticks)
            ax.tick_params(axis="both", colors=self.chart_color, labelsize=14, length=10, width=2)
            ax.set_xticklabels([])
            #Chart Title
            ax.set_title(self.chart_title, fontsize=18, color=self.chart_color)
            #Average Grade Line On = True or Off = False
            if self.avg_grade_line == True:
                ax.axhline(self.average_grade, color="blue", linestyle="--", linewidth=2)

        if self.chart_type == "pie":
            labels = ("Done", "In Progress", "Open")
            sizes = self.pie_chart_values
            fig, ax = plt.subplots()
            #Background invisible
            fig.patch.set_alpha(0)
            ax.set_facecolor("none")

            ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=["#008F11", "#92e5a1", "#A5FFFF"], pctdistance=0.4,
                   labeldistance=0.6, explode=(0.1, 0, 0), shadow=True, startangle=90, radius=1.2, textprops={'fontsize': 8})

        if self.chart_type == "pie70":
            fig, ax = plt.subplots()
            # Total weeks = 70% from Pie-Charts
            remaining_converting_for_pie_chart = 70 / 26 * self.remaining_weeks_semester
            passed_converting_for_pie_chart = 70 - remaining_converting_for_pie_chart


            size = 0.3
            #values outer ring - [invisible 15%, red-range, yellow-range, green-range, invisible 15%]
            vals_o = [15, 3, 10, 57, 15]
            #values inner ring - [invisible 15%, green-range, grey-range, invisible 15%]
            #green-range + grey-range := 70%!
            vals_i = [15, remaining_converting_for_pie_chart, passed_converting_for_pie_chart, 15]


            #Specs and Style outer ring
            ax.pie(vals_o, radius=1, colors=["none", "red", "yellow", "#003B00", "none"],
                   wedgeprops=dict(width=0.05, edgecolor='none'),startangle=270)
            #Specs and Style inner ring
            ax.pie(vals_i, radius=0.92, colors=["none", "0.2", "#003B00", "none"],
                   wedgeprops=dict(width=size, edgecolor='none'),startangle=270)
            #Background invisible
            fig.patch.set_alpha(0)
            ax.set_facecolor("none")

            ax.set(aspect="equal")


#class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
#    def __init__(self, *args, obj=None, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.setupUi(self)
#Das wird die Klasse für die in QT Creator erstelle GUI