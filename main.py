from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QGridLayout, QWidget, QRadioButton, QButtonGroup,QPushButton, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTableView

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QGridLayout()
        self.central_widget.setLayout(self.grid_layout)

        self.setWindowTitle("Віктарына")

        self.main_label = QLabel('ВІКТАРЫНА НА СТАЛІЦЫ СВЕТУ', self)
        self.main_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.main_label.setStyleSheet('font-family: Arial Black; font-size: 16pt')
        self.grid_layout.addWidget(self.main_label, 0, 2)

        self.show_info()

        self.button = QPushButton('Завяршыць тэст', self)
        self.button.setStyleSheet(
            'background-color: green; color: white; font-size: 14pt; font-family: Arial; font-weight: bold')
        self.button.resize(200, 50)
        self.grid_layout.addWidget(self.button, self.counter, 2)

        self.button_exit = QPushButton('Выйсці', self)
        self.button_exit.setStyleSheet(
            'font-size: 14pt; font-family: Arial;')
        self.grid_layout.addWidget(self.button_exit, 0, 0)

        self.button.clicked.connect(self.check_answ)
        self.button_exit.clicked.connect(self.exit_prog)


    def show_info(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('database.db')

        if self.db.open():
            self.query1 = QSqlQuery()
            self.query1.exec_("SELECT id, description FROM Questions")

            self.counter = 1
            self.group_dict = {}

            while self.query1.next():
                self.id = self.query1.value('id')
                self.description = self.query1.value('description')
                self.label = QLabel(f'{self.id}. {self.description}', self)
                self.label.setStyleSheet('font-family: Arial; font-size: 12pt')
                self.grid_layout.addWidget(self.label, self.counter, 0)

                self.query2 = QSqlQuery()
                self.query2.exec_(f"SELECT id, answer, correct FROM Answers WHERE question_id = {self.id}")

                self.counter += 2
                self.counter1 = 0
                self.group = QButtonGroup(self)

                self.answer_dict = {}

                while self.query2.next():

                    self.answer_id = self.query2.value('id')
                    self.answer = self.query2.value('answer')
                    self.correct = self.query2.value('correct')
                    self.answer_label = QRadioButton(f'{self.answer}', self)
                    self.answer_label.setStyleSheet('font-family: Arial; font-size: 12pt; color: blue')
                    self.grid_layout.addWidget(self.answer_label, self.counter - 1, self.counter1)

                    self.group.addButton(self.answer_label)

                    self.counter1 += 1
                    self.answer_dict[self.answer_label] = self.correct
                    self.group_dict[self.id] = self.answer_dict

                self.group.setExclusive(True)
            self.db.close()

        else:
            print("Error")

        print(self.group_dict)
        # print(self.answ_dict)


    def check_answ(self):

        self.sum_corr = 0
        self.que = len(self.group_dict)

        for i in range(1, self.que + 1):

            # скідванне стану кнопак
            for key in self.group_dict[i].keys():
                key.setChecked(False)

            counter = 0
            for self.key, self.value in self.group_dict[i].items():
                if self.key.isChecked():
                    self.sum_corr += self.value
                if self.key.isChecked():
                    counter += 1
                if counter == 0:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Памылка")
                    msg.setInformativeText(f"Вы не выбралі адказу на пытанне {i}.")
                    msg.setWindowTitle("Памылка")
                    msg.exec_()
                    return

        print(f"Вы выбралі {self.sum_corr} правільных адказаў")
        self.mark = int(self.sum_corr/self.que * 10)
        print(f"Mark {self.mark}")

        self.show_results(self.sum_corr, self.mark)

    def show_results(self, corr, mark):

        self.corr_label = QLabel(f'Колькасць правільных адказаў: {corr}', self)
        self.corr_label.setStyleSheet('font-family: Arial Black; font-size: 14pt')
        self.grid_layout.addWidget(self.corr_label, 1, 4)

        self.mark_label = QLabel(str(mark), self)
        self.mark_label.setStyleSheet('font-family: Arial Black; font-size: 40pt; color: red')
        self.grid_layout.addWidget(self.mark_label, 0, 4)

        self.button.hide()

    def exit_prog(self):
        sys.exit()


def quiz_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    quiz_app()