from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import QTimer, Qt
import numpy as np

class GradientPlot(QWidget):
    def __init__(self, measure_function, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.measure_function = measure_function
        self.values = np.zeros((8, 8))
        self.legend = QLabel(self)
        self.legend.setGeometry(700, 20, 100, 400)
        self.legend.setStyleSheet("font-size: 12px")
        self.legend_values = np.linspace(0, 1, 11)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_values)
        self.timer.start(500)

    def paintEvent(self, event):
        painter = QPainter(self)
        w, h = self.width(), self.height()
        cell_w, cell_h = w // 8, h // 8
        for i in range(8):
            for j in range(8):
                value = self.values[i, j]
                color = self.get_color(value)
                painter.setBrush(QBrush(QColor(*color)))
                painter.setPen(QPen(Qt.NoPen))
                painter.drawRect(i * cell_w, j * cell_h, cell_w, cell_h)

        for i, value in enumerate(self.legend_values):
            color = self.get_color(value)
            painter.setBrush(QBrush(QColor(*color)))
            painter.setPen(QPen(Qt.NoPen))
            painter.drawRect(700, 40 + i * 30, 30, 30)
            painter.setPen(QPen(Qt.black))
            painter.drawText(740, 60 + i * 30, "{:.2f}".format(value))

    def get_color(self, value):
        r = int(value * 255)
        g = int((1-value) * 255)
        b = 0
        return (r, g, b)

    def update_values(self):
        for i in range(8):
            for j in range(8):
                self.values[i, j] = self.measure_function()
        self.update()

class LinePlot(QWidget):
    def __init__(self, measure_function, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.measure_function = measure_function
        self.values = []

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_values)
        self.timer.start(500)

    def paintEvent(self, event):
        painter = QPainter(self)
        w, h = self.width(), self.height()
        painter.setBrush(QBrush(Qt.white))
        painter.setPen(QPen(Qt.black, 2))
        painter.drawRect(0, 0, w-1, h-1)

        if len(self.values) > 1:
            painter.setPen(QPen(Qt.blue, 2))
            x_scale = (w-20) / (len(self.values)-1)
            y_scale = (h-20) / 2
            last_x, last_y = None, None
            for i, value in enumerate(self.values):
                x = 10 + i * x_scale
                y = h - 10 - value * y_scale
                if last_x is not None:
                    painter.drawLine(last_x, last_y, x, y)
                last_x, last_y = x, y

    def update_values(self):
        self.values.append(self.measure_function())
        if len(self.values) > (self.width() - 20):
            self.values.pop(0)
        self.update()

class MainWindow(QMainWindow):
    def __init__(self, measure_function, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.measure_function = measure_function
        self.setWindowTitle("Real-time Plotting")
        self.setGeometry(100, 100, 1000, 1000)

        self.gradient_plot = GradientPlot(measure_function, self)
        self.gradient_plot.setGeometry(0, 0, 200, 200)

        self.line_plot1 = LinePlot(measure_function, self)
        self.line_plot1.setGeometry(50, 750, 400, 200)

        self.line_plot2 = LinePlot(measure_function, self)
        self.line_plot2.setGeometry(550, 750, 400, 200)

        self.quit_button = QPushButton("Quit", self)
        self.quit_button.setGeometry(50, 950, 150, 50)
        self.quit_button.clicked.connect(self.quit)

        self.function_button = QPushButton("Function", self)
        self.function_button.setGeometry(250, 950, 150, 50)
        # self.function_button.clicked.connect(self.measure_function)

        self.show()

    def quit(self):
        QApplication.quit()

def measure():
    return np.random.randint(0,100)

if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow(measure)
    app.exec_()

