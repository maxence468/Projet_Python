import pytest
import todolist
import sqlite3

@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Tache(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nom TEXT NOT NULL, 
        etat BOOLEAN NOT NULL DEFAULT 0
    );
    """)
    conn.commit()
    yield conn
    conn.close()

def test_ajoutTacheBDD(db):
    db.execute(f'INSERT INTO Tache (nom) VALUES ("nomTest")')
    assert db.execute("SELECT COUNT(*) FROM Tache").fetchone()[0] == 1