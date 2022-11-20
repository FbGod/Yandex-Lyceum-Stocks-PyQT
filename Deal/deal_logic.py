from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QLabel, QPushButton, QMessageBox, QComboBox

import database


class ActionDeal:

    def add_deal(self):
        items_type = database.connect_to_deal_type('print')
        items_place = database.connect_to_deal_place('print')
        items_currency = database.connect_to_currency('print')

        self.add_deal_diag = QDialog()

        self.type_id = QComboBox()
        self.type_id.addItems([str(elem[1]) + ' -> id=' + str(elem[0]) for elem in items_type])

        self.place_id = QComboBox()
        self.place_id.addItems([str(elem[1]) + ' -> id=' + str(elem[0]) for elem in items_place])

        self.currency_id = QComboBox()
        self.currency_id.addItems([str(elem[1]) + ' -> id=' + str(elem[0]) for elem in items_currency])


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
        items_type = database.connect_to_deal_type('print')
        items_place = database.connect_to_deal_place('print')
        items_currency = database.connect_to_currency('print')

        type_id = int(items_type[int(self.type_id.currentIndex())][0])

        place_id = int(items_place[int(self.place_id.currentIndex())][0])
        currency_id = int(items_currency[int(self.currency_id.currentIndex())][0])

        deal_number = self.deal_number.text()
        ticker = self.ticker.text()
        order = self.order.text()
        quantity = int(self.quantity.text())
        price = float(self.price.text())
        trader = self.trader.text()
        comission = float(self.comission.text())

        totalcost = float(price * quantity + price * quantity * comission)

        database.connect_to_deal('add', type_id, place_id, currency_id, deal_number, ticker, order, quantity, price,
                                 totalcost, trader, comission)
        self.add_deal_diag.close()
        self.update_deal_table()

    def delete_deal(self):
        rows = list(set([i.row() for i in self.db_space.selectedItems()]))
        ids = [self.db_space.item(i, 0).text() for i in rows]

        button = QMessageBox.question(self, "Удаление", "Удалить из таблицы поле с id = " + ",".join(map(str, ids)) +
                                      '?')

        if button == QMessageBox.Yes:
            database.connect_to_deal('delete', ids)
            self.update_table_currency()

        else:
            print("No!")
        self.update_deal_table()

    def update_deal(self):
        try:
            items_type = database.connect_to_deal_type('print')
            items_place = database.connect_to_deal_place('print')
            items_currency = database.connect_to_currency('print')

            print(items_type)

            index = self.db_space.currentIndex()
            new_index = self.db_space.model().index(index.row(), 0)
            index_to_upd = self.db_space.model().data(new_index)
            items1 = database.connect_to_deal('dialog', index_to_upd)
            items = items1[0]
            print(items)
            self.add_deal_diag = QDialog()
            self.type_id = QComboBox()
            self.type_id.addItems([str(elem[1]) + ' -> id=' + str(elem[0]) for elem in items_type])
            for elem in items_type:
                if elem[0] == items[1]:
                    self.type_id.setCurrentIndex(items_type.index(elem))

            self.place_id = QComboBox()
            self.place_id.addItems([str(elem[1]) + ' -> id=' + str(elem[0]) for elem in items_place])
            for elem in items_place:
                if elem[0] == items[2]:
                    self.place_id.setCurrentIndex(items_place.index(elem))

            self.currency_id = QComboBox()
            self.currency_id.addItems([str(elem[1]) + ' -> id=' + str(elem[0]) for elem in items_currency])
            for elem in items_currency:
                if elem[0] == items[3]:
                    self.currency_id.setCurrentIndex(items_currency.index(elem))

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
        except Exception as e:
            print('Ошибка при обновлении: ', e)

    def updt_deal(self):
        items_type = database.connect_to_deal_type('print')
        items_place = database.connect_to_deal_place('print')
        items_currency = database.connect_to_currency('print')

        index = self.db_space.currentIndex()
        new_index = self.db_space.model().index(index.row(), 0)
        index_to_upd = self.db_space.model().data(new_index)

        type_id = int(items_type[int(self.type_id.currentIndex())][0])

        place_id = int(items_place[int(self.place_id.currentIndex())][0])
        currency_id = int(items_currency[int(self.currency_id.currentIndex())][0])

        deal_number = self.deal_number.text()
        ticker = self.ticker.text()
        order = self.order.text()
        quantity = int(self.quantity.text())
        price = float(self.price.text())
        trader = self.trader.text()
        comission = float(self.comission.text())

        totalcost = float(price * quantity + price * quantity * comission)

        database.connect_to_deal('update', type_id, place_id, currency_id, deal_number, ticker, order, quantity, price,
                                 totalcost, trader, comission, index_to_upd)
        self.add_deal_diag.close()
        self.update_deal_table()
