from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtSvg import QSvgRenderer

class SvgIconManager:
    def __init__(self, svg_file_path):
        self.svg_file_path = svg_file_path
        self.renderer = QSvgRenderer(svg_file_path)

    def get_colored_icon(self, color: QColor, size=(100, 100)):
        # Crée un QPixmap transparent de la taille souhaitée
        pixmap = QPixmap(size[0], size[1])
        pixmap.fill(Qt.transparent)  # Remplissage transparent

        # Peindre l'icône SVG sur le pixmap avec la couleur choisie
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Définit le pinceau de peinture avec la couleur
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        
        # Dessine l'icône SVG
        self.renderer.render(painter)
        painter.end()
        
        return pixmap