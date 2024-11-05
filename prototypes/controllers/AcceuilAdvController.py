import sys
import os
from PyQt6.QtWidgets import QApplication, QMenu, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtCore import Qt
from acceuilAdvView import AcceuilAdvView

class AcceuilAdvController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view = AcceuilAdvView(self)
        self.view.showFullScreen()
        self.current_pixmap = None  # Variable to hold the currently displayed image

    def showMenu(self):
        menu = QMenu(self.view)
        menu.setStyleSheet("QMenu { color: #FF4500; background-color: #000000; }")  # Rouge magma pour le menu avec fond noir

        # Option "Mode Webcam"
        action_webcam = QAction(QIcon('webcam_icon.jpeg'), 'Mode Webcam', self.view)
        menu.addAction(action_webcam)

        # Option "Paramètres"
        action_settings = QAction(QIcon('settings_icon.jpgg'), 'Paramètres', self.view)
        action_settings.triggered.connect(self.openSettings)
        menu.addAction(action_settings)

        # Option "Quitter"
        action_exit = QAction('Quitter', self.view)
        action_exit.triggered.connect(self.view.close)
        menu.addAction(action_exit)

        # Option "À propos du logiciel"
        action_about = QAction(QIcon('info_icon.jpeg'), 'À propos du logiciel', self.view)
        menu.addAction(action_about)

        # Option "Historique"
        action_historique = QAction(QIcon('historic_icon.png'), 'Historique', self.view)
        menu.addAction(action_historique)

        # Option "Favoris"
        action_favorite = QAction(QIcon('favorite_icon.png'), 'Favoris', self.view)
        menu.addAction(action_favorite)

        # Option "Sauvegarder l'image"
        action_save = QAction('Sauvegarder l\'image', self.view)
        action_save.triggered.connect(self.saveImage)
        menu.addAction(action_save)

        menu.exec(self.view.menu_icon.mapToGlobal(self.view.menu_icon.rect().bottomLeft()))

    def openSettings(self):
        from ParamAdvView import ParamAdvView  # Importer ici pour éviter les dépendances circulaires
        self.settings_window = ParamAdvView()  # Créer une instance de la fenêtre de paramètres
        self.settings_window.setStyleSheet("color: #FF4500; background-color: #000000;")  # Appliquer la couleur rouge magma
        self.settings_window.show()

    def openFileDialog(self):
        file_dialog = QFileDialog(self.view, 'Sélectionnez une image', os.path.expanduser('~'), 'Images (*.png *.jpg *.bmp)')
        file_dialog.setStyleSheet("QLabel, QPushButton { color: #FF4500; background-color: #000000; }")
        
        file_path, _ = file_dialog.getOpenFileName()

        if file_path:
            self.current_pixmap = QPixmap(file_path)
            self.current_pixmap = self.current_pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio)
            self.view.displayImage(self.current_pixmap)
            self.view.setUploadLabelText('')
        else:
            self.view.setUploadLabelText('Aucune image sélectionnée')

    def saveImage(self):
        if self.current_pixmap is None:
            QMessageBox.warning(self.view, "Aucune image", "Aucune image à sauvegarder.")
            return

        file_dialog = QFileDialog(self.view, 'Sauvegarder l\'image', os.path.expanduser('~'), 'Images (*.png *.jpg *.bmp)')
        file_dialog.setStyleSheet("QLabel, QPushButton { color: #FF4500; background-color: #000000; }")
        
        file_path, _ = file_dialog.getSaveFileName()

        if file_path:
            self.current_pixmap.save(file_path)
            QMessageBox.information(self.view, "Image sauvegardée", f"L'image a été sauvegardée à {file_path}.")


if __name__ == '__main__':
    controller = AcceuilAdvController()
    try:
        sys.exit(controller.app.exec())
    except SystemExit:
        print('Closing Window...')
