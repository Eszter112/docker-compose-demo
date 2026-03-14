from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# On s'assure que le dossier /data existe dès l'import
os.makedirs("/data", exist_ok=True)

# Chemin de la BDD
DB_PATH = "/data/messages.db"


def init_db():
    """Initialise la BDD si elle n'existe pas"""
    os.makedirs("/data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


# 🔥 IMPORTANT : on initialise la BDD dès l'import du module
init_db()


@app.route("/")
def home():
    return "Hello from Flask!"


@app.route("/write")
def write():
    msg = request.args.get("msg", "Message par défaut")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (content) VALUES (?)", (msg,))
    conn.commit()
    conn.close()
    return f"✅ Message écrit : {msg}"


@app.route("/read")
def read():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages")
    messages = cursor.fetchall()
    conn.close()

    if not messages:
        return "Aucun message"

    result = "<h2>Messages enregistrés :</h2><ul>"
    for msg in messages:
        result += f"<li>ID {msg[0]}: {msg[1]}</li>"
    result += "</ul>"
    return result


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
