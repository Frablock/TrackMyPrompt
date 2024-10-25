# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QMessageBox, QMainWindow
from views.signin import Ui_SignInWindow
from db.UserDAO import UserDAO
from PyQt6.QtSql import QSqlQuery
from views.login import LoginWindow  # Import de la classe LoginWindow

class SignInController(QMainWindow):
    def __init__(self):
        super(SignInController, self).__init__()
        self.ui = Ui_SignInWindow()  # Charger l'interface utilisateur
        self.ui.setupUi(self)
        self.setWindowTitle("Sign Up")

        # Crée une instance de UserDAO pour interagir avec la base de données
        self.user_dao = UserDAO()

        # Connecter les boutons aux méthodes de gestion
        self.ui.submitButton.clicked.connect(self.handle_submit)
        self.ui.go_to_login_button.clicked.connect(self.go_to_login)  # Bouton pour retourner au login

    def handle_submit(self):
        # Récupérer les valeurs des champs de saisie
        username = self.ui.usernameEdit.text().strip()
        password = self.ui.passwordEdit.text()
        password_confirm = self.ui.passwordEdit_2.text()

        # Vérifier les champs
        if not username or not password:
            self.show_message("Error", "Username and password cannot be empty")
            return

        # Vérifier si les mots de passe correspondent
        if password != password_confirm:
            self.show_message("Error", "Passwords do not match")
            return

        # Créer un nouvel utilisateur
        if self.user_dao.user_exists(username):
            self.show_message("Error", "Username already exists")
        else:
            if self.user_dao.add_user(username, password):  # Méthode add_user qui insère en base
                self.show_message("Success", "Account created successfully!")
                self.go_to_login()
            else:
                self.show_message("Error", "Failed to create account")

    def show_message(self, title, message):
        """Afficher une boîte de dialogue d'information."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    def go_to_login(self):
        """Naviguer vers la fenêtre de connexion (login)."""
        self.navigate_to(LoginWindow)

    def navigate_to(self, window_class):
        """Fermer la fenêtre actuelle et ouvrir la nouvelle fenêtre spécifiée."""
        self.close()
        self.new_window = window_class()
        self.new_window.show()