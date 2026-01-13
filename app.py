from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime
import subprocess
import sys

app = Flask(__name__)
app.secret_key = "attendance_secret"

@app.route('/')
def index():
    return render_template('index.html', attendance_data=None, no_data=False, selected_date='')

# ▶ Register Face
@app.route('/register_face')
def register_face():
    subprocess.Popen([sys.executable, "get_faces_from_camera_tkinter.py"])
    flash("Face registration window opened")
    return redirect(url_for('index'))

# ▶ Extract Features
@app.route('/extract_features')
def extract_features():
    subprocess.run([sys.executable, "features_extraction_to_csv.py"])
    flash("Face features extracted successfully")
    return redirect(url_for('index'))

# ▶ Start Attendance
@app.route('/start_attendance')
def start_attendance():
    subprocess.Popen([sys.executable, "attendance_taker.py"])
    flash("Attendance system started")
    return redirect(url_for('index'))

# ▶ View Attendance
@app.route('/attendance', methods=['POST'])
def attendance():
    selected_date = request.form.get('selected_date')
    formatted_date = datetime.strptime(selected_date, '%Y-%m-%d').strftime('%Y-%m-%d')

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, time FROM attendance WHERE date = ?", (formatted_date,))
    attendance_data = cursor.fetchall()
    conn.close()

    if not attendance_data:
        return render_template('index.html', no_data=True, selected_date=selected_date)

    return render_template('index.html', attendance_data=attendance_data, selected_date=selected_date)

if __name__ == '__main__':
    app.run(debug=True)
