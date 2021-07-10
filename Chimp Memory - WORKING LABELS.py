import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.lives = 3
        self.level = 1
        self.next_num = 1

        self.setWindowTitle("Monke Game")
        self.setStyleSheet("background-color: black;")
        self.setWindowIcon(QIcon("icon.png"))

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.boxlayout = QVBoxLayout()
        self.centralwidget.setLayout(self.boxlayout)

        self.horizontal_text = QHBoxLayout()

        self.counter_level = QLabel()
        self.counter_level.setText("Current level: " + str(self.level))
        self.counter_level.setFont(QFont('Arial', 20))
        self.counter_level.setStyleSheet("color: white")
        self.horizontal_text.addWidget(self.counter_level)

        self.counter_lives = QLabel()
        self.counter_lives.setText("Current lives: " + str(self.lives))
        self.counter_lives.setFont(QFont('Arial', 20))
        self.counter_lives.setStyleSheet("color: white")
        self.counter_lives.setAlignment(QtCore.Qt.AlignRight)
        self.horizontal_text.addWidget(self.counter_lives)

        self.boxlayout.addLayout(self.horizontal_text)

        self.grid_layout = QGridLayout()
        self.boxlayout.addLayout(self.grid_layout)

        self.lost_msg = QMessageBox()
        self.lost_msg.setWindowTitle("Game Over")
        self.lost_msg.setText("You lost all your 3 lives")
        self.lost_msg.setStandardButtons(QMessageBox.Ok)
        self.lost_msg.setFont(QFont('Arial', 15))
        self.lost_msg.buttonClicked.connect(QtCore.QCoreApplication.instance().quit)

    def create_grid(self):
        for x in range(5):
            for y in range(6):
                self.button = QPushButton()
                self.button.setMinimumSize(100, 100)
                self.button.setStyleSheet("background-color: white")
                self.button.setFont(QFont('Arial', 20))
                self.button.clicked.connect(lambda _, r=y, c=x: self.clicked(r, c))
                self.grid_layout.addWidget(self.button, x, y)
        self.grid_layout.setContentsMargins(20, 20, 20, 20)
        self.grid_layout.setSpacing(20)

    def game_init(self):
        self.hidden = random.sample(range(self.grid_layout.count()), self.grid_layout.count() - self.level)
        self.shown = [x for x in list(range(0, self.grid_layout.count())) if x not in self.hidden]
        random.shuffle(self.shown)

        print(self.hidden)
        print(self.shown)

        for x in self.hidden:
            self.grid_layout.itemAt(x).widget().setStyleSheet("background-color: black;")

        for i in self.shown:
            self.grid_layout.itemAt(i).widget().setText(str(self.shown.index(i) + 1))

    def clicked(self, x, y):
        print(self.grid_layout.itemAtPosition(y, x).widget().text())
        if self.grid_layout.itemAtPosition(y, x).widget().text() == str(self.next_num):
            self.grid_layout.itemAtPosition(y, x).widget().setDisabled(True)
            self.next_num += 1
            if self.next_num == 2:
                for i in self.shown:
                    self.grid_layout.itemAt(i).widget().setStyleSheet("background-color: white; color: white")
            self.grid_layout.itemAtPosition(y, x).widget().setStyleSheet("background-color: black; color:black")

        else:
            self.lives -= 1
            self.counter_lives.setText("Current lives: " + str(self.lives))
            if self.lives <= 0:
                self.lost_msg.exec_()
                sys.exit(app.exec_())

            print("False")

        if (self.next_num - 1) == self.level:
            print("next level")
            self.next_level()

    def next_level(self):
        self.level += 1
        self.counter_level.setText("Current level: " + str(self.level))
        self.next_num = 1
        for i in range(self.grid_layout.count()):
            self.grid_layout.itemAt(i).widget().setDisabled(False)
            self.grid_layout.itemAt(i).widget().setText("")
            self.grid_layout.itemAt(i).widget().setStyleSheet("background-color: white; color: black")
        self.game_init()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.create_grid()
    window.game_init()
    window.show()
    sys.exit(app.exec_())
