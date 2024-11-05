# ParamAdvController.py

import sys
from PyQt6.QtWidgets import QApplication
from ParamAdvView import ParamAdvView  # Import the view class

class ParamAdvController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view = ParamAdvView()  # Create an instance of the view
        self.view.normal_mode_button.clicked.connect(self.return_to_normal_mode)  # Connect button to method
        self.view.show()

    def run(self):
        sys.exit(self.app.exec())

    def return_to_normal_mode(self):
        # Logic to handle when returning to normal mode can be placed here
        print("Returning to normal mode...")
        self.view.close()  # Close the advanced parameters window

if __name__ == "__main__":
    controller = ParamAdvController()
    controller.run()
