from models.database import DatabaseManager
from models.student_model import StudentModel
from models.academic_model import AcademicModel
from models.university_model import UniversityModel

class MainController:
    """Contrôleur principal orchestrant la logique de l'application (Passerelle MVC)."""
    
    def __init__(self):
        # 1. Initialisation de la base de données unique
        self.db_manager = DatabaseManager()
        
        # 2. Initialisation des modèles spécialisés
        self.student_model = StudentModel(self.db_manager)
        self.academic_model = AcademicModel(self.db_manager)
        self.university_model = UniversityModel(self.db_manager)
        
        # Variable pour mémoriser l'utilisateur actuellement connecté
        self.current_user = None

    # --- LOGIQUE D'AUTHENTIFICATION ---
    def verifier_connexion(self, username, password):
        """Vérifie les identifiants et retourne le rôle ('admin', 'etudiant' ou None)."""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, username, role FROM utilisateurs 
                WHERE username = ? AND password = ?
            """, (username, password))
            user = cursor.fetchone()
            
            if user:
                self.current_user = {"id": user[0], "username": user[1], "role": user[2]}
                return user[2] # Retourne 'admin' ou 'etudiant'
            return None
        except Exception as e:
            print(f"Erreur d'authentification: {e}")
            return None
        finally:
            conn.close()

    # --- PASSERELLE CRUD ÉTUDIANTS ---
    def ajouter_etudiant(self, matricule, nom, prenom, email, niveau, filiere_id, username, password):
        """Demande au modèle d'ajouter un étudiant après validation de base."""
        if not matricule or not nom or not prenom or not email:
            return False, "Veuillez remplir tous les champs obligatoires."
        
        # Hashage ou traitement de sécurité possible ici si nécessaire
        success = self.student_model.create_student(
            matricule, nom, prenom, email, niveau, filiere_id, username, password
        )
        if success:
            return True, "Étudiant créé avec succès !"
        return False, "Échec de la création (Matricule ou Email peut-être déjà utilisé)."

    def lister_tous_les_etudiants(self):
        """Récupère la liste complète via le modèle."""
        return self.student_model.get_all_students()

    # --- PASSERELLE ACADÉMIQUE ---
    def attribuer_notes_et_calculer(self, etudiant_id, cours_id, cc, tp, exam):
        """Transmet les notes, déclenche le calcul de la note finale et du statut UE."""
        if not (0 <= cc <= 20 and 0 <= tp <= 20 and 0 <= exam <= 20):
            return False, "Les notes doivent être comprises entre 0 et 20."
            
        success = self.academic_model.enregistrer_notes(etudiant_id, cours_id, cc, tp, exam)
        if success:
            return True, "Notes enregistrées et calculs mis à jour !"
        return False, "Erreur lors de l'enregistrement des notes."

    def generer_donnees_bulletin(self, etudiant_id):
        """Récupère le bulletin complet avec calcul automatique de la moyenne générale."""
        lignes_bulletin = self.academic_model.obtenir_bulletin_complet(etudiant_id)
        moyenne_generale, mention = self.academic_model.get_student_average(etudiant_id)
        
        return {
            "notes": lignes_bulletin,
            "moyenne_generale": moyenne_generale,
            "mention": mention
        }

    # --- PASSERELLE RECHERCHES & FILTRES ---
    def filtrer_classe(self, filiere_id, niveau):
        """Retourne la liste des étudiants filtrée par filière et niveau (ex: TIC L2)."""
        return self.university_model.filtrer_etudiants_par_filiere_et_niveau(filiere_id, niveau)