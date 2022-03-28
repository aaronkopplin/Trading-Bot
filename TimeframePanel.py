import csv
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import date, timedelta
from datetime import datetime
from Chart import Chart
from Strategy import Account, Trade
import StyleInfo


class TimeframePanel(QtWidgets.QWidget):
    def __init__(self, chart: Chart):
        super().__init__()
        self.chart = chart

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.panel = QWidget()
        self.layout.addWidget(self.panel)
        self.panel.setStyleSheet(f"background-color: {StyleInfo.panel_color}; "
                                 f"color: white;"
                                 f"font-size: {StyleInfo.font_size}pt;")

        self.panel_layout = QHBoxLayout()
        self.panel_layout.setContentsMargins(0, 0, 0, 0)
        self.panel.setLayout(self.panel_layout)

        # begin time frame
        self.begin_timeframe = QDateTimeEdit()
        self.begin_timeframe.setDateTime(QDateTime(date.today() - timedelta(7)))
        self.panel_layout.addWidget(self.begin_timeframe)

        # end time frame
        self.end_timeframe = QDateTimeEdit()
        self.end_timeframe.setDateTime(QDateTime(date.today()))
        self.panel_layout.addWidget(self.end_timeframe)

        #  candle selector
        self.candle_selector = QComboBox()
        self.candle_selector.addItem("1m")
        self.candle_selector.addItem("2m")
        self.candle_selector.addItem("5m")
        self.candle_selector.addItem("15m")
        self.candle_selector.addItem("30m")
        self.candle_selector.addItem("1h")
        self.candle_selector.addItem("1d")
        self.candle_selector.addItem("5d")
        self.candle_selector.addItem("1wk")
        self.panel_layout.addWidget(self.candle_selector)

        self.load_parameters()

        # submit_button button
        self.submit_button = QPushButton("SUBMIT")
        self.submit_button.setStyleSheet(StyleInfo.button_style)
        self.submit_button.clicked.connect(self.run_query)
        self.panel_layout.addWidget(self.submit_button)

    def run_query(self):
        self.chart.run_query(self.begin_timeframe.dateTime(),
                             self.end_timeframe.dateTime(),
                             self.candle_selector.currentText())

    def load_parameters(self):
        data = []
        with open("last_query.csv") as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        parameters = data.pop()
        ticker = parameters[0]
        begin = parameters[1]
        end = parameters[2]
        interval = parameters[3]

        self.begin_timeframe.setDateTime(datetime.strptime(begin, "%Y-%m-%d"))
        self.end_timeframe.setDateTime(datetime.strptime(end, "%Y-%m-%d"))
        self.candle_selector.setCurrentText(interval)