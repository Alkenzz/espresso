import sys
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QHeaderView, QFileDialog
from PyQt5 import uic
HEADERS = ['Номер', 'Название', 'Обжарка', 'Помолка', 'Вкус', 'Цена, руб.', 'Объем, г']


class Espresso(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        database = QFileDialog.getOpenFileName(
            self, 'Выберите базу данных с кофе', '', 'База данных (*.sqlite);;Все файлы(*)')[0]
        self.connection = sqlite3.connect(database)
        self.tableWidget.setColumnCount(len(HEADERS))
        self.tableWidget.setHorizontalHeaderLabels(HEADERS)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(HEADERS.index('Вкус'), QHeaderView.Stretch)
        self.load_base()

    def load_base(self):
        cursor = self.connection.cursor()
        result = cursor.execute(
            """SELECT coffee.id, coffee.title, roasts.title, coffee.ground,
            coffee.taste, coffee.price, coffee.pack
            FROM coffee JOIN roasts ON coffee.roast == roasts.id""").fetchall()
        self.tableWidget.setRowCount(len(result))
        for (i, row) in enumerate(result):
            for (j, elem) in enumerate(row):
                if j == HEADERS.index('Помолка'):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(bool(elem))))
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Espresso()
    ex.show()
    sys.exit(app.exec_())