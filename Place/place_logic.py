from PyQt5.QtWidgets import QLineEdit, QDialog, QMessageBox, QLabel, QPushButton, QFormLayout

import database


class ActionPlace:
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
        database.connect_to_deal_place('add', long, short)
        self.add_place_diag.close()
        self.update_table_places()

    def place_btn_del(self):
        rows = list(set([i.row() for i in self.place_table.selectedItems()]))
        ids = [self.place_table.item(i, 0).text() for i in rows]

        button = QMessageBox.question(self, "Удаление", "Удалить из таблицы поле с id = " + ",".join(map(str, ids)) +
                                      '? Вместе с ней будут удалены соответствующие поля из таблицы Deal!')

        if button == QMessageBox.Yes:
            database.connect_to_deal_place('delete', ids)
            self.update_table_places()

        else:
            print("No!")
        self.update_deal_table()

    def place_btn_update(self):
        try:
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
        except Exception as e:
            print('Ошибка при обновлении: ', e)

    def update_place(self):
        index = self.place_table.currentIndex()
        new_index = self.place_table.model().index(index.row(), 0)
        index_to_upd = self.place_table.model().data(new_index)
        print(index_to_upd)
        new = [self.add_place_diag_place_long.text(), self.add_place_diag_place_sort.text()]
        database.connect_to_deal_place('update', index_to_upd, new)
        self.add_place_diag.close()
        self.update_table_places()
        self.update_deal_table()
