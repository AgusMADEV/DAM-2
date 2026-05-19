import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "foodiehub_mobile.sqlite3"

app = Flask(__name__)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_db() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_db() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS mobile_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                dni TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                emoji TEXT DEFAULT '🍽️',
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                prep_time_min INTEGER DEFAULT 30,
                difficulty TEXT DEFAULT 'Media',
                cover_emoji TEXT DEFAULT '🍽️',
                ingredients TEXT DEFAULT '[]',
                created_at TEXT NOT NULL,
                FOREIGN KEY(category_id) REFERENCES categories(id)
            );

            CREATE TABLE IF NOT EXISTS app_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                started_at TEXT NOT NULL,
                ended_at TEXT,
                screens_visited INTEGER DEFAULT 0,
                recipes_viewed INTEGER DEFAULT 0,
                favorites_count INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES mobile_users(id)
            );

            CREATE TABLE IF NOT EXISTS user_favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                recipe_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE(user_id, recipe_id),
                FOREIGN KEY(user_id) REFERENCES mobile_users(id),
                FOREIGN KEY(recipe_id) REFERENCES recipes(id)
            );

            CREATE TABLE IF NOT EXISTS app_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                recipe_id INTEGER,
                screen_name TEXT,
                payload_json TEXT DEFAULT '{}',
                created_at TEXT NOT NULL,
                FOREIGN KEY(session_id) REFERENCES app_sessions(id)
            );
            """
        )


def seed_data() -> None:
    with get_db() as connection:
        has_categories = connection.execute("SELECT COUNT(*) AS n FROM categories").fetchone()["n"]
        if has_categories:
            return

        # Insertar categorías
        categories = [
            ("Desayunos", "🥞"),
            ("Comidas", "🍝"),
            ("Postres", "🍰"),
            ("Ensaladas", "🥗"),
            ("Bebidas", "🍹"),
        ]
        connection.executemany(
            "INSERT INTO categories (name, emoji, created_at) VALUES (?, ?, ?)",
            [(name, emoji, now_iso()) for name, emoji in categories],
        )

        # Insertar recetas
        recipes = [
            # Desayunos
            (1, "Pancakes Americanos", "Esponjosos pancakes con sirope de arce", 20, "Fácil", "🥞", 
             '["2 tazas de harina", "2 huevos", "1.5 tazas leche", "Azúcar", "Levadura"]'),
            (1, "Tostadas Francesas", "Tostadas doradas perfectas", 15, "Fácil", "🍞",
             '["4 rebanadas pan", "2 huevos", "Leche", "Canela", "Azúcar"]'),
            
            # Comidas
            (2, "Pasta Carbonara", "Receta italiana clásica", 25, "Media", "🍝",
             '["400g pasta", "200g panceta", "3 huevos", "Queso parmesano", "Pimienta negra"]'),
            (2, "Paella Valenciana", "Paella tradicional española", 60, "Difícil", "🥘",
             '["Arroz bomba", "Pollo", "Conejo", "Judías verdes", "Garrofón", "Azafrán"]'),
            (2, "Lasaña Boloñesa", "Capas de pasta con carne", 90, "Difícil", "🍝",
             '["Pasta lasaña", "Carne picada", "Salsa bechamel", "Tomate", "Queso"]'),
            (2, "Tacos al Pastor", "Tacos mexicanos auténticos", 45, "Media", "🌮",
             '["Carne de cerdo", "Piña", "Cebolla", "Cilantro", "Tortillas"]'),
            
            # Postres
            (3, "Tarta de Chocolate", "Tarta húmeda y deliciosa", 75, "Media", "🍰",
             '["Chocolate negro", "Huevos", "Azúcar", "Harina", "Mantequilla"]'),
            (3, "Crème Brûlée", "Postre francés cremoso", 50, "Difícil", "🍮",
             '["Nata", "Yemas de huevo", "Azúcar", "Vainilla"]'),
            (3, "Tiramisú", "Postre italiano con café", 30, "Fácil", "🍰",
             '["Bizcochos", "Café", "Mascarpone", "Huevos", "Cacao"]'),
            
            # Ensaladas
            (4, "Ensalada César", "Ensalada con pollo y crutones", 20, "Fácil", "🥗",
             '["Lechuga romana", "Pollo", "Crutones", "Parmesano", "Salsa césar"]'),
            (4, "Ensalada Griega", "Fresca y mediterránea", 15, "Fácil", "🥗",
             '["Tomate", "Pepino", "Cebolla", "Aceitunas", "Queso feta"]'),
            
            # Bebidas
            (5, "Smoothie de Frutas", "Batido saludable", 5, "Fácil", "🍹",
             '["Plátano", "Fresas", "Yogur", "Miel", "Hielo"]'),
            (5, "Mojito Cubano", "Cóctel refrescante", 10, "Fácil", "🍹",
             '["Ron blanco", "Lima", "Azúcar", "Menta", "Soda"]'),
        ]
        
        connection.executemany(
            """INSERT INTO recipes (category_id, title, description, prep_time_min, 
               difficulty, cover_emoji, ingredients, created_at) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            [(cat_id, title, desc, time, diff, emoji, ing, now_iso()) 
             for cat_id, title, desc, time, diff, emoji, ing in recipes],
        )


# ══════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════

@app.route("/")
def index():
    return render_template("index.html")


# ── USERS ─────────────────────────────────────────────
@app.route("/api/users/register", methods=["POST"])
def register_user():
    data = request.get_json()
    name = (data.get("name") or "").strip()
    dni = (data.get("dni") or "").strip()
    
    if not name or not dni:
        return jsonify({"ok": False, "error": "Nombre y DNI requeridos"}), 400

    with get_db() as connection:
        existing = connection.execute(
            "SELECT id FROM mobile_users WHERE dni = ?", (dni,)
        ).fetchone()
        
        if existing:
            user_id = existing["id"]
        else:
            cursor = connection.execute(
                "INSERT INTO mobile_users (name, dni, created_at) VALUES (?, ?, ?)",
                (name, dni, now_iso()),
            )
            user_id = cursor.lastrowid

    return jsonify({"ok": True, "userId": user_id, "name": name})


# ── SESSIONS ──────────────────────────────────────────
@app.route("/api/sessions/start", methods=["POST"])
def start_session():
    data = request.get_json()
    user_id = data.get("userId")
    
    if not user_id:
        return jsonify({"ok": False, "error": "userId requerido"}), 400

    with get_db() as connection:
        cursor = connection.execute(
            "INSERT INTO app_sessions (user_id, started_at) VALUES (?, ?)",
            (user_id, now_iso()),
        )
        session_id = cursor.lastrowid

    return jsonify({"ok": True, "sessionId": session_id})


@app.route("/api/sessions/<int:session_id>/end", methods=["POST"])
def end_session(session_id):
    with get_db() as connection:
        connection.execute(
            "UPDATE app_sessions SET ended_at = ? WHERE id = ?",
            (now_iso(), session_id),
        )
    return jsonify({"ok": True})


# ── CATEGORIES ────────────────────────────────────────
@app.route("/api/categories")
def get_categories():
    with get_db() as connection:
        rows = connection.execute("SELECT * FROM categories ORDER BY name").fetchall()
    
    categories = [dict(row) for row in rows]
    return jsonify({"ok": True, "categories": categories})


# ── RECIPES ───────────────────────────────────────────
@app.route("/api/recipes")
def get_recipes():
    with get_db() as connection:
        query = """
            SELECT r.*, c.name as category_name, c.emoji as category_emoji
            FROM recipes r
            JOIN categories c ON r.category_id = c.id
            ORDER BY r.created_at DESC
        """
        rows = connection.execute(query).fetchall()
    
    recipes = []
    for row in rows:
        r = dict(row)
        r["ingredients"] = json.loads(r["ingredients"])
        recipes.append(r)
    
    return jsonify({"ok": True, "recipes": recipes})


# ── FAVORITES ─────────────────────────────────────────
@app.route("/api/favorites", methods=["GET"])
def get_favorites():
    user_id = request.args.get("userId")
    
    if not user_id:
        return jsonify({"ok": False, "error": "userId requerido"}), 400

    with get_db() as connection:
        rows = connection.execute(
            "SELECT recipe_id FROM user_favorites WHERE user_id = ?",
            (user_id,)
        ).fetchall()
    
    favorite_ids = [row["recipe_id"] for row in rows]
    return jsonify({"ok": True, "favoriteIds": favorite_ids})


@app.route("/api/favorites/toggle", methods=["POST"])
def toggle_favorite():
    data = request.get_json()
    user_id = data.get("userId")
    recipe_id = data.get("recipeId")
    
    if not user_id or not recipe_id:
        return jsonify({"ok": False, "error": "userId y recipeId requeridos"}), 400

    with get_db() as connection:
        existing = connection.execute(
            "SELECT id FROM user_favorites WHERE user_id = ? AND recipe_id = ?",
            (user_id, recipe_id)
        ).fetchone()
        
        if existing:
            connection.execute(
                "DELETE FROM user_favorites WHERE user_id = ? AND recipe_id = ?",
                (user_id, recipe_id)
            )
            is_favorite = False
        else:
            connection.execute(
                "INSERT INTO user_favorites (user_id, recipe_id, created_at) VALUES (?, ?, ?)",
                (user_id, recipe_id, now_iso())
            )
            is_favorite = True

    return jsonify({"ok": True, "isFavorite": is_favorite})


# ── EVENTS ────────────────────────────────────────────
@app.route("/api/events", methods=["POST"])
def log_event():
    data = request.get_json()
    session_id = data.get("sessionId")
    event_type = data.get("eventType")
    recipe_id = data.get("recipeId")
    screen_name = data.get("screenName")
    payload = data.get("payload", {})
    
    if not session_id or not event_type:
        return jsonify({"ok": False, "error": "sessionId y eventType requeridos"}), 400

    with get_db() as connection:
        connection.execute(
            """INSERT INTO app_events 
               (session_id, event_type, recipe_id, screen_name, payload_json, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (session_id, event_type, recipe_id, screen_name, json.dumps(payload), now_iso())
        )

    return jsonify({"ok": True})


# ── STATS ─────────────────────────────────────────────
@app.route("/api/stats")
def get_stats():
    with get_db() as connection:
        users_count = connection.execute("SELECT COUNT(*) as n FROM mobile_users").fetchone()["n"]
        categories_count = connection.execute("SELECT COUNT(*) as n FROM categories").fetchone()["n"]
        recipes_count = connection.execute("SELECT COUNT(*) as n FROM recipes").fetchone()["n"]
        sessions_count = connection.execute("SELECT COUNT(*) as n FROM app_sessions").fetchone()["n"]
        events_count = connection.execute("SELECT COUNT(*) as n FROM app_events").fetchone()["n"]
        favorites_count = connection.execute("SELECT COUNT(*) as n FROM user_favorites").fetchone()["n"]

    return jsonify({
        "ok": True,
        "stats": {
            "users": users_count,
            "categories": categories_count,
            "recipes": recipes_count,
            "sessions": sessions_count,
            "events": events_count,
            "favorites": favorites_count,
        }
    })


# ── LEADERBOARD ───────────────────────────────────────
@app.route("/api/leaderboard")
def get_leaderboard():
    with get_db() as connection:
        query = """
            SELECT 
                u.id,
                u.name,
                COUNT(DISTINCT s.id) as sessions,
                COUNT(DISTINCT f.id) as favorites
            FROM mobile_users u
            LEFT JOIN app_sessions s ON u.id = s.user_id
            LEFT JOIN user_favorites f ON u.id = f.user_id
            GROUP BY u.id, u.name
            ORDER BY favorites DESC, sessions DESC
            LIMIT 10
        """
        rows = connection.execute(query).fetchall()
    
    leaders = [dict(row) for row in rows]
    return jsonify({"ok": True, "leaders": leaders})


# ── SEED ──────────────────────────────────────────────
@app.route("/api/seed", methods=["POST"])
def seed():
    seed_data()
    return jsonify({"ok": True, "message": "Datos de prueba cargados"})


# ── EXPORT / IMPORT ───────────────────────────────────
@app.route("/api/export")
def export_data():
    with get_db() as connection:
        tables = ["mobile_users", "categories", "recipes", "app_sessions", "user_favorites", "app_events"]
        data = {}
        
        for table in tables:
            rows = connection.execute(f"SELECT * FROM {table}").fetchall()
            data[table] = [dict(row) for row in rows]

    return jsonify({"ok": True, "data": data})


@app.route("/api/import", methods=["POST"])
def import_data():
    data = request.get_json()
    imported = data.get("data", {})
    
    with get_db() as connection:
        # Limpiar tablas
        connection.execute("DELETE FROM app_events")
        connection.execute("DELETE FROM user_favorites")
        connection.execute("DELETE FROM app_sessions")
        connection.execute("DELETE FROM recipes")
        connection.execute("DELETE FROM categories")
        connection.execute("DELETE FROM mobile_users")
        
        # Importar datos
        for user in imported.get("mobile_users", []):
            connection.execute(
                "INSERT INTO mobile_users (id, name, dni, created_at) VALUES (?, ?, ?, ?)",
                (user["id"], user["name"], user["dni"], user["created_at"])
            )
        
        for cat in imported.get("categories", []):
            connection.execute(
                "INSERT INTO categories (id, name, emoji, created_at) VALUES (?, ?, ?, ?)",
                (cat["id"], cat["name"], cat["emoji"], cat["created_at"])
            )
        
        for recipe in imported.get("recipes", []):
            connection.execute(
                """INSERT INTO recipes 
                   (id, category_id, title, description, prep_time_min, difficulty, 
                    cover_emoji, ingredients, created_at) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (recipe["id"], recipe["category_id"], recipe["title"], recipe["description"],
                 recipe["prep_time_min"], recipe["difficulty"], recipe["cover_emoji"],
                 recipe["ingredients"], recipe["created_at"])
            )

    return jsonify({"ok": True, "message": "Datos importados correctamente"})


# ══════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════

if __name__ == "__main__":
    init_db()
    seed_data()
    print("🍳 FoodieHub Mobile Lab iniciado en http://localhost:5091")
    app.run(debug=True, host="0.0.0.0", port=5091)
