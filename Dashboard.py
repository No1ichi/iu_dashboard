import sys
import os
from datetime import date

from PyQt6.QtWidgets import QApplication

from src.DashboardClasses import learning_tracker
from src.GUIClasses import MainWindow
from src.DataManagingClasses import user_data, exam_data, study_data, menu_data, get_data_path

# Default Werte der JSON-Dateien erstellen, falls Datei noch leer
def initialize_defaults():
    """Initialisiert die Default-Werte für Study-Data File, User-Data File und Exam-Data File,
    falls sie noch nicht vorhanden sind."""
    # Initialisiere Default-Werte für studydata JSON-File
    if os.path.exists(get_data_path("studydata.json")):
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
    if os.path.exists(get_data_path("userdata.json")):
        user_data_file = user_data.load()
        if "University" not in user_data_file:
            user_data.update("University", ["Name", "Street", "Town"])
        if "Student Name" not in user_data_file:
            user_data.update("Student Name", "")
        if "Student Number" not in user_data_file:
            user_data.update("Student Number", "")
        if "Course of Study" not in user_data_file:
            user_data.update("Course of Study", "")
        if "Learning Status" not in user_data_file:
            user_data.update("Learning Status", False)
        if "Learning Status Button" not in user_data_file:
            user_data.update("Learning Status Button", False)
        if "Learning Status Date" not in user_data_file:
            user_data.update("Learning Status Date", "")
        if "Current Streak" not in user_data_file:
            user_data.update("Current Streak", 0)
        if "Best Streak" not in user_data_file:
            user_data.update("Best Streak", 0)
        else:
            pass

    # Initialisiere Default-Werte für examdata JSON-File
    if os.path.exists(get_data_path("examdata.json")):
        exam_data_file = exam_data.load()
        if exam_data_file == {}:
            exam_data.update("", ["Status", 0])
        else:
            pass

# Resetten des LearningTracker Button-Status bei neuem Tag
learning_track_data = user_data.load()
lt_date = learning_track_data.get("Learning Status Date")
today = str(date.today())
if lt_date != today:
    user_data.update("Learning Status", False)
    user_data.update("Learning Status Button", False)
    learning_tracker.load_data(user_data)
else:
    learning_tracker.load_data(user_data)


initialize_defaults()

app = QApplication(sys.argv)
window = MainWindow(user_data, study_data, exam_data, menu_data)
window.show()
app.exec()
