from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # замени на свой ключ

# Функция для подключения к базе
def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# Главная страница
@app.route("/")
def index():
    topics = ["Ввод и вывод данных", "Условные операторы", "Циклы", "Функции", "Списки", "Словари"]
    return render_template("index.html", topics=topics, username=session.get("username"))

# Регистрация
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = get_db()
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash("Регистрация успешна! Войдите.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Имя пользователя уже существует.")
        finally:
            conn.close()

    return render_template("register.html")

# Вход
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["username"] = user["username"]
            return redirect(url_for("index"))
        else:
            flash("Неверное имя или пароль.")

    return render_template("login.html")

# Выход
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
