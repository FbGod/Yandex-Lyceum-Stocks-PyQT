import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

from pyecharts.charts import Line
from pyecharts import options as opts

from datetime import datetime
from datetime import timedelta
import pandas_datareader as data_reader
import pandas as pd
import os
import sqlite3

con = sqlite3.connect("database/stocks.db")


def get_stock_data(stocktickers, days):
    start = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    end = (datetime.now()).strftime('%Y-%m-%d')
    stock = []
    for stockticker in stocktickers:
        data = data_reader.DataReader(stockticker, 'yahoo', start, end)
        data['stock_ticker'] = stockticker
        stock.append(data)

    return pd.concat(stock)


def connect_to_deal(request='print'):
    cursor = con.cursor()
    if request == 'print':
        return cursor.execute("""SELECT * FROM Deal""").fetchall()


def connect_to_deal_place(request='print', *args):
    cursor = con.cursor()
    if request == 'print':
        return cursor.execute("""SELECT * FROM DealPlace""").fetchall()
    elif request == 'add':
        cursor.execute("""INSERT INTO DealPlace(PlaceFull,PlaceShort) VALUES (?,?)""", (args[0], args[1]))
        con.commit()
    elif request == 'delete':
        cursor.execute("DELETE FROM DealPlace WHERE id IN (" + ", ".join(
            '?' * len(args[0])) + ")", list(map(int, args[0])))
        con.commit()
    elif request == 'update':
        old = args[0]
        update_list = args[1]
        print(update_list[0], update_list[1], old)
        cursor.execute("UPDATE DealPlace SET PlaceFull = (?), PlaceShort = (?) WHERE id = (?)", (update_list[0], update_list[1], old))
        con.commit()


def connect_to_deal_type(request='print', *args):
    cursor = con.cursor()
    if request == 'print':
        return cursor.execute("""SELECT * FROM DealType""").fetchall()
    elif request == 'add':
        cursor.execute("""INSERT INTO DealType(Type) VALUES (?)""", (args[0]))
        con.commit()
    elif request == 'delete':
        cursor.execute("DELETE FROM DealType WHERE id IN (" + ", ".join(
            '?' * len(args[0])) + ")", list(map(int, args[0])))
        con.commit()
    elif request == 'update':
        old = args[0]
        update_list = args[1]
        print(update_list[0], update_list[1], old)
        cursor.execute("UPDATE DealType SET Type = (?) WHERE id = (?)", (update_list[0], old))
        con.commit()


def connect_to_currency(request='print', *args):
    cursor = con.cursor()
    if request == 'print':
        return cursor.execute("""SELECT * FROM Currency""").fetchall()
    elif request == 'add':
        cursor.execute("""INSERT INTO Currency(CurrencyFull,CurrencyShort) VALUES (?,?)""", (args[0], args[1]))
        con.commit()
    elif request == 'delete':
        cursor.execute("DELETE FROM Currency WHERE id IN (" + ", ".join(
            '?' * len(args[0])) + ")", list(map(int, args[0])))
        con.commit()
    elif request == 'update':
        old = args[0]
        update_list = args[1]
        print(update_list[0], update_list[1], old)
        cursor.execute("UPDATE Currency SET CurrencyFull = (?), CurrencyShort = (?) WHERE id = (?)", (update_list[0], update_list[1], old))
        con.commit()


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.table = QTableWidget()

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

        self.setWindowTitle('Stock Market App')

        self.currency_tab = QWidget()
        self.places_tab = QWidget()
        self.deal_types_tab = QWidget()
        self.central_widget = QWidget()

        self.view = QWebEngineView()

        self.setCentralWidget(self.central_widget)

        self.db_space = QTableWidget()

        self.setup_tables_space = QTabWidget()

        self.setup_tables_space.addTab(self.currency_tab, "Таблица валют")
        self.setup_tables_space.addTab(self.places_tab, "Таблица мест сделки")
        self.setup_tables_space.addTab(self.deal_types_tab, "Таблица типов сделки")

        self.lay = QGridLayout(self.central_widget)
        self.lay.addWidget(self.db_space, 0, 0, 2, 1)
        self.lay.addWidget(self.view, 0, 1)
        self.lay.addWidget(self.setup_tables_space, 1, 1)

        self.lay.setColumnStretch(0, 1)
        self.lay.setColumnStretch(1, 1)

        self.lay.setRowStretch(0, 1)
        self.lay.setRowStretch(1, 1)

        self.currency_tab_ui()
        self.places_tab_ui()
        self.deal_types_tab_ui()

        self.create_line_chart()
        self.showMaximized()

    """ Currency """

    def currency_tab_ui(self):
        layout = QFormLayout()
        items = connect_to_currency('print')
        self.currency_table.setColumnCount(3)
        self.currency_table.setRowCount(0)
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

    def update_table_currency(self):
        items = connect_to_currency('print')
        self.currency_table.setColumnCount(3)
        self.currency_table.setRowCount(0)
        for i, row in enumerate(items):
            self.currency_table.setRowCount(
                self.currency_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.currency_table.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def currency_btn_add(self):
        self.add_currency_diag = QDialog()
        self.add_currency_diag_currency_long = QLineEdit()
        self.add_currency_diag_currency_sort = QLineEdit()
        self.add_currency_diag.setGeometry(300, 150, 300, 150)
        self.add_currency_diag.setWindowTitle('Добавить валюту')
        long_txt = QLabel('Полное наименование валюты')
        short_txt = QLabel('Короткое наименование валюты')
        layout = QFormLayout()
        layout.addRow(long_txt)
        layout.addRow(self.add_currency_diag_currency_long)
        layout.addRow(short_txt)
        layout.addRow(self.add_currency_diag_currency_sort)
        layout.addRow(button_save_currency := QPushButton('Ok'))
        self.add_currency_diag.setLayout(layout)
        button_save_currency.clicked.connect(self.save_currency)
        self.add_currency_diag.show()
        self.add_currency_diag.exec_()

    def save_currency(self):
        long = self.add_currency_diag_currency_long.text()
        short = self.add_currency_diag_currency_sort.text()
        connect_to_currency('add', long, short)
        self.update_table_currency()
        self.add_currency_diag.close()

    def currency_btn_del(self):
        rows = list(set([i.row() for i in self.currency_table.selectedItems()]))
        ids = [self.currency_table.item(i, 0).text() for i in rows]

        button = QMessageBox.question(self, "Удаление", "Удалить из таблицы поле с id = " + ",".join(map(str, ids)) +
                                      '? Вместе с ней будут удалены соответствующие поля из таблицы Deal!')

        if button == QMessageBox.Yes:
            connect_to_currency('delete', ids)
            self.update_table_currency()

        else:
            print("No!")

    def currency_btn_update(self):
        self.add_currency_diag = QDialog()
        self.add_currency_diag_currency_long = QLineEdit()
        self.add_currency_diag_currency_sort = QLineEdit()
        self.add_currency_diag.setGeometry(300, 150, 300, 150)
        self.add_currency_diag.setWindowTitle('Изменить валюту')
        long_txt = QLabel('Полное наименование валюты')
        short_txt = QLabel('Короткое наименование валюты')
        layout = QFormLayout()
        layout.addRow(long_txt)
        layout.addRow(self.add_currency_diag_currency_long)
        layout.addRow(short_txt)
        layout.addRow(self.add_currency_diag_currency_sort)
        layout.addRow(button_save_currency := QPushButton('Ok'))
        self.add_currency_diag.setLayout(layout)
        button_save_currency.clicked.connect(self.update_currency)
        self.add_currency_diag.show()
        self.add_currency_diag.exec_()

    def update_currency(self):
        index = self.currency_table.currentIndex()
        new_index = self.currency_table.model().index(index.row(), 0)
        index_to_upd = self.currency_table.model().data(new_index)
        print(index_to_upd)
        new = [self.add_currency_diag_currency_long.text(), self.add_currency_diag_currency_sort.text()]
        connect_to_currency('update', index_to_upd, new)
        self.add_currency_diag.close()
        self.update_table_currency()

    """ Places """

    def places_tab_ui(self):
        layout = QFormLayout()
        items = connect_to_deal_place('print')
        self.place_table.setColumnCount(3)
        self.place_table.setRowCount(0)
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

    def update_table_places(self):
        items = connect_to_deal_place('print')
        self.place_table.setColumnCount(3)
        self.place_table.setRowCount(0)
        for i, row in enumerate(items):
            self.place_table.setRowCount(
                self.place_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.place_table.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def places_btn_add(self):
        self.add_place_diag = QDialog()
        self.add_place_diag_place_long = QLineEdit()
        self.add_place_diag_place_sort = QLineEdit()
        self.add_place_diag.setGeometry(300, 150, 300, 150)
        self.add_place_diag.setWindowTitle('Добавить место')
        long_txt = QLabel('Полное наименование места проведения сделки')
        short_txt = QLabel('Короткое наименование места проведения сделки')
        layout = QFormLayout()
        layout.addRow(long_txt)
        layout.addRow(self.add_place_diag_place_long)
        layout.addRow(short_txt)
        layout.addRow(self.add_place_diag_place_sort)
        layout.addRow(button_save_place := QPushButton('Ok'))
        self.add_place_diag.setLayout(layout)
        button_save_place.clicked.connect(self.save_place)
        self.add_place_diag.show()
        self.add_place_diag.exec_()

    def save_place(self):
        long = self.add_place_diag_place_long.text()
        short = self.add_place_diag_place_sort.text()
        connect_to_deal_place('add', long, short)
        self.add_place_diag.close()
        self.update_table_places()

    def place_btn_del(self):
        rows = list(set([i.row() for i in self.place_table.selectedItems()]))
        ids = [self.place_table.item(i, 0).text() for i in rows]

        button = QMessageBox.question(self, "Удаление", "Удалить из таблицы поле с id = " + ",".join(map(str, ids)) +
                                      '? Вместе с ней будут удалены соответствующие поля из таблицы Deal!')

        if button == QMessageBox.Yes:
            connect_to_deal_place('delete', ids)
            self.update_table_places()

        else:
            print("No!")

    def place_btn_update(self):
        self.add_place_diag = QDialog()
        self.add_place_diag_place_long = QLineEdit()
        self.add_place_diag_place_sort = QLineEdit()
        self.add_place_diag.setGeometry(300, 150, 300, 150)
        self.add_place_diag.setWindowTitle('Добавить место')
        long_txt = QLabel('Полное наименование места проведения сделки')
        short_txt = QLabel('Короткое наименование места проведения сделки')
        layout = QFormLayout()
        layout.addRow(long_txt)
        layout.addRow(self.add_place_diag_place_long)
        layout.addRow(short_txt)
        layout.addRow(self.add_place_diag_place_sort)
        layout.addRow(button_save_place := QPushButton('Ok'))
        self.add_place_diag.setLayout(layout)
        button_save_place.clicked.connect(self.update_place)
        self.add_place_diag.show()
        self.add_place_diag.exec_()

    def update_place(self):
        index = self.place_table.currentIndex()
        new_index = self.place_table.model().index(index.row(), 0)
        index_to_upd = self.place_table.model().data(new_index)
        print(index_to_upd)
        new = [self.add_place_diag_place_long.text(), self.add_place_diag_place_sort.text()]
        connect_to_deal_place('update', index_to_upd, new)
        self.add_place_diag.close()
        self.update_table_places()

    """ Types """

    def deal_types_tab_ui(self):
        layout = QFormLayout()
        items = connect_to_deal_type('print')
        self.type_table.setColumnCount(2)
        self.type_table.setRowCount(0)
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

    def update_table_types(self):
        items = connect_to_deal_type('print')
        self.type_table.setColumnCount(2)
        self.type_table.setRowCount(0)
        for i, row in enumerate(items):
            self.type_table.setRowCount(
                self.type_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.type_table.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def type_btn_add(self):
        self.add_type_diag = QDialog()
        self.add_type_diag_type = QLineEdit()
        self.add_type_diag.setGeometry(300, 75, 300, 75)
        self.add_type_diag.setWindowTitle('Добавить тип сделки')
        txt = QLabel('Тип сделки')
        layout = QFormLayout()
        layout.addRow(txt)
        layout.addRow(self.add_type_diag_type)
        layout.addRow(button_save_type := QPushButton('Ok'))
        self.add_type_diag.setLayout(layout)
        button_save_type.clicked.connect(self.save_type)
        self.add_type_diag.show()
        self.add_type_diag.exec_()

    def save_type(self):
        type_from_field = self.add_type_diag_type.text()
        connect_to_deal_type('add', [type_from_field])
        self.add_type_diag.close()
        self.update_table_types()

    def type_btn_del(self):
        rows = list(set([i.row() for i in self.type_table.selectedItems()]))
        ids = [self.type_table.item(i, 0).text() for i in rows]

        button = QMessageBox.question(self, "Удаление", "Удалить из таблицы поле с id = " + ",".join(map(str, ids)) +
                                      '? Вместе с ней будут удалены соответствующие поля из таблицы Deal!')

        if button == QMessageBox.Yes:
            connect_to_deal_type('delete', ids)
            self.update_table_types()

        else:
            print("No!")

    def type_btn_update(self):
        self.add_type_diag = QDialog()
        self.add_type_diag_type = QLineEdit()
        self.add_type_diag.setGeometry(300, 75, 300, 75)
        self.add_type_diag.setWindowTitle('Добавить тип сделки')
        txt = QLabel('Тип сделки')
        layout = QFormLayout()
        layout.addRow(txt)
        layout.addRow(self.add_type_diag_type)
        layout.addRow(button_save_type := QPushButton('Ok'))
        self.add_type_diag.setLayout(layout)
        button_save_type.clicked.connect(self.update_type)
        self.add_type_diag.show()
        self.add_type_diag.exec_()

    def update_type(self):
        index = self.type_table.currentIndex()
        new_index = self.type_table.model().index(index.row(), 0)
        index_to_upd = self.type_table.model().data(new_index)
        print(index_to_upd)
        new = [self.add_type_diag_type.text()]
        connect_to_deal_type('update', index_to_upd, new)
        self.add_type_diag.close()
        self.update_table_types()

    """ Line chart """

    def create_line_chart(self):
        stock_name = ['GOOGL']
        data = get_stock_data(stock_name, 17)
        stockDate = data.index.tolist()
        open = data['Open'].tolist()
        close = data['Close'].tolist()

        line = (
            Line()
                .add_xaxis(xaxis_data=stockDate)
                .add_yaxis(series_name="Open", y_axis=open, symbol="circle", is_symbol_show=True, is_smooth=True,
                           is_selected=True)
                .add_yaxis(series_name="Close", y_axis=close, symbol="circle", is_symbol_show=True, is_smooth=True,
                           is_selected=True)
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title=stock_name[0]))
        )

        html_file = (os.getcwd() + "\\stockchart.html")
        line.render(path=html_file)
        self.view.load(QUrl.fromLocalFile(html_file))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
