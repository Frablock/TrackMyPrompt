import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from login import Ui_MainWindow
from signin import Ui_SignInWindow


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
        self.ui.go_to_signin_button.clicked.connect(self.go_to_signin)  # Assuming button to navigate to sign-in window

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
        username = self.ui.usernameEdit.text()
        password = self.ui.passwordEdit.text()

        if not username or not password:
            self.show_message("Error", "Username and password cannot be empty")
            return

        query = QSqlQuery()
        query.prepare('SELECT Password FROM Users WHERE Username=:username')
        query.bindValue(':username', username)
        query.exec()

        if query.first():
            if query.value(0) == password:
                self.show_message("Success", "Login successful!")
                time.sleep(1)
                self.navigate_to(MainApp)
            else:
                self.show_message("Error", "Password is incorrect")
        else:
            self.show_message("Error", "Username is not found")

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    def navigate_to(self, window_class):
        """Close current window and open a new one of the specified class."""
        self.close()
        self.new_window = window_class()
        self.new_window.show()

    def go_to_signin(self):
        """Navigate to the sign-in window."""
        self.navigate_to(SigninWindow)  # Assuming SigninWindow exists and is imported


class SigninWindow(QMainWindow):
    def __init__(self):
        super(SigninWindow, self).__init__()
        self.ui = Ui_SignInWindow()  # Load the UI generated from Qt Designer
        self.ui.setupUi(self)
        self.setWindowTitle('Sign Up')
        self.setWindowIcon(QIcon(''))

        self.ui.submitButton.clicked.connect(self.handle_submit)
        self.ui.go_to_login_button.clicked.connect(self.go_to_login)  # Assuming button to navigate back to login

        self.status = self.ui.status_label  # Label for status messages

    def handle_submit(self):
        username = self.ui.usernameEdit.text().strip()
        password = self.ui.passwordEdit.text()
        password_confirm = self.ui.passwordEdit_2.text()

        if not username or not password:
            self.show_message("Error", "Username and password cannot be empty")
            return

        if password != password_confirm:
            self.show_message("Error", "Passwords do not match")
            return

        query = QSqlQuery()
        query.prepare("INSERT INTO Users (Username, Password) VALUES (:username, :password)")
        query.bindValue(':username', username)
        query.bindValue(':password', password)

        if query.exec():
            self.show_message("Success", "Account created successfully!")
            self.go_to_login()
        else:
            self.show_message("Error", "Failed to create account")

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    def go_to_login(self):
        """Navigate back to the login window."""
        self.navigate_to(LoginWindow)

    def navigate_to(self, window_class):
        """Close current window and open a new one of the specified class."""
        self.close()
        self.new_window = window_class()
        self.new_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    loginWindow = LoginWindow()
    loginWindow.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')