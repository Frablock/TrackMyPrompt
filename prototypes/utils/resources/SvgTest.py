from PyQt5.QtWidgets import QApplication, QLabel, QColorDialog, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QColor
import SvgIconManager

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Chemin du fichier SVG
        self.icon_manager = SvgIconManager.SvgIconManager("camera.svg")
        
        # Label pour afficher l'icône
        self.icon_label = QLabel(self)
        
        # Bouton pour changer de couleur
        self.color_button = QPushButton("Choisir une couleur")
        self.color_button.clicked.connect(self.choose_color)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.icon_label)
        layout.addWidget(self.color_button)
        self.setLayout(layout)
        
        # Couleur par défaut
        self.update_icon(QColor(0, 122, 204))  # Bleu par défaut

    def choose_color(self):
        # Ouvre un dialog pour choisir une couleur
        color = QColorDialog.getColor()
        if color.isValid():
            self.update_icon(color)

    def update_icon(self, color: QColor):
        # Met à jour l'icône avec la couleur choisie
        pixmap = self.icon_manager.get_colored_icon(color, size=(100, 100))
        self.icon_label.setPixmap(pixmap)

# Main
app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
