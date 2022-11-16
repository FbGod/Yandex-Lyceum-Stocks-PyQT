import sys

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QPushButton, QTableWidget, QWidget, QLineEdit, QTabWidget, QGridLayout, \
    QTableWidgetItem, QFormLayout, QApplication

import Currency.currency_logic
import Deal.deal_logic
import Place.place_logic
import Type.type_logic
import Stock_Create.stock
import database
from Stock_Create import stock

deal_column_names = ['id', 'Тип', 'Место', 'Валюта', 'Номер сделки', 'Тикер', 'Номер поручения', 'Количество',
                     'Цена акции', 'Общая сумма', 'Код трейдера', 'Коммисия торговой площадки']
deal_place_currency_names = ['id', 'Полное название', 'Короткое название']
deal_type_column = ['id', 'Тип']


class MainWindow(QMainWindow, Currency.currency_logic.ActionCurrency,
                 Place.place_logic.ActionPlace, Type.type_logic.ActionType,
                 Stock_Create.stock.ActionStock, Deal.deal_logic.ActionDeal):

    """MAIN WINDOW + DEAL"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.edit_currency = QPushButton("Изменить")
        self.delete_currency = QPushButton("Удалить")
        self.add_currency = QPushButton("Добавить")
        self.currency_table = QTableWidget()

        self.edit_deal_type = QPushButton("Изменить")
        self.delete_deal_type = QPushButton("Удалить")
        self.add_deal_type = QPushButton("Добавить")
        self.type_table = QTableWidget()

        self.edit_deal_place = QPushButton("Изменить")
        self.delete_deal_place = QPushButton("Удалить")
        self.add_deal_place = QPushButton("Добавить")
        self.place_table = QTableWidget()

        self.setWindowTitle('Stocks Saver')

        self.currency_tab = QWidget()
        self.places_tab = QWidget()
        self.deal_types_tab = QWidget()
        self.central_widget = QWidget()

        self.view = QWebEngineView()

        self.setCentralWidget(self.central_widget)

        self.db_space = QTableWidget()
        self.add_to_db_space = QPushButton("Добавить")
        self.add_to_db_space.clicked.connect(self.add_deal)
        self.delete_from_db_space = QPushButton("Удалить")
        self.delete_from_db_space.clicked.connect(self.delete_deal)
        self.update_db_space = QPushButton("Изменить")
        self.update_db_space.clicked.connect(self.update_deal)

        self.enter_ticker = QLineEdit(str(stock.stock_name[0]))
        self.enter_ticker_btn = QPushButton('Показать')
        self.enter_ticker_btn.clicked.connect(self.retry_stock_chart)

        self.setup_tables_space = QTabWidget()

        self.setup_tables_space.addTab(self.currency_tab, "Таблица валют")
        self.setup_tables_space.addTab(self.places_tab, "Таблица мест сделки")
        self.setup_tables_space.addTab(self.deal_types_tab, "Таблица типов сделки")

        self.lay = QGridLayout(self.central_widget)
        self.lay.addWidget(self.db_space, 0, 0, 10, 1)
        self.lay.addWidget(self.add_to_db_space, 10, 0)
        self.lay.addWidget(self.update_db_space, 11, 0)
        self.lay.addWidget(self.delete_from_db_space, 12, 0)
        self.lay.addWidget(self.view, 0, 1, 5, 1)
        self.lay.addWidget(self.enter_ticker, 5, 1)
        self.lay.addWidget(self.enter_ticker_btn, 6, 1)
        self.lay.addWidget(self.setup_tables_space, 7, 1, 6, 1)

        self.currency_tab_ui()
        self.places_tab_ui()
        self.deal_types_tab_ui()

        self.create_line_chart(stock.stock_name)
        self.showMaximized()

        self.update_deal_table()

    """UPDATE DEAL TABLE"""

    def update_deal_table(self):
        items = database.connect_to_deal('print')
        self.db_space.setColumnCount(12)
        self.db_space.setHorizontalHeaderLabels(deal_column_names)
        self.db_space.setRowCount(0)
        for i, row in enumerate(items):
            self.db_space.setRowCount(
                self.db_space.rowCount() + 1)
            for j, elem in enumerate(row):
                self.db_space.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    """GET STOCK CHART"""

    def retry_stock_chart(self):
        stock_name = [self.enter_ticker.text()]
        self.create_line_chart(stock_name)

    """CURRENCY"""

    def currency_tab_ui(self):
        layout = QFormLayout()
        items = database.connect_to_currency('print')
        self.currency_table.setColumnCount(3)
        self.currency_table.setRowCount(0)
        self.currency_table.setHorizontalHeaderLabels(deal_place_currency_names)
        for i, row in enumerate(items):
            self.currency_table.setRowCount(
                self.currency_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.currency_table.setItem(
                    i, j, QTableWidgetItem(str(elem)))

        layout.addRow(self.add_currency)
        layout.addRow(self.edit_currency)
        layout.addRow(self.delete_currency)
        layout.addRow(self.currency_table)
        self.currency_tab.setLayout(layout)
        self.add_currency.clicked.connect(self.currency_btn_add)
        self.delete_currency.clicked.connect(self.currency_btn_del)
        self.edit_currency.clicked.connect(self.currency_btn_update)

    """UPDATE CURRENCY TABLE"""

    def update_table_currency(self):
        items = database.connect_to_currency('print')
        self.currency_table.setColumnCount(3)
        self.currency_table.setRowCount(0)
        self.currency_table.setHorizontalHeaderLabels(deal_place_currency_names)
        for i, row in enumerate(items):
            self.currency_table.setRowCount(
                self.currency_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.currency_table.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    """DEAL PLACE"""

    def places_tab_ui(self):
        layout = QFormLayout()
        items = database.connect_to_deal_place('print')
        self.place_table.setColumnCount(3)
        self.place_table.setRowCount(0)
        self.place_table.setHorizontalHeaderLabels(deal_place_currency_names)
        for i, row in enumerate(items):
            self.place_table.setRowCount(
                self.place_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.place_table.setItem(
                    i, j, QTableWidgetItem(str(elem)))

        layout.addRow(self.add_deal_place)
        layout.addRow(self.edit_deal_place)
        layout.addRow(self.delete_deal_place)
        layout.addRow(self.place_table)
        self.places_tab.setLayout(layout)
        self.add_deal_place.clicked.connect(self.places_btn_add)
        self.edit_deal_place.clicked.connect(self.place_btn_update)
        self.delete_deal_place.clicked.connect(self.place_btn_del)

    """UPDATE DEAL PLACE TABLE"""

    def update_table_places(self):
        items = database.connect_to_deal_place('print')
        self.place_table.setColumnCount(3)
        self.place_table.setRowCount(0)
        self.place_table.setHorizontalHeaderLabels(deal_place_currency_names)
        for i, row in enumerate(items):
            self.place_table.setRowCount(
                self.place_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.place_table.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    """DEAL TYPE"""

    def deal_types_tab_ui(self):
        layout = QFormLayout()
        items = database.connect_to_deal_type('print')
        self.type_table.setColumnCount(2)
        self.type_table.setRowCount(0)
        self.type_table.setHorizontalHeaderLabels(deal_type_column)
        for i, row in enumerate(items):
            self.type_table.setRowCount(
                self.type_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.type_table.setItem(
                    i, j, QTableWidgetItem(str(elem)))

        layout.addRow(self.add_deal_type)
        layout.addRow(self.edit_deal_type)
        layout.addRow(self.delete_deal_type)
        layout.addRow(self.type_table)
        self.deal_types_tab.setLayout(layout)
        self.add_deal_type.clicked.connect(self.type_btn_add)
        self.delete_deal_type.clicked.connect(self.type_btn_del)
        self.edit_deal_type.clicked.connect(self.type_btn_update)

    """UPDATE DEAL TYPE TABLE"""

    def update_table_types(self):
        items = database.connect_to_deal_type('print')
        self.type_table.setColumnCount(2)
        self.type_table.setRowCount(0)
        self.type_table.setHorizontalHeaderLabels(deal_type_column)
        for i, row in enumerate(items):
            self.type_table.setRowCount(
                self.type_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.type_table.setItem(
                    i, j, QTableWidgetItem(str(elem)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
