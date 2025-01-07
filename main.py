import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

from helpers.datastore import DataStore
from helpers.url_validator import url_validator
from ui.mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Setup menu items
        self.ui.action_quit.triggered.connect(QCoreApplication.quit)
        self.ui.action_about.triggered.connect(self.on_about_clicked)

        self.ui.add_button.clicked.connect(self.on_add_button_clicked)
        self.ui.remove_button.clicked.connect(self.on_remove_button_clicked)

        self.ui.title_list.itemClicked.connect(self.on_title_selected)
        self.ui.items_list.itemClicked.connect(self.on_item_selected)

        self.data_store = DataStore()


    def on_add_button_clicked(self):
        url = self.ui.feed_line_edit.text()
        if url_validator(url):
            self.ui.title_list.addItem(self.data_store.add_to_feed(url))
            self.ui.feed_line_edit.clear()
        else:
            QMessageBox().warning(self,"Invalid FEED","Entered feed URL is incorrect, Please enter a valid URL")



    def on_remove_button_clicked(self):
        selected_feed = self.ui.title_list.currentItem()

        self.data_store.remove_feed(selected_feed.text())
        self.ui.title_list.takeItem(self.ui.title_list.row(selected_feed))
        self.ui.items_list.clear()
        self.ui.item_browser.clear()


    def on_about_clicked(self):
        msgbox = QMessageBox()
        msgbox.setText("This is a free RSS reader made using pyside6 and python3")
        msgbox.exec()

    def on_title_selected(self):
        title = self.ui.title_list.currentItem().text()

        title_items = self.data_store.get_title_dict(title)

        self.ui.items_list.clear()

        if len(title_items) != 0:
            for item in title_items:
                self.ui.items_list.addItem(item['title'])

    def on_item_selected(self):
        item_details = self.data_store.get_item_text(
            self.ui.title_list.currentItem().text(),
            self.ui.items_list.currentItem().text())

        if item_details != "":
            self.ui.item_browser.setText(item_details)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window =MainWindow()
    window.show()

    sys.exit(app.exec())


