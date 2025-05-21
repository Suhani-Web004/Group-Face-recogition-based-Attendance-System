from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required to use sessions

# ---------- ROUTES ----------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)', (name, email, message))
        conn.commit()
        conn.close()

        return redirect(url_for('thank_you'))
    return render_template('contact.html')

# Enhanced UI Pages
@app.route('/feature2')
def feature2():
    return render_template('feature2.html')

@app.route('/about2')
def about2():
    return render_template('about2.html')

@app.route('/contact2')
def contact2():
    return render_template('contact2.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html')

@app.route('/teacher')
def teacher():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('teacher.html')

@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')

@app.route('/takeimage')
def takeimage():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('takeimage.html')

@app.route('/live')
def live():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('live.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# ---------- AUTH ROUTES ----------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('home'))  # ✅ Redirects to home.html
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit()
            session['username'] = username
            return redirect(url_for('home'))
        except sqlite3.IntegrityError:
            return render_template('signup.html', error="Username already exists")
        finally:
            conn.close()

    return render_template('signup.html')

# ---------- DATABASE INITIALIZATION ----------

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# ---------- MAIN ----------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
