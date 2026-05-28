import sys
from PyQt6.QtWidgets import QApplication
from controllers.main_controller import MainController
from views.login_view import LoginView

def main():
    # 1. Création de l'application Qt
    app = QApplication(sys.argv)
    
    # 2. Instanciation du contrôleur unique (Le C de MVC)
    controller = MainController()
    
    # 3. Création et affichage de la vue de connexion en lui passant le contrôleur
    fenetre_login = LoginView(controller)
    fenetre_login.show()
    
    # 4. Lancement de la boucle d'exécution de PyQt6
    sys.exit(app.exec())

if __name__ == "__main__":
    main()