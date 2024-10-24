from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QComboBox

class ParamWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Paramètres')
        self.setGeometry(100, 100, 400, 300)  # Définir la taille de la fenêtre

        # Layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Label de recherche de paramètres
        search_label = QLabel('Rechercher un paramètre', self)
        layout.addWidget(search_label)

        # Nom du modèle
        model_label = QLabel('Nom du modèle :', self)
        layout.addWidget(model_label)
        
        self.model_combo = QComboBox(self)
        self.model_combo.addItems(['Yolo8', 'ModelX', 'ResNet50'])  # Ajouter des options de modèles
        layout.addWidget(self.model_combo)

        # Couleur maître
        color_label = QLabel('Couleur maître :', self)
        layout.addWidget(color_label)
        
        self.color_combo = QComboBox(self)
        self.color_combo.addItems(['Rouge Magma', 'Bleu Océan', 'Vert Forêt'])  # Ajouter des couleurs
        layout.addWidget(self.color_combo)

        # Mode avancé
        self.advanced_checkbox = QCheckBox('Activer le mode avancé', self)
        layout.addWidget(self.advanced_checkbox)
