from flask import Flask, render_template, request, redirect, send_from_directory
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('suggestions.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            suggestion TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/download-resume')
def download_resume():
    return send_from_directory(directory='static/resume', path='Manoj_hp_resume.pdf', as_attachment=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Education')
def Education():
    return render_template('Education.html')

@app.route('/Certificates')
def Certificates():
    return render_template('Certificates.html')

@app.route('/suggestion', methods=['GET', 'POST'])
def suggestion():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        suggestion_text = request.form['suggestion']

        conn = sqlite3.connect('suggestions.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO suggestions (name, email, suggestion) VALUES (?, ?, ?)',
                       (name, email, suggestion_text))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('suggestion.html')

if __name__ == '__main__':
    app.run(debug=True)
