import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from ui.mainwindow import Ui_MainWindow
from PySide6.QtCore import QCoreApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.addButton.clicked.connect(self.on_addbutton_clicked)
        self.ui.removeButton.clicked.connect(self.on_removebutton_clicked)
        self.ui.actionQuit.triggered.connect(QCoreApplication.quit)

    def on_addbutton_clicked(self):
        print("add button clicked")

    def on_removebutton_clicked(self):
        print("Remove button clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window =MainWindow()
    window.show()

    sys.exit(app.exec())


