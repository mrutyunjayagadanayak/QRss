import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from ui.mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.addButton.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        print("button clicked")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window =MainWindow()
    window.show()

    sys.exit(app.exec())


