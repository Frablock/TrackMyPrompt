import sys
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QApplication, QHBoxLayout, QMenu, QMainWindow, QLineEdit
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize

class AcceuilPage(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller  # Référence au contrôleur
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Accueil')
        self.setStyleSheet("background-color: #000000;")  # Fond noir

        # Mise en page principale
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        search_layout = QHBoxLayout()

        # Label "À rechercher"
        self.search_label = QLabel('À rechercher', self)
        self.search_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.search_label.setStyleSheet('font-size: 20px; color: #FF4500;')  # Texte rouge magma
        search_layout.addWidget(self.search_label)

        # Champ de saisie pour la recherche
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText('Entrez votre recherche ici...')
        self.search_input.setStyleSheet('font-size: 16px; color: white; background-color: #333;')  # Style du champ de saisie
        search_layout.addWidget(self.search_input)

        # Bouton de recherche
        self.search_button = QPushButton('Rechercher', self)
        self.search_button.setStyleSheet('font-size: 16px; background-color: #FF4500; color: white;')  # Style du bouton
        search_layout.addWidget(self.search_button)

        # Espacement flexible pour pousser les icônes à droite
        search_layout.addStretch()

        # Icône microphone à droite
        self.mic_icon = QLabel(self)
        self.mic_icon.setPixmap(QPixmap('mic_icon.png').scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio))
        self.mic_icon.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        search_layout.addWidget(self.mic_icon)

        # Espacement entre les icônes
        search_layout.addSpacing(10)

        # Icône menu burger à droite
        self.menu_icon = QPushButton(self)
        self.menu_icon.setIcon(QIcon('menu_icon.jpeg'))  # Mettre l'icône du menu burger
        self.menu_icon.setIconSize(QSize(25, 25))
        self.menu_icon.setFlat(True)
        self.menu_icon.setStyleSheet("border: none;")
        self.menu_icon.clicked.connect(self.controller.showMenu)  # Connexion à la méthode du contrôleur
        search_layout.addWidget(self.menu_icon)

        # Ajouter le layout de recherche au layout principal
        main_layout.addLayout(search_layout)

        # Zone centrale pour téléversement d'image
        self.label_upload = QLabel('Téléversez une image', self)
        self.label_upload.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_upload.setStyleSheet('font-size: 20px; color: #FF4500;')  # Texte rouge magma
        main_layout.addWidget(self.label_upload)

        # Icône de téléversement (cliquable)
        self.upload_button = QPushButton(self)
        self.upload_button.setIcon(QIcon('upload_icon.jpg'))  # Remplacer par ton icône de téléversement
        self.upload_button.setIconSize(QSize(50, 50))  # Taille de l'icône
        self.upload_button.setFlat(True)  # Supprimer le cadre autour du bouton
        self.upload_button.clicked.connect(self.controller.openFileDialog)  # Connexion à la méthode du contrôleur
        self.upload_button.setStyleSheet("border: none;")  # Supprimer les bordures du bouton
        main_layout.addWidget(self.upload_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Label pour afficher l'image téléversée
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.image_label)

    def displayImage(self, pixmap):
        """Affiche l'image téléversée."""
        self.image_label.setPixmap(pixmap)

    def setUploadLabelText(self, text):
        """Définit le texte de l'étiquette de téléversement."""
        self.label_upload.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = AcceuilPage(None)  # Espace réservé pour le contrôleur
    mainWindow.showFullScreen()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Fermeture de la fenêtre...')
