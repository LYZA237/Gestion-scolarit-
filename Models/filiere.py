from models.database import DatabaseManager

class UniversityModel:
    """Modèle gérant la logique des Départements, Filières et requêtes par Niveau."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def ajouter_departement(self, nom_dep):
        """Ajoute un nouveau département (ex: Génie Informatique)."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO departements (nom_dep) VALUES (?)", (nom_dep,))
                conn.commit()
                return True
        except Exception:
            return False

    def ajouter_filiere(self, nom_filiere, departement_id):
        """Ajoute une filière au sein d'un département (ex: TIC)."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO filieres (nom_filiere, departement_id) VALUES (?, ?)", (nom_filiere, departement_id))
                conn.commit()
                return True
        except Exception:
            return False

    def filtrer_etudiants_par_filiere_et_niveau(self, filiere_id, niveau):
        """Affiche les étudiants inscrits dans une filière et un niveau précis (ex: TIC et L2)."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.matricule, e.nom, e.prenom, e.email 
                FROM etudiants e
                WHERE e.filiere_id = ? AND e.niveau = ?
            """, (filiere_id, niveau))
            return cursor.fetchall()
            
    def obtenir_filieres_par_departement(self, departement_id):
        """Récupère toutes les filières d'un département donné."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nom_filiere FROM filieres WHERE departement_id = ?", (departement_id,))
            return cursor.fetchall()