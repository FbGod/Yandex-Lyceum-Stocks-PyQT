from PyQt5.QtWidgets import QMessageBox, QDialog, QLineEdit, QLabel, QFormLayout, QPushButton

import database


class ActionType:
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
        database.connect_to_deal_type('add', [type_from_field])
        self.add_type_diag.close()
        self.update_table_types()

    def type_btn_del(self):
        rows = list(set([i.row() for i in self.type_table.selectedItems()]))
        ids = [self.type_table.item(i, 0).text() for i in rows]

        button = QMessageBox.question(self, "Удаление", "Удалить из таблицы поле с id = " + ",".join(map(str, ids)) +
                                      '? Вместе с ней будут удалены соответствующие поля из таблицы Deal!')

        if button == QMessageBox.Yes:
            database.connect_to_deal_type('delete', ids)
            self.update_table_types()

        else:
            print("No!")
        self.update_deal_table()

    def type_btn_update(self):
        try:
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
        except Exception as e:
            print('Ошибка при обновлении: ', e)

    def update_type(self):
        index = self.type_table.currentIndex()
        new_index = self.type_table.model().index(index.row(), 0)
        index_to_upd = self.type_table.model().data(new_index)
        print(index_to_upd)
        new = [self.add_type_diag_type.text()]
        database.connect_to_deal_type('update', index_to_upd, new)
        self.add_type_diag.close()
        self.update_table_types()
        self.update_deal_table()
