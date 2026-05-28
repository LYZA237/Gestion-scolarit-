import sys
from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, 
                             QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout)
from PyQt6.QtCore import Qt
from controllers.main_controller import MainController

class LoginView(QWidget):
    """Fenêtre d'authentification de l'application (Vue)."""
    
    def __init__(self, controller: MainController):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        """Initialise les composants graphiques de la fenêtre."""
        self.setWindowTitle("Connexion - Gestion Scolarité")
        self.setFixedSize(350, 250)
        
        # Disposition principale verticale
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Titre d'accueil
        self.title_label = QLabel("Authentification")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(self.title_label)
        
        # Champ d'identifiant
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur (ex: admin)")
        layout.addWidget(self.username_input)
        
        # Champ de mot de passe
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password) # Cache les caractères
        layout.addWidget(self.password_input)
        
        # Bouton de connexion
        self.login_button = QPushButton("Se connecter")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db; 
                color: white; 
                font-weight: bold; 
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        # Connexion du clic du bouton à notre méthode de vérification
        self.login_button.clicked.connect(self.gerer_connexion)
        layout.addWidget(self.login_button)
        
        self.setLayout(layout)

    def gerer_connexion(self):
        """Récupère les saisies et demande au contrôleur de valider."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")
            return
            
        # Appel de la logique dans le contrôleur
        role = self.controller.verifier_connexion(username, password)
        
        if role == 'admin':
            QMessageBox.information(self, "Succès", f"Bienvenue, Administrateur {username} !")
            # C'est ici qu'on ouvrira le tableau de bord Admin plus tard
            self.close()
        elif role == 'etudiant':
            QMessageBox.information(self, "Succès", f"Bienvenue dans votre espace Étudiant, {username} !")
            # C'est ici qu'on ouvrira l'espace Étudiant plus tard
            self.close()
        else:
            QMessageBox.critical(self, "Échec", "Nom d'utilisateur ou mot de passe incorrect.")