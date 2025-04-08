from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow
from matplotlib.figure import Figure

from MainWindow import Ui_MainWindow
from DashboardClasses import charts

#Größer AVG-Grade Line-Chart - Daten sind nur zu Testzwecken
line_chart_avg_grade_big = charts("line", [1,2,2,1.4,5,1.3,2.3,4,2.3,3.3])
line_chart_avg_grade_big.fig.subplots_adjust(left=0.06, right=0.99, top=0.95, bottom=0.05)
#Course Status Pie-Chart - Daten sind nur zu Testzwecken
pie_chart_course_status = charts("pie", pie_chart_values=[5,5,40])
pie_chart_course_status.fig.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.01)
#Kleiner AVG-Grade Line-Chart - Daten sind nur zu Testzwecken
line_chart_avg_grade_small = charts("line", [1,2,2,1.4,5,1.3,2.3,4,2.3,3.3])
line_chart_avg_grade_small.fig = Figure(figsize=(1, 0.5), dpi=100)
line_chart_avg_grade_small.fig.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.05)
#Remaining Weeks Pie Chart - Daten sind nur zu Testzwecken
remaining_weeks_pie_chart = charts("pie70", remaining_weeks_semester=22)
remaining_weeks_pie_chart.fig.subplots_adjust(left=0.001, right=0.999, top=0.95, bottom=0.05)


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

        #Layout für MPL-Insert AVG-Grades Line Chart Small
        layout = QtWidgets.QVBoxLayout(self.frame_avg_grades_chart_small)
        self.frame_avg_grades_chart_small.setLayout(layout)
        #Einbetten von MPL-Widget in frame_3
        layout.addWidget(line_chart_avg_grade_small)

        #Layout für MPL-Insert Weeks Left Pie-Chart
        layout = QtWidgets.QVBoxLayout(self.frame_3)
        self.frame_3.setLayout(layout)
        #Einbetten von MPL-Widget in frame_3
        layout.addWidget(remaining_weeks_pie_chart)



