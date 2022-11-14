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
stock_name = ['GOOGL']
deal_column_names = ['id', 'Тип', 'Место', 'Валюта', 'Номер сделки', 'Тикер', 'Номер поручения', 'Количество', 'Цена акции', 'Общая сумма', 'Код трейдера', 'Коммисия торговой площадки']
deal_place_currency_names = ['id', 'Полное название', 'Короткое название']
deal_type_column = ['id', 'Тип']


def get_stock_data(stocktickers, days):
    start = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    end = (datetime.now()).strftime('%Y-%m-%d')
    stock = []
    for stockticker in stocktickers:
        data = data_reader.DataReader(stockticker, 'yahoo', start, end)
        data['stock_ticker'] = stockticker
        stock.append(data)

    return pd.concat(stock)


def connect_to_deal(request='print', *args):
    cursor = con.cursor()
    if request == 'print':
        return cursor.execute("""select d.id, dt.Type, dp.PlaceFull, c.CurrencyFull, d.Number, d.Tiker, d.Orderr, d.Quantity, d.Price, d.TotalCost, d.Trader, d.Commision 
    from Deal d 
    join DealType dt on (d.TypeID = dt.id) 
    inner join DealPlace dp on (d.PlaceID = dp.id) 
    inner join Currency c on (c.id = d.CurrencyID);""").fetchall()
    elif request == 'add':
        cursor.execute("""INSERT INTO Deal(TypeID, PlaceID, CurrencyID, Number, Tiker, Orderr, Quantity, Price, TotalCost, Trader, Commision) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                       (args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9], args[10]))
        con.commit()
    elif request == 'update':
        print(args)
        cursor.execute("UPDATE Deal SET TypeID=(?), PlaceID=(?), CurrencyID=(?), Number=(?), Tiker=(?), Orderr=(?), Quantity=(?), Price=(?), TotalCost=(?), Trader=(?), Commision=(?) WHERE id=(?)",
                       (args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9], args[10], int(args[-1])))
        con.commit()
    elif request == 'delete':
        print(args)
        cursor.execute("DELETE FROM Deal WHERE id IN (" + ", ".join(
            '?' * len(args[0])) + ")", list(map(int, args[0])))
        con.commit()
    elif request == 'dialog':
        return cursor.execute("""SELECT * FROM Deal WHERE id = ?""", (args[0],)).fetchall()


def connect_to_deal_place(request='print', *args):
    cursor = con.cursor()
    if request == 'print':
        return cursor.execute("""SELECT * FROM DealPlace""").fetchall()
    elif request == 'add':
        cursor.execute("""INSERT INTO DealPlace(PlaceFull,PlaceShort) VALUES (?,?)""", (args[0], args[1]))
        con.commit()
    elif request == 'delete':

        cursor.execute("DELETE FROM Deal WHERE PlaceID IN (" + ", ".join(
            '?' * len(args[0])) + ")", list(map(int, args[0])))

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
        cursor.execute("DELETE FROM Deal WHERE TypeID IN (" + ", ".join(
            '?' * len(args[0])) + ")", list(map(int, args[0])))

        cursor.execute("DELETE FROM DealType WHERE id IN (" + ", ".join(
            '?' * len(args[0])) + ")", list(map(int, args[0])))
        con.commit()
    elif request == 'update':
        old = args[0]
        update_list = args[1]
        print(args)
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
        cursor.execute("DELETE FROM Deal WHERE CurrencyID IN (" + ", ".join(
            '?' * len(args[0])) + ")", list(map(int, args[0])))

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
        self.add_to_db_space = QPushButton("Добавить")
        self.add_to_db_space.clicked.connect(self.add_deal)
        self.delete_from_db_space = QPushButton("Удалить")
        self.delete_from_db_space.clicked.connect(self.delete_deal)
        self.update_db_space = QPushButton("Изменить")
        self.update_db_space.clicked.connect(self.update_deal)

        self.enter_ticker = QLineEdit(str(stock_name[0]))
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

        self.create_line_chart(stock_name)
        self.showMaximized()

        self.update_deal_table()

    def retry_stock_chart(self):
        stock_name = [self.enter_ticker.text()]
        self.create_line_chart(stock_name)

    def update_deal_table(self):
        items = connect_to_deal('print')
        self.db_space.setColumnCount(12)
        self.db_space.setHorizontalHeaderLabels(deal_column_names)
        self.db_space.setRowCount(0)
        for i, row in enumerate(items):
            self.db_space.setRowCount(
                self.db_space.rowCount() + 1)
            for j, elem in enumerate(row):
                self.db_space.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    """BUTTONS"""

    def add_deal(self):
        self.add_deal_diag = QDialog()
        self.type_id = QLineEdit()
        self.place_id = QLineEdit()
        self.currency_id = QLineEdit()
        self.deal_number = QLineEdit()
        self.ticker = QLineEdit()
        self.order = QLineEdit()
        self.quantity = QLineEdit()
        self.price = QLineEdit()
        self.totalcost = 0
        self.trader = QLineEdit()
        self.comission = QLineEdit()

        self.add_deal_diag.setGeometry(700, 150, 700, 150)
        self.add_deal_diag.setWindowTitle('Информация о сделке')
        layout = QFormLayout()
        layout.addRow(QLabel('id Тип'))
        layout.addRow(self.type_id)

        layout.addRow(QLabel('id Место'))
        layout.addRow(self.place_id)

        layout.addRow(QLabel('id Валюта'))
        layout.addRow(self.currency_id)

        layout.addRow(QLabel('Номер сделки'))
        layout.addRow(self.deal_number)

        layout.addRow(QLabel('Тикер'))
        layout.addRow(self.ticker)

        layout.addRow(QLabel('Номер поручения'))
        layout.addRow(self.order)

        layout.addRow(QLabel('Количество'))
        layout.addRow(self.quantity)

        layout.addRow(QLabel('Цена'))
        layout.addRow(self.price)

        layout.addRow(QLabel('Код трейдера'))
        layout.addRow(self.trader)

        layout.addRow(QLabel('Коммисия торговой площадки'))
        layout.addRow(self.comission)

        layout.addRow(button_save_deal := QPushButton('Ok'))
        self.add_deal_diag.setLayout(layout)
        button_save_deal.clicked.connect(self.save_deal)
        self.add_deal_diag.show()
        self.add_deal_diag.exec_()

    def save_deal(self):
        type_id = int(self.type_id.text())

        place_id = int(self.place_id.text())
        currency_id = int(self.currency_id.text())
        deal_number = self.deal_number.text()
        ticker = self.ticker.text()
        order = self.order.text()
        quantity = int(self.quantity.text())
        price = float(self.price.text())
        trader = self.trader.text()
        comission = float(self.comission.text())

        totalcost = float(price * quantity * comission)

        connect_to_deal('add', type_id, place_id, currency_id, deal_number, ticker, order, quantity, price, totalcost, trader, comission)
        self.add_deal_diag.close()
        self.update_deal_table()

    def delete_deal(self):
        rows = list(set([i.row() for i in self.db_space.selectedItems()]))
        ids = [self.db_space.item(i, 0).text() for i in rows]

        button = QMessageBox.question(self, "Удаление", "Удалить из таблицы поле с id = " + ",".join(map(str, ids)) +
                                      '?')

        if button == QMessageBox.Yes:
            connect_to_deal('delete', ids)
            self.update_table_currency()

        else:
            print("No!")
        self.update_deal_table()

    def update_deal(self):
        index = self.db_space.currentIndex()
        new_index = self.db_space.model().index(index.row(), 0)
        index_to_upd = self.db_space.model().data(new_index)
        items1 = connect_to_deal('dialog', index_to_upd)
        items = items1[0]
        print(items)
        self.add_deal_diag = QDialog()
        self.type_id = QLineEdit()
        self.type_id.setText(str(items[1]))

        self.place_id = QLineEdit()
        self.place_id.setText(str(items[2]))

        self.currency_id = QLineEdit()
        self.currency_id.setText(str(items[3]))

        self.deal_number = QLineEdit()
        self.deal_number.setText(str(items[4]))

        self.ticker = QLineEdit()
        self.ticker.setText(str(items[5]))

        self.order = QLineEdit()
        self.order.setText(str(items[6]))

        self.quantity = QLineEdit()
        self.quantity.setText(str(items[7]))

        self.price = QLineEdit()
        self.price.setText(str(items[8]))

        self.totalcost = 0

        self.trader = QLineEdit()
        self.trader.setText(str(items[10]))

        self.comission = QLineEdit()
        self.comission.setText(str(items[11]))

        self.add_deal_diag.setGeometry(700, 150, 700, 150)
        self.add_deal_diag.setWindowTitle('Информация о сделке')
        layout = QFormLayout()
        layout.addRow(QLabel('id Тип'))
        layout.addRow(self.type_id)

        layout.addRow(QLabel('id Место'))
        layout.addRow(self.place_id)

        layout.addRow(QLabel('id Валюта'))
        layout.addRow(self.currency_id)

        layout.addRow(QLabel('Номер сделки'))
        layout.addRow(self.deal_number)

        layout.addRow(QLabel('Тикер'))
        layout.addRow(self.ticker)

        layout.addRow(QLabel('Номер поручения'))
        layout.addRow(self.order)

        layout.addRow(QLabel('Количество'))
        layout.addRow(self.quantity)

        layout.addRow(QLabel('Цена'))
        layout.addRow(self.price)

        layout.addRow(QLabel('Код трейдера'))
        layout.addRow(self.trader)

        layout.addRow(QLabel('Коммисия торговой площадки'))
        layout.addRow(self.comission)

        layout.addRow(button_save_deal := QPushButton('Ok'))
        self.add_deal_diag.setLayout(layout)
        button_save_deal.clicked.connect(self.updt_deal)
        self.add_deal_diag.show()
        self.add_deal_diag.exec_()

    def updt_deal(self):
        index = self.db_space.currentIndex()
        new_index = self.db_space.model().index(index.row(), 0)
        index_to_upd = self.db_space.model().data(new_index)

        type_id = int(self.type_id.text())

        place_id = int(self.place_id.text())
        currency_id = int(self.currency_id.text())
        deal_number = self.deal_number.text()
        ticker = self.ticker.text()
        order = self.order.text()
        quantity = int(self.quantity.text())
        price = float(self.price.text())
        trader = self.trader.text()
        comission = float(self.comission.text())

        totalcost = float(price * quantity * comission)

        connect_to_deal('update', type_id, place_id, currency_id, deal_number, ticker, order, quantity, price, totalcost, trader, comission, index_to_upd)
        self.add_deal_diag.close()
        self.update_deal_table()


    """ Currency """

    def currency_tab_ui(self):
        layout = QFormLayout()
        items = connect_to_currency('print')
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

    def update_table_currency(self):
        items = connect_to_currency('print')
        self.currency_table.setColumnCount(3)
        self.currency_table.setRowCount(0)
        self.currency_table.setHorizontalHeaderLabels(deal_place_currency_names)
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
        self.update_deal_table()

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
        self.update_deal_table()

    """ Places """

    def places_tab_ui(self):
        layout = QFormLayout()
        items = connect_to_deal_place('print')
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

    def update_table_places(self):
        items = connect_to_deal_place('print')
        self.place_table.setColumnCount(3)
        self.place_table.setRowCount(0)
        self.place_table.setHorizontalHeaderLabels(deal_place_currency_names)
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
        self.update_deal_table()

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
        self.update_deal_table()

    """ Types """

    def deal_types_tab_ui(self):
        layout = QFormLayout()
        items = connect_to_deal_type('print')
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

    def update_table_types(self):
        items = connect_to_deal_type('print')
        self.type_table.setColumnCount(2)
        self.type_table.setRowCount(0)
        self.type_table.setHorizontalHeaderLabels(deal_type_column)
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
        self.update_deal_table()

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
        self.update_deal_table()

    """ Line chart """

    def create_line_chart(self, name):
        stock_name = name
        data = get_stock_data(stock_name, 14)
        stockDate = data.index.tolist()
        open = data['Open'].tolist()
        close = data['Close'].tolist()

        line = (
            Line()
                .add_xaxis(xaxis_data=stockDate)
                .add_yaxis(series_name="Открытие", y_axis=open, symbol="circle", is_symbol_show=True, is_smooth=True,
                           is_selected=True)
                .add_yaxis(series_name="Закрытие", y_axis=close, symbol="circle", is_symbol_show=True, is_smooth=True,
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
