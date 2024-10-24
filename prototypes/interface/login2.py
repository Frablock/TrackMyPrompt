import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from main import Ui_MainWindow  # Generated from Qt Designer


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        label = QLabel('Main App', parent=self)


class LoginWindow(QMainWindow):  # Inherit QMainWindow instead of QWidget
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui = Ui_MainWindow()  # Load the UI generated from Qt Designer
        self.ui.setupUi(self)  # Apply the UI to the current window (LoginWindow)
        self.setWindowTitle('Login')
        self.setWindowIcon(QIcon(''))

        # Connect login button to checkCredential method
        self.ui.sign_in_button.clicked.connect(self.checkCredential)

        self.status = self.ui.status_label  # Label for status messages

        self.connectToDB()

    def connectToDB(self):
        # Connect to an SQLite database
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('users.db')

        if not db.open():
            self.status.setText('Connection failed')
        else:
            self.status.setText('Connected to the database')

    def checkCredential(self):
        username = self.ui.username_lineEdit.text()
        password = self.ui.password_lineEdit.text()

        if not username or not password:
            self.show_message("Error", "Username and password cannot be empty")
            return

        query = QSqlQuery()
        query.prepare('SELECT Password FROM Users WHERE Username=:username')
        query.bindValue(':username', username)
        query.exec()

        if query.first():
            if query.value(0) == password:
                time.sleep(1)
                self.close()
            else:
                self.status.setText('Password is incorrect')
        else:
            self.status.setText('Username is not found')

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    loginWindow = LoginWindow()
    loginWindow.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')
