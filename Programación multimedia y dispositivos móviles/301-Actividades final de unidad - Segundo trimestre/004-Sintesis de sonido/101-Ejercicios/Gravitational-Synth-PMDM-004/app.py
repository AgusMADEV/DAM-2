import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "gravitational_synth.sqlite3"

app = Flask(__name__)


def now_iso() -> str:
    """Retorna timestamp UTC en formato ISO"""
    return datetime.now(timezone.utc).isoformat()


def get_db() -> sqlite3.Connection:
    """Conexión a SQLite con row_factory"""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    """Crea las tablas si no existen"""
    with get_db() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS compositions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                bpm INTEGER NOT NULL DEFAULT 120,
                wave_type TEXT NOT NULL DEFAULT 'sine',
                sequencer_grid TEXT NOT NULL,
                settings_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            """
        )


def seed_demo_data() -> None:
    """Crea datos de demostración si la BD está vacía"""
    with get_db() as connection:
        total = connection.execute("SELECT COUNT(*) AS n FROM compositions").fetchone()["n"]
        if total:
            return

        # Usuario demo
        user_id = connection.execute(
            "INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)",
            ("Demo User", "demo@example.com", now_iso()),
        ).lastrowid

        # Composición demo: ritmo básico de kick (D4) y hat (C5)
        demo_grid = [
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],  # C5 - Hi-hat pattern
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # B4
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # A4
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # G4
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # F4
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # E4
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # D4 - Kick pattern
        ]

        demo_settings = {
            "particleRadius": 15,
            "initialVelocity": 5,
            "particleMass": 1.0,
            "gravity": 0.2,
            "gravityEnabled": True,
            "masterVolume": 0.7,
            "noteDuration": 200,
            "reverbAmount": 0.3
        }

        connection.execute(
            """
            INSERT INTO compositions (
                user_id, title, description, bpm, wave_type, 
                sequencer_grid, settings_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                "Demo Beat",
                "Ritmo básico de demostración",
                120,
                "triangle",
                json.dumps(demo_grid),
                json.dumps(demo_settings),
                now_iso(),
            ),
        )


@app.route("/")
def home():
    """Sirve el archivo HTML principal"""
    return render_template("index.html")


@app.route("/api/health")
def health():
    """Health check endpoint"""
    return jsonify({
        "ok": True,
        "service": "Gravitational Synth API",
        "timestamp": now_iso()
    })


@app.route("/api/users", methods=["POST"])
def create_user():
    """Crea un nuevo usuario"""
    body = request.get_json(silent=True) or {}
    name = str(body.get("name", "")).strip()
    email = str(body.get("email", "")).strip()

    if not name:
        return jsonify({"ok": False, "error": "El nombre es obligatorio"}), 400

    with get_db() as connection:
        user_id = connection.execute(
            "INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)",
            (name, email, now_iso()),
        ).lastrowid

    return jsonify({
        "ok": True,
        "userId": user_id,
        "name": name,
        "email": email
    })


@app.route("/api/compositions", methods=["GET"])
def get_compositions():
    """Lista todas las composiciones (últimas 50)"""
    with get_db() as connection:
        rows = connection.execute(
            """
            SELECT 
                c.id,
                c.title,
                c.description,
                c.bpm,
                c.wave_type,
                c.created_at,
                u.name AS author_name
            FROM compositions c
            LEFT JOIN users u ON c.user_id = u.id
            ORDER BY c.created_at DESC
            LIMIT 50
            """
        ).fetchall()

    compositions = [dict(row) for row in rows]
    return jsonify({"ok": True, "compositions": compositions})


@app.route("/api/compositions/<int:comp_id>", methods=["GET"])
def get_composition(comp_id):
    """Obtiene una composición específica por ID"""
    with get_db() as connection:
        row = connection.execute(
            """
            SELECT 
                c.*,
                u.name AS author_name,
                u.email AS author_email
            FROM compositions c
            LEFT JOIN users u ON c.user_id = u.id
            WHERE c.id = ?
            """,
            (comp_id,)
        ).fetchone()

    if not row:
        return jsonify({"ok": False, "error": "Composición no encontrada"}), 404

    comp = dict(row)
    # Parse JSON fields
    comp["sequencer_grid"] = json.loads(comp["sequencer_grid"])
    comp["settings_json"] = json.loads(comp["settings_json"])

    return jsonify({"ok": True, "composition": comp})


@app.route("/api/compositions", methods=["POST"])
def save_composition():
    """Guarda una nueva composición"""
    body = request.get_json(silent=True) or {}
    
    user_id = body.get("userId") or None
    title = str(body.get("title", "")).strip()
    description = str(body.get("description", "")).strip()
    bpm = int(body.get("bpm", 120))
    wave_type = str(body.get("waveType", "sine"))
    sequencer_grid = body.get("sequencerGrid")
    settings = body.get("settings", {})

    if not title:
        return jsonify({"ok": False, "error": "El título es obligatorio"}), 400

    if not sequencer_grid or not isinstance(sequencer_grid, list):
        return jsonify({"ok": False, "error": "El grid del secuenciador es obligatorio"}), 400

    with get_db() as connection:
        comp_id = connection.execute(
            """
            INSERT INTO compositions (
                user_id, title, description, bpm, wave_type,
                sequencer_grid, settings_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                title,
                description,
                bpm,
                wave_type,
                json.dumps(sequencer_grid),
                json.dumps(settings),
                now_iso(),
            ),
        ).lastrowid

    return jsonify({
        "ok": True,
        "compositionId": comp_id,
        "message": f"Composición '{title}' guardada correctamente"
    })


@app.route("/api/compositions/<int:comp_id>", methods=["DELETE"])
def delete_composition(comp_id):
    """Elimina una composición"""
    with get_db() as connection:
        cursor = connection.execute("DELETE FROM compositions WHERE id = ?", (comp_id,))
        
        if cursor.rowcount == 0:
            return jsonify({"ok": False, "error": "Composición no encontrada"}), 404

    return jsonify({
        "ok": True,
        "message": f"Composición {comp_id} eliminada"
    })


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Retorna estadísticas globales"""
    with get_db() as connection:
        total_comps = connection.execute("SELECT COUNT(*) AS n FROM compositions").fetchone()["n"]
        total_users = connection.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"]

    return jsonify({
        "ok": True,
        "stats": {
            "totalCompositions": total_comps,
            "totalUsers": total_users
        }
    })


if __name__ == "__main__":
    print("🎵 Inicializando Gravitational Synth API...")
    init_db()
    seed_demo_data()
    print("✅ Base de datos lista")
    print("🚀 Servidor corriendo en http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)
