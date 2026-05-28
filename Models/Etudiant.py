from models.database import DatabaseManager

class StudentModel:
    """Modèle gérant la logique métier et le CRUD des étudiants."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def create_student(self, nom, prenom, email, filiere, username, password):
        """Ajoute un utilisateur et son profil étudiant associé."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            # 1. Créer d'abord son compte utilisateur (Rôle étudiant)
            cursor.execute("""
                INSERT INTO utilisateurs (username, password, role) 
                VALUES (?, ?, 'etudiant')
            """, (username, password))
            
            user_id = cursor.lastrowid
            
            # 2. Créer son profil étudiant lié
            cursor.execute("""
                INSERT INTO etudiants (nom, prenom, email, filiere, utilisateur_id) 
                VALUES (?, ?, ?, ?, ?)
            """, (nom, prenom, email, filiere, user_id))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'étudiant: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def get_all_students(self):
        """Récupère la liste complète des étudiants."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM etudiants")
            return cursor.fetchall()

    def update_student(self, student_id, nom, prenom, email, filiere):
        """Modifie les informations d'un étudiant existant."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE etudiants 
                    SET nom = ?, prenom = ?, email = ?, filiere = ? 
                    WHERE id = ?
                """, (nom, prenom, email, filiere, student_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Erreur lors de la modification: {e}")
            return False

    def delete_student(self, student_id):
        """Supprime un étudiant et son compte utilisateur lié."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            # Récupérer l'id utilisateur d'abord
            cursor.execute("SELECT utilisateur_id FROM etudiants WHERE id = ?", (student_id,))
            result = cursor.fetchone()
            
            if result and result[0]:
                user_id = result[0]
                # Supprimer l'utilisateur (le ON DELETE SET NULL ou CASCADE gère le reste)
                cursor.execute("DELETE FROM utilisateurs WHERE id = ?", (user_id,))
            
            cursor.execute("DELETE FROM etudiants WHERE id = ?", (student_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()