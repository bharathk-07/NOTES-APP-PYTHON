from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ---------------- DATABASE ---------------- #

def init_db():

    conn = sqlite3.connect("notes.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            date TEXT,
            favorite INTEGER DEFAULT 0,
            trash INTEGER DEFAULT 0

        )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ---------------- #

@app.route('/')
def index():

    conn = sqlite3.connect("notes.db")
    c = conn.cursor()

    c.execute(
        "SELECT * FROM notes WHERE trash=0 ORDER BY id DESC"
    )

    notes = c.fetchall()

    conn.close()

    return render_template("index.html", notes=notes)

# ---------------- ADD NOTE ---------------- #

@app.route('/add', methods=['POST'])
def add_note():

    title = request.form['title']
    content = request.form['content']

    date = datetime.now().strftime("%d %b %Y | %I:%M %p")

    conn = sqlite3.connect("notes.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO notes(title, content, date) VALUES(?,?,?)",
        (title, content, date)
    )

    conn.commit()
    conn.close()

    return redirect('/')

# ---------------- EDIT NOTE ---------------- #

@app.route('/edit/<int:id>', methods=['POST'])
def edit_note(id):

    title = request.form['title']
    content = request.form['content']

    conn = sqlite3.connect("notes.db")
    c = conn.cursor()

    c.execute(
        "UPDATE notes SET title=?, content=? WHERE id=?",
        (title, content, id)
    )

    conn.commit()
    conn.close()

    return redirect('/')

# ---------------- FAVORITE ---------------- #

@app.route('/favorite/<int:id>')
def favorite_note(id):

    conn = sqlite3.connect("notes.db")
    c = conn.cursor()

    c.execute(
        """
        UPDATE notes
        SET favorite =
        CASE
            WHEN favorite=0 THEN 1
            ELSE 0
        END
        WHERE id=?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')

# ---------------- FAVORITES PAGE ---------------- #

@app.route('/favorites')
def favorites():

    conn = sqlite3.connect("notes.db")
    c = conn.cursor()

    c.execute(
        """
        SELECT * FROM notes
        WHERE favorite=1
        AND trash=0
        ORDER BY id DESC
        """
    )

    notes = c.fetchall()

    conn.close()

    return render_template("index.html", notes=notes)

# ---------------- DELETE ---------------- #

@app.route('/delete/<int:id>')
def delete_note(id):

    conn = sqlite3.connect("notes.db")
    c = conn.cursor()

    c.execute(
        "UPDATE notes SET trash=1 WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')

# ---------------- TRASH ---------------- #

@app.route('/trash')
def trash():

    conn = sqlite3.connect("notes.db")
    c = conn.cursor()

    c.execute(
        """
        SELECT * FROM notes
        WHERE trash=1
        ORDER BY id DESC
        """
    )

    notes = c.fetchall()

    conn.close()

    return render_template("index.html", notes=notes)

# ---------------- RESTORE ---------------- #

@app.route('/restore/<int:id>')
def restore_note(id):

    conn = sqlite3.connect("notes.db")
    c = conn.cursor()

    c.execute(
        "UPDATE notes SET trash=0 WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/trash')

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)