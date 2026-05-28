import sqlite3

class Database:
    """Gestionnaire de base de données complet gérant la structure universitaire, le CRUD et les notes."""
    
    def __init__(self, db_name="scolarite.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Active le support des clés étrangères pour les suppressions en cascade
            cursor.execute("PRAGMA foreign_keys = ON;")
            
            # 1. Authentification
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS utilisateurs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT CHECK(role IN ('admin', 'etudiant')) NOT NULL
                )
            """)
            
            # 2. Départements
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom_dep TEXT UNIQUE NOT NULL
                )
            """)
            
            # 3. Filières (liées à un département)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS filieres (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom_filiere TEXT NOT NULL,
                    departement_id INTEGER,
                    FOREIGN KEY (departement_id) REFERENCES departements(id) ON DELETE CASCADE,
                    UNIQUE(nom_filiere, departement_id)
                )
            """)
            
            # 4. Étudiants (liés à une filière et un niveau : L1, L2, L3, M1, M2...)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS etudiants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    matricule TEXT UNIQUE NOT NULL,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    niveau TEXT CHECK(niveau IN ('L1', 'L2', 'L3', 'M1', 'M2')) NOT NULL,
                    filiere_id INTEGER,
                    utilisateur_id INTEGER,
                    FOREIGN KEY (filiere_id) REFERENCES filieres(id) ON DELETE SET NULL,
                    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE SET NULL
                )
            """)
            
            # 5. Cours / UE (rattachés à une filière et un niveau spécifique)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cours (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    nom_cours TEXT NOT NULL,
                    coefficient INTEGER NOT NULL,
                    niveau TEXT NOT NULL,
                    filiere_id INTEGER,
                    poids_cc REAL DEFAULT 0.2,
                    poids_tp REAL DEFAULT 0.2,
                    poids_exam REAL DEFAULT 0.6,
                    FOREIGN KEY (filiere_id) REFERENCES filieres(id) ON DELETE CASCADE
                )
            """)
            
            # 6. Inscriptions aux cours
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    etudiant_id INTEGER,
                    cours_id INTEGER,
                    FOREIGN KEY (etudiant_id) REFERENCES etudiants(id) ON DELETE CASCADE,
                    FOREIGN KEY (cours_id) REFERENCES cours(id) ON DELETE CASCADE,
                    UNIQUE(etudiant_id, cours_id)
                )
            """)
            
            # 7. Notes Détaillées
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    etudiant_id INTEGER,
                    cours_id INTEGER,
                    note_tpe REAL CHECK(note_tpe >= 0 AND note_tpe <= 20),     
                    note_cc REAL CHECK(note_cc >= 0 AND note_cc <= 20),
                    note_tp REAL CHECK(note_tp >= 0 AND note_tp <= 20),
                    note_exam REAL CHECK(note_exam >= 0 AND note_exam <= 20),
                    note_finale REAL,
                    statut TEXT,
                    FOREIGN KEY (etudiant_id) REFERENCES etudiants(id) ON DELETE CASCADE,
                    FOREIGN KEY (cours_id) REFERENCES cours(id) ON DELETE CASCADE,
                    UNIQUE(etudiant_id, cours_id)
                )
            """)
            
            # Administrateur par défaut
            cursor.execute("SELECT COUNT(*) FROM utilisateurs WHERE username = 'admin'")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO utilisateurs (username, password, role) VALUES ('admin', 'admin123', 'admin')")
                
            conn.commit()