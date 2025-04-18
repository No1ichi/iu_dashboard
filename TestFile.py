from DataManagingClasses import menu_data, study_data, exam_data

# Nicht Löschen! Alte Course-Klasse:
class Course:
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



