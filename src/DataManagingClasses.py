import json
import os
import sys
from datetime import datetime

def get_base_path():
    if getattr(sys, 'frozen', False):
        # im One-Dir-Modus
        return os.path.dirname(sys.executable)
    else:
        # im Entwicklungs-Modus
        return os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir)
        )

def get_data_path(filename):
    base = get_base_path()
    data_dir = os.path.join(base, "data")
    # stell sicher, dass data_dir existiert
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, filename)

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
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            default_data = {} if self.default_type == "dict" else []
            self.save(default_data)
            print(f"Initialisiere neue JSON-Datei: {self.filename}")
        else:
            pass

    def save(self, data):
        """Speichert Daten in die JSON-Datei."""
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except IOError as error:
            print(f"Fehler beim schreiben der Datei: {error}")

    def load(self):
        """Lädt die JSON-Daten aus der Datei und gibt sie zurück."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print("File not Fount. New File will be created")
            self.new_file()
            return {} if self.default_type == "dict" else []
        except json.JSONDecodeError:
            print("File-Decoding Error. New File will be created")
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

class InputHandler:
    """Prüft und validiert Benutzereingaben."""

    @staticmethod
    def validate_text(text):
        """Überprüft, ob ein Text nicht leer ist."""
        return bool(text.strip())

    @staticmethod
    def validate_number(value):
        """Überprüft, ob die Eingabe eine gültige Zahl ist."""
        try:
            float(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_grade(value):
        """Überprüft, ob die Eingabe eine gültige Note ist in Range 1-6"""
        try:
            grade = float(value)
            return 1.0 <= grade <= 6.0
        except ValueError:
            return False

    @staticmethod
    def validate_date(date_text):
        """Überprüft, ob die Datums-Eingabe in der Vergangenheit liegt und liefert False wenn nicht."""
        if datetime.strptime(date_text, "%Y-%m-%d") <= datetime.now():
            return True
        else:
            return False

#JSON-Files zur Datenspeicherung
user_data = JSONFile(get_data_path("userdata.json"))
study_data = JSONFile(get_data_path("studydata.json"))
exam_data = JSONFile(get_data_path("examdata.json"))
menu_data = JSONFile(get_data_path("menu_data.json"))

input_handler = InputHandler()