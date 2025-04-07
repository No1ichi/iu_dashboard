import sys
from PyQt6.QtWidgets import QMainWindow,QApplication, QWidget

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

matplotlib.use("QtAgg")



class charts(FigureCanvasQTAgg):
    def __init__(
        self,
        chart_type="line",
        y_values=None,
        average_grade=0,
        pie_chart_values=None,
        remaining_weeks_semester=None,
        parent: QWidget = None
    ):
        self.fig = Figure(figsize=(10, 5), dpi=100)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)

        # Attribute
        self.chart_type = chart_type
        self.y_values = y_values or []
        self.x_values = list(range(len(self.y_values)))
        self.chart_color = "#003B00"
        self.chart_title = ""
        self.y_ticks = range(0, 7)
        self.avg_grade_line = False
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
        if self.avg_grade_line:
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
        remaining = self.remaining_weeks_semester or 0
        remaining_converted = 70 / self.total_weeks_semester * remaining
        passed_converted = 70 - remaining_converted

        size = 0.3
        vals_o = [15, 3, 10, 57, 15]
        vals_i = [15, remaining_converted, passed_converted, 15]

        ax.pie(
            vals_o,
            radius=1,
            colors=["none", "red", "yellow", "#003B00", "none"],
            wedgeprops=dict(width=0.05, edgecolor='none'),
            startangle=270
        )

        ax.pie(
            vals_i,
            radius=0.92,
            colors=["none", "0.2", "#003B00", "none"],
            wedgeprops=dict(width=size, edgecolor='none'),
            startangle=270
        )

        ax.set(aspect="equal")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        sc = charts("line", [1,2,3])
        self.setCentralWidget(sc)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()