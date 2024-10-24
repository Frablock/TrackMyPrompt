import sys
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QApplication, QHBoxLayout, QMenu, QMainWindow
from PyQt6.QtGui import QAction  # Modifier l'import de QAction ici
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
from param import ParamWindow  # Importer la fenêtre des paramètres

class AcceuilPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Accueil')

        # Layout principal
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Barre de recherche simulée (juste un label) avec les icônes micro et menu
        search_layout = QHBoxLayout()

        # Label "À rechercher"
        self.search_label = QLabel('À rechercher', self)
        self.search_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.search_label.setStyleSheet('font-size: 20px;')
        search_layout.addWidget(self.search_label)

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
        self.menu_icon.setIcon(QIcon('menu_icon.png'))  # Mettre l'icône du menu burger
        self.menu_icon.setIconSize(QSize(25, 25))
        self.menu_icon.setFlat(True)
        self.menu_icon.setStyleSheet("border: none;")
        self.menu_icon.clicked.connect(self.showMenu)
        search_layout.addWidget(self.menu_icon)

        # Ajouter le layout de recherche au layout principal
        main_layout.addLayout(search_layout)

        # Zone centrale pour téléversement d'image
        self.label_upload = QLabel('Téléversez une image', self)
        self.label_upload.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_upload.setStyleSheet('font-size: 20px;')
        main_layout.addWidget(self.label_upload)

        # Icône de téléversement (cliquable)
        self.upload_button = QPushButton(self)
        self.upload_button.setIcon(QIcon('upload_icon.png'))  # Remplacer par ton icône de téléversement
        self.upload_button.setIconSize(QSize(50, 50))  # Taille de l'icône
        self.upload_button.setFlat(True)  # Supprimer le cadre autour du bouton
        self.upload_button.clicked.connect(self.openFileDialog)  # Connecter l'icône au téléversement de fichier
        self.upload_button.setStyleSheet("border: none;")  # Supprimer les bordures du bouton
        main_layout.addWidget(self.upload_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Label pour afficher l'image téléversée
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.image_label)

    def showMenu(self):
        # Créer un menu contextuel
        menu = QMenu(self)

        # Option "Mode Webcam"
        action_webcam = QAction(QIcon('webcam_icon.png'), 'Mode Webcam', self)
        menu.addAction(action_webcam)

        # Option "Paramètres"
        action_settings = QAction(QIcon('settings_icon.png'), 'Paramètres', self)
        action_settings.triggered.connect(self.openSettings)
        menu.addAction(action_settings)

        # Option "À propos du logiciel"
        action_about = QAction(QIcon('info_icon.png'), 'À propos du logiciel', self)
        menu.addAction(action_about)

        # Option "Sauvegarder l'image"
        action_save = QAction('Sauvegarder l\'image', self)
        action_save.triggered.connect(self.saveImage)
        menu.addAction(action_save)

        # Affiche le menu à la position du bouton menu_icon
        menu.exec(self.menu_icon.mapToGlobal(self.menu_icon.rect().bottomLeft()))

    def openSettings(self):
        # Ouvrir la fenêtre des paramètres définie dans `param.py`
        self.settings_window = ParamWindow()  # Créer une instance de ParamWindow
        self.settings_window.show()

    def openFileDialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Sélectionnez une image', os.path.expanduser('~'), 'Images (*.png *.jpg *.bmp)')
        
        if file_path:
            # Charger et afficher l'image sélectionnée
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio)  # Redimensionner l'image
            self.image_label.setPixmap(pixmap)
            self.label_upload.setText('')  # Effacer le texte "Téléversez une image"
        else:
            self.label_upload.setText('Aucune image sélectionnée')


    def saveImage(self):
        # Simuler la sauvegarde de l'image
        print("Image sauvegardée !")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Créer une instance de la page d'accueil
    mainWindow = AcceuilPage()

    # Ouvrir la fenêtre en plein écran
    mainWindow.showFullScreen()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')

