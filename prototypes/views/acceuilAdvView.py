import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication, QHBoxLayout, QMainWindow, QLineEdit
from PyQt6.QtGui import QIcon, QPixmap, QDragEnterEvent, QDropEvent
from PyQt6.QtCore import Qt, QSize

class AcceuilAdvView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller  # Reference to the controller
        self.initUI()
        
        # Enable drag and drop
        self.setAcceptDrops(True)

    def initUI(self):
        self.setWindowTitle('Accueil Avancé')
        self.setStyleSheet("background-color: #000000; color: #FF4500;")  # Fond noir et texte rouge magma

        # Main layout
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

        # Microphone icon on the right
        self.mic_icon = QLabel(self)
        self.mic_icon.setPixmap(QPixmap('mic_icon.png').scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio))
        self.mic_icon.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        search_layout.addWidget(self.mic_icon)

        # Space between icons
        search_layout.addSpacing(10)

        # Menu button on the right
        self.menu_icon = QPushButton(self)
        self.menu_icon.setIcon(QIcon('menu_icon.jpeg'))  # Set the hamburger menu icon
        self.menu_icon.setIconSize(QSize(25, 25))
        self.menu_icon.setFlat(True)
        self.menu_icon.setStyleSheet("border: none;")  # Remove border around button
        self.menu_icon.clicked.connect(self.controller.showMenu)  # Connect to the controller method
        search_layout.addWidget(self.menu_icon)

        # Add the search layout to the main layout
        main_layout.addLayout(search_layout)

        # Central area for image upload
        self.label_upload = QLabel('Téléversez une image', self)
        self.label_upload.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_upload.setStyleSheet('font-size: 20px; color: #FF4500;')  # Texte rouge magma
        main_layout.addWidget(self.label_upload)

        # Upload icon button
        self.upload_button = QPushButton(self)
        self.upload_button.setIcon(QIcon('upload_icon.jpg'))  # Replace with your upload icon
        self.upload_button.setIconSize(QSize(50, 50))  # Icon size
        self.upload_button.setFlat(True)  # Remove the border around the button
        self.upload_button.clicked.connect(self.controller.openFileDialog)  # Connect to the controller method
        self.upload_button.setStyleSheet("border: none;")  # Remove borders from the button
        main_layout.addWidget(self.upload_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Label to display the uploaded image
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.image_label)

    def displayImage(self, pixmap):
        """Display the uploaded image."""
        self.image_label.setPixmap(pixmap)

    def setUploadLabelText(self, text):
        """Set the text of the upload label."""
        self.label_upload.setText(text)

    # Enable drag-and-drop methods
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasImage() or event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):  # Check for image file types
                    self.controller.current_pixmap = QPixmap(file_path)  # Store the current image
                    self.controller.current_pixmap = self.controller.current_pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio)  # Resize the image
                    self.displayImage(self.controller.current_pixmap)  # Display the image
                    self.setUploadLabelText('')  # Clear the upload label text
                    break
            else:
                self.setUploadLabelText('Format d\'image non supporté.')  # Invalid file type message

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = AcceuilAdvView(None)  # Placeholder for the controller
    mainWindow.showFullScreen()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')
