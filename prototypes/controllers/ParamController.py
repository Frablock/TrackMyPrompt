# ParamController.py

import sys
from PyQt6.QtWidgets import QApplication
from ParamWindow import ParamWindow

class ParamController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view = ParamWindow()  # Créer une instance de la fenêtre des paramètres
        self.view.show()

    def run(self):
        sys.exit(self.app.exec())

    def getParams(self):
        model = self.view.getSelectedModel()
        color = self.view.getSelectedColor()
        advanced_mode = self.view.isAdvancedMode()
        print(f"Model: {model}, Color: {color}, Advanced Mode: {advanced_mode}")

if __name__ == '__main__':
    controller = ParamController()
    controller.run()
