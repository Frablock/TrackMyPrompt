# AcceuilController.py

import sys
import os
from PyQt6.QtWidgets import QApplication, QMenu, QFileDialog, QMessageBox, QDialog
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtCore import Qt  # Added Qt import
from views.accueilPage import AcceuilPage  # Import the view

class AcceuilController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view = AcceuilPage(self)  # Pass the controller to the view
        self.view.showFullScreen()
        self.current_pixmap = None  # Variable to hold the currently displayed image

    def showMenu(self):
        # Applique le style au QMenu pour que les actions héritent du style
        menu = QMenu(self.view)
        menu.setStyleSheet("QMenu { color: #FF4500; background-color: #000000; }") 
        # Ajout des actions sans appeler setStyleSheet() sur elles
        action_webcam = QAction(QIcon('webcam_icon.jpeg'), 'Mode Webcam', self.view)
        menu.addAction(action_webcam)

        action_settings = QAction(QIcon('settings_icon.jpg'), 'Paramètres', self.view)
        action_settings.triggered.connect(self.openSettings)
        menu.addAction(action_settings)

        action_exit = QAction('Quitter', self.view)
        action_exit.triggered.connect(self.view.close)
        menu.addAction(action_exit)

        action_about = QAction(QIcon('info_icon.jpeg'), 'À propos du logiciel', self.view)
        menu.addAction(action_about)

        action_historique = QAction(QIcon('historic_icon.png'), 'Historique', self.view)
        menu.addAction(action_historique)

        action_favorite = QAction(QIcon('favorite_icon.png'), 'Favoris', self.view)
        menu.addAction(action_favorite)

        action_save = QAction('Sauvegarder l\'image', self.view)
        action_save.triggered.connect(self.saveImage)
        menu.addAction(action_save)

        # Affiche le menu à la position du bouton menu_icon
        menu.exec(self.view.menu_icon.mapToGlobal(self.view.menu_icon.rect().bottomLeft()))


    def openSettings(self):
        # Ouvrir la fenêtre des paramètres
        from ParamWindow import ParamWindow  # Import ici pour éviter les dépendances circulaires
        self.settings_window = ParamWindow()  # Créer une instance de ParamWindow
        self.settings_window.setStyleSheet("color: #FF4500; background-color: #000000;")
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
    controller = AcceuilController()
    try:
        sys.exit(controller.app.exec())
    except SystemExit:
        print('Closing Window...')
