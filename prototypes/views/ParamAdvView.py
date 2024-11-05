# ParamAdvView.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QPushButton, QComboBox

class ParamAdvView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Paramètres Avancés')
        self.setGeometry(150, 150, 400, 400)  # Définir la taille de la fenêtre

        # Layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Taille du batch
        batch_size_label = QLabel('Taille du batch :', self)
        layout.addWidget(batch_size_label)
        
        self.batch_size_spin = QSpinBox(self)
        self.batch_size_spin.setRange(1, 128)  # Plage de valeurs
        layout.addWidget(self.batch_size_spin)

        # Taux d'apprentissage
        learning_rate_label = QLabel('Taux d\'apprentissage :', self)
        layout.addWidget(learning_rate_label)
        
        self.learning_rate_spin = QSpinBox(self)
        self.learning_rate_spin.setRange(1, 100)  # Plage de valeurs
        self.learning_rate_spin.setSingleStep(1)
        layout.addWidget(self.learning_rate_spin)

        # Nombre d'époques
        epochs_label = QLabel('Nombre d\'époques :', self)
        layout.addWidget(epochs_label)
        
        self.epochs_spin = QSpinBox(self)
        self.epochs_spin.setRange(1, 1000)  # Plage de valeurs
        self.epochs_spin.setSingleStep(10)
        layout.addWidget(self.epochs_spin)

        # Type d'optimiseur
        optimizer_label = QLabel('Optimiseur :', self)
        layout.addWidget(optimizer_label)

        self.optimizer_combo = QComboBox(self)
        self.optimizer_combo.addItems(['Adam', 'SGD', 'RMSprop'])  # Options d'optimiseur
        layout.addWidget(self.optimizer_combo)

        # Bouton pour revenir en mode normal
        self.normal_mode_button = QPushButton('Revenir en mode normal', self)
        layout.addWidget(self.normal_mode_button)

        # Connecter le bouton à une méthode qui fermera la fenêtre
        self.normal_mode_button.clicked.connect(self.close)
