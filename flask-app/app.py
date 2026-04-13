import os
from datetime import date, datetime, timedelta

import pymysql
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
load_dotenv()


def get_db():
    return pymysql.connect(
        host=os.getenv("FLASK_DB_HOST", "127.0.0.1"),
        port=int(os.getenv("FLASK_DB_PORT", "3306")),
        user=os.getenv("FLASK_DB_USER", "root"),
        password=os.getenv("FLASK_DB_PASSWORD", ""),
        database=os.getenv("FLASK_DB_NAME", "smart_pantry"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )


def initialize_db():
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ingredients (
                id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(120) NOT NULL,
                quantity DECIMAL(10, 2) NOT NULL,
                unit VARCHAR(50) NOT NULL,
                expiry_date DATE NOT NULL,
                created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usage_logs (
                id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                ingredient_id BIGINT UNSIGNED NOT NULL,
                used_quantity DECIMAL(10, 2) NOT NULL,
                date DATE NOT NULL,
                created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                CONSTRAINT fk_usage_ingredient
                    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
                    ON DELETE CASCADE
            )
            """
        )
        connection.commit()


def seed_db_if_empty():
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM ingredients")
        count = cursor.fetchone()["total"]
        if count > 0:
            return

        ingredients = [
            ("Milk", 2, "bottle", "2026-04-20"),
            ("Eggs", 12, "piece", "2026-04-18"),
            ("Rice", 1.5, "kg", "2026-12-31"),
        ]
        cursor.executemany(
            "INSERT INTO ingredients (name, quantity, unit, expiry_date) VALUES (%s, %s, %s, %s)",
            ingredients,
        )
        cursor.execute("SELECT id FROM ingredients WHERE name = %s ORDER BY id LIMIT 1", ("Milk",))
        milk_id = cursor.fetchone()["id"]
        cursor.execute("SELECT id FROM ingredients WHERE name = %s ORDER BY id LIMIT 1", ("Eggs",))
        eggs_id = cursor.fetchone()["id"]

        usage_logs = [
            (milk_id, 1, "2026-04-13"),
            (eggs_id, 2, "2026-04-13"),
        ]
        cursor.executemany(
            "INSERT INTO usage_logs (ingredient_id, used_quantity, date) VALUES (%s, %s, %s)",
            usage_logs,
        )
        connection.commit()


def parse_expiry_date(raw_value):
    try:
        return datetime.strptime(str(raw_value), "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def serialize_ingredient(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "quantity": float(row["quantity"]),
        "unit": row["unit"],
        "expiry_date": row["expiry_date"].isoformat(),
    }


def serialize_usage(row):
    return {
        "id": row["id"],
        "ingredient_id": row["ingredient_id"],
        "used_quantity": float(row["used_quantity"]),
        "date": row["date"].isoformat(),
    }


@app.route("/")
def hello():
    return render_template("index.html")


@app.get("/api/ingredients")
def list_ingredients():
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ingredients ORDER BY id")
        rows = cursor.fetchall()
    return jsonify([serialize_ingredient(row) for row in rows])


@app.get("/api/ingredients/<int:ingredient_id>")
def get_ingredient(ingredient_id):
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ingredients WHERE id = %s", (ingredient_id,))
        row = cursor.fetchone()
    if row is None:
        return jsonify({"error": "Ingredient not found"}), 404
    return jsonify(serialize_ingredient(row))


@app.post("/api/ingredients")
def create_ingredient():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    quantity = payload.get("quantity")
    unit = payload.get("unit")
    expiry_date = payload.get("expiry_date")

    if not name or quantity is None or not unit or not expiry_date:
        return jsonify({"error": "name, quantity, unit, expiry_date are required"}), 422
    if parse_expiry_date(expiry_date) is None:
        return jsonify({"error": "expiry_date must be in YYYY-MM-DD format"}), 422

    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO ingredients (name, quantity, unit, expiry_date) VALUES (%s, %s, %s, %s)",
            (name, quantity, unit, expiry_date),
        )
        ingredient_id = cursor.lastrowid
        cursor.execute("SELECT * FROM ingredients WHERE id = %s", (ingredient_id,))
        row = cursor.fetchone()
        connection.commit()
    return jsonify(serialize_ingredient(row)), 201


@app.put("/api/ingredients/<int:ingredient_id>")
def update_ingredient(ingredient_id):
    payload = request.get_json(silent=True) or {}
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ingredients WHERE id = %s", (ingredient_id,))
        row = cursor.fetchone()
        if row is None:
            return jsonify({"error": "Ingredient not found"}), 404

        name = payload.get("name", row["name"])
        quantity = payload.get("quantity", row["quantity"])
        unit = payload.get("unit", row["unit"])
        expiry_date = payload.get("expiry_date", row["expiry_date"])
        if parse_expiry_date(expiry_date) is None:
            return jsonify({"error": "expiry_date must be in YYYY-MM-DD format"}), 422

        cursor.execute(
            "UPDATE ingredients SET name = %s, quantity = %s, unit = %s, expiry_date = %s WHERE id = %s",
            (name, quantity, unit, expiry_date, ingredient_id),
        )
        cursor.execute("SELECT * FROM ingredients WHERE id = %s", (ingredient_id,))
        updated = cursor.fetchone()
        connection.commit()
    return jsonify(serialize_ingredient(updated))


@app.delete("/api/ingredients/<int:ingredient_id>")
def delete_ingredient(ingredient_id):
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM ingredients WHERE id = %s", (ingredient_id,))
        exists = cursor.fetchone()
        if exists is None:
            return jsonify({"error": "Ingredient not found"}), 404
        cursor.execute("DELETE FROM ingredients WHERE id = %s", (ingredient_id,))
        connection.commit()
    return "", 204


@app.post("/api/ingredients/<int:ingredient_id>/use")
def use_ingredient(ingredient_id):
    payload = request.get_json(silent=True) or {}
    used_quantity = payload.get("used_quantity")
    usage_date = payload.get("date", date.today().isoformat())
    try:
        used_quantity = float(used_quantity)
    except (TypeError, ValueError):
        return jsonify({"error": "used_quantity must be a positive number"}), 422
    if used_quantity <= 0:
        return jsonify({"error": "used_quantity must be a positive number"}), 422
    if parse_expiry_date(usage_date) is None:
        return jsonify({"error": "date must be in YYYY-MM-DD format"}), 422

    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ingredients WHERE id = %s", (ingredient_id,))
        ingredient = cursor.fetchone()
        if ingredient is None:
            return jsonify({"error": "Ingredient not found"}), 404

        remaining = float(ingredient["quantity"]) - used_quantity
        if remaining < 0:
            return jsonify({"error": "Insufficient stock"}), 422

        cursor.execute("UPDATE ingredients SET quantity = %s WHERE id = %s", (remaining, ingredient_id))
        cursor.execute(
            "INSERT INTO usage_logs (ingredient_id, used_quantity, date) VALUES (%s, %s, %s)",
            (ingredient_id, used_quantity, usage_date),
        )
        usage_id = cursor.lastrowid
        cursor.execute("SELECT * FROM usage_logs WHERE id = %s", (usage_id,))
        usage_log = cursor.fetchone()
        cursor.execute("SELECT * FROM ingredients WHERE id = %s", (ingredient_id,))
        ingredient_after = cursor.fetchone()
        connection.commit()

    return jsonify({"ingredient": serialize_ingredient(ingredient_after), "usage": serialize_usage(usage_log)}), 201


@app.get("/api/ingredients/<int:ingredient_id>/usage")
def ingredient_usage(ingredient_id):
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM ingredients WHERE id = %s", (ingredient_id,))
        ingredient = cursor.fetchone()
        if ingredient is None:
            return jsonify({"error": "Ingredient not found"}), 404
        cursor.execute(
            "SELECT * FROM usage_logs WHERE ingredient_id = %s ORDER BY date DESC, id DESC",
            (ingredient_id,),
        )
        rows = cursor.fetchall()
    return jsonify([serialize_usage(row) for row in rows])


@app.get("/api/ingredients/expiring")
def expiring_ingredients():
    raw_days = request.args.get("days", "3")
    try:
        days = max(int(raw_days), 0)
    except ValueError:
        return jsonify({"error": "days must be an integer"}), 422
    limit_date = (date.today() + timedelta(days=days)).isoformat()
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM ingredients WHERE expiry_date <= %s ORDER BY expiry_date ASC, id ASC",
            (limit_date,),
        )
        rows = cursor.fetchall()
    return jsonify([serialize_ingredient(row) for row in rows])


@app.get("/api/ingredients/low-stock")
def low_stock_ingredients():
    raw_threshold = request.args.get("threshold", "1")
    try:
        threshold = float(raw_threshold)
    except ValueError:
        return jsonify({"error": "threshold must be a number"}), 422
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM ingredients WHERE quantity <= %s ORDER BY quantity ASC, id ASC",
            (threshold,),
        )
        rows = cursor.fetchall()
    return jsonify([serialize_ingredient(row) for row in rows])


initialize_db()
seed_db_if_empty()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
