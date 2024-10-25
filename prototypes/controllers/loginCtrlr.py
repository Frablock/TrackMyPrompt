# -*- coding: utf-8 -*-

from db.UserDAO import UserDAO
from views.home import Ui_HomeWindow
from views.signin import Ui_SignInWindow
from PyQt6.QtWidgets import QMessageBox

class LoginController:
    def __init__(self, ui, main_app):
        self.ui = ui
        self.user_dao = UserDAO()
        self.main_app = main_app  # Référence à la fenêtre principale pour gérer la navigation

        # Connecter les boutons aux méthodes correspondantes
        self.ui.sign_in_button.clicked.connect(self.handle_login)
        self.ui.go_to_signin_button.clicked.connect(self.handle_signin)

    def handle_login(self):
        # Récupérer les informations de l'utilisateur
        username = self.ui.usernameEdit.text().strip()
        password = self.ui.passwordEdit.text()

        # Vérifier si les champs sont remplis
        if not username or not password:
            self.show_message("Error", "Username and password cannot be empty")
            return

        # Vérifier si l'utilisateur existe et si le mot de passe est correct
        if not self.user_dao.user_exists(username):
            self.ui.status_label.setText("User not found")
        elif self.user_dao.get_password(username) != password:
            self.ui.status_label.setText("Wrong password")
        else:
            self.show_message("Success", "Login successful!")
            self.show_home_page()  # Ouvrir la page d'accueil

    def handle_signin(self):
        """Navigue vers la page d'inscription."""
        self.show_signin_page()

    def show_home_page(self):
        """Lance la fenêtre d'accueil et ferme la fenêtre de connexion."""
        self.main_app.close()
        self.home_window = Ui_HomeWindow()
        self.home_window.show()

    def show_signin_page(self):
        """Lance la fenêtre d'inscription et ferme la fenêtre de connexion."""
        self.main_app.close()
        self.signin_window = Ui_SignInWindow()
        self.signin_window.show()

    def show_message(self, title, message):
        """Affiche un message d'information."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()