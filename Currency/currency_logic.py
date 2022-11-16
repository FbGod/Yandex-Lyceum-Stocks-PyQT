from PyQt5.QtWidgets import QLabel, QDialog, QLineEdit, QFormLayout, QPushButton, QMessageBox

import database


class ActionCurrency:
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
        database.connect_to_currency('add', long, short)
        self.update_table_currency()
        self.add_currency_diag.close()

    def currency_btn_del(self):
        rows = list(set([i.row() for i in self.currency_table.selectedItems()]))
        ids = [self.currency_table.item(i, 0).text() for i in rows]

        button = QMessageBox.question(self, "Удаление", "Удалить из таблицы поле с id = " + ",".join(map(str, ids)) +
                                      '? Вместе с ней будут удалены соответствующие поля из таблицы Deal!')

        if button == QMessageBox.Yes:
            database.connect_to_currency('delete', ids)
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
        database.connect_to_currency('update', index_to_upd, new)
        self.add_currency_diag.close()
        self.update_table_currency()
        self.update_deal_table()

