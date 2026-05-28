import sqlite3

class DatabaseManager:
    """Classe responsable de la connexion et de la structure de la base de données."""
    
    def __init__(self, db_name="scolarite.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        """Retourne une connexion active à la base de données."""
        return sqlite3.connect(self.db_name)

    def init_db(self):
        """Crée les tables de l'application si elles n'existent pas encore."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Table des utilisateurs (Pour l'authentification Admin / Étudiant)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS utilisateurs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT CHECK(role IN ('admin', 'etudiant')) NOT NULL
                )
            """)
            
            # 2. Table des étudiants (Pour le CRUD complet)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS etudiants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    filiere TEXT NOT NULL,
                    utilisateur_id INTEGER,
                    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE SET NULL
                )
            """)
            
            # 3. Table des cours
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cours (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    nom_cours TEXT NOT NULL,
                    coefficient INTEGER DEFAULT 1
                )
            """)
            
            # 4. Table des notes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    etudiant_id INTEGER,
                    cours_id INTEGER,
                    note_examen REAL CHECK(note_examen >= 0 AND note_examen <= 20),
                    FOREIGN KEY (etudiant_id) REFERENCES etudiants(id) ON DELETE CASCADE,
                    FOREIGN KEY (cours_id) REFERENCES cours(id) ON DELETE CASCADE,
                    UNIQUE(etudiant_id, cours_id)
                )
            """)
            
            # On insère un compte Administrateur par défaut si la table est vide
            cursor.execute("SELECT COUNT(*) FROM utilisateurs WHERE username = 'admin'")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO utilisateurs (username, password, role) 
                    VALUES ('admin', 'admin123', 'admin')
                """)
                
            conn.commit()