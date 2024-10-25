import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QMenu
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon, QAction
from paramAdv import ParamAdvWindow

# Classe pour la gestion du drag and drop des images
class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText('\n\n Déposez l\'image ici ou cliquez pour la téléverser \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa;
                font-size: 16px;
                color: white;
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Ouvre un dialogue de fichier pour sélectionner une image
            file_path, _ = QFileDialog.getOpenFileName(self, "Choisissez une image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
            if file_path:
                self.setPixmap(QPixmap(file_path))

class AcceuilAdvPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Accueil avec Drag and Drop")
        self.resize(600, 600)
        self.setAcceptDrops(True)  # Autorise le drag and drop

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        layout = QVBoxLayout(central_widget)

        # Barre de recherche + menu burger
        search_layout = QHBoxLayout()

        # Ajout de l'icône du menu burger
        self.menu_icon = QPushButton(self)
        self.menu_icon.setIcon(QIcon('menu_icon.png'))  # Mettre l'icône du menu burger
        self.menu_icon.setIconSize(QSize(25, 25))
        self.menu_icon.setFlat(True)  # Supprime la bordure
        self.menu_icon.setStyleSheet("border: none;")
        self.menu_icon.clicked.connect(self.showMenu)  # Connecte le bouton au menu burger
        search_layout.addWidget(self.menu_icon)

        # Ajout de la barre de recherche fictive (texte non éditable)
        search_label = QPushButton("À rechercher")
        search_label.setFlat(True)
        search_label.setStyleSheet("border: none; font-size: 18px; color: white;")
        search_layout.addWidget(search_label)

        layout.addLayout(search_layout)

        # Zone de drag and drop pour les images
        self.photoViewer = ImageLabel()
        layout.addWidget(self.photoViewer)

    def showMenu(self):
        # Création d'un menu contextuel qui apparaît lorsqu'on clique sur l'icône du menu burger
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

        action_historique = QAction(QIcon('historic_icon.png'), 'Historique', self)
        menu.addAction(action_historique)

        # Option "Paramètres"
        action_favorite = QAction(QIcon('favorite_icon.png'), 'Favoris', self)
        menu.addAction(action_favorite)

        # Option "Sauvegarder l'image"
        action_save = QAction('Sauvegarder l\'image', self)
        action_save.triggered.connect(self.save_image)
        menu.addAction(action_save)

        # Affiche le menu juste sous l'icône du menu burger
        menu.exec(self.menu_icon.mapToGlobal(self.menu_icon.rect().bottomLeft()))

    def save_image(self):
        # Fonction pour sauvegarder l'image
        if not self.photoViewer.pixmap():
            return  # Si aucune image n'est affichée, on ne fait rien
        file_path, _ = QFileDialog.getSaveFileName(self, "Sauvegarder l'image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.photoViewer.pixmap().save(file_path)

    def openSettings(self):
        # Ouvrir la fenêtre des paramètres définie dans `param.py`
        self.settings_window = ParamAdvWindow()  # Créer une instance de ParamWindow
        self.settings_window.show()

    # Méthodes pour le drag and drop
    def dragEnterEvent(self, event):
        # Vérifie si les fichiers glissés sont des images
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                event.acceptProposedAction()  # Accepte le fichier
            else:
                event.ignore()  # Ignore si ce n'est pas une image
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        # Autorise le mouvement pendant le drag
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        # Traitement du fichier déposé
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                self.set_image(file_path)
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()

    def set_image(self, file_path):
        # Affiche l'image dans le QLabel
        self.photoViewer.setPixmap(QPixmap(file_path))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AcceuilAdvPage()
    window.show()
    sys.exit(app.exec())