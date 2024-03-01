from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Connect to your database (replace placeholders with your credentials)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="AttendEase"
)

@app.route('/', methods=['GET', 'POST'])
def upload_images():
    if request.method == 'POST':
        mycursor = mydb.cursor()

        try:
            images_directory = "/opt/lampp/htdocs/AttendEase/images"
            image_paths = []

            for i in range(1, 4):  # Updated loop range
                img = request.files.get(f'image{i}')
                if img:
                    original_filename = secure_filename(img.filename)
                    image_path = os.path.join(images_directory, original_filename)
                    img.save(image_path)
                    image_paths.append(image_path)
                    print(f"Saved image: {image_path}")

            sql = "INSERT INTO students (name, email, reg_number, image_paths) VALUES (%s, %s, %s, %s)"
            val = (request.form['student_name'], request.form['student_email'],
                   request.form['reg_number'], ",".join(image_paths))
            mycursor.execute(sql, val)
            mydb.commit()

            flash('Student details successfully uploaded!', 'success')

        except mysql.connector.Error as err:
            print("Database error:", err)
            flash('Failed to upload student details!', 'error')
        except Exception as e:
            print("Unexpected error:", e)
            flash('Failed to upload student details!', 'error')

    return render_template('upload.html')

@app.route('/students')
def students():
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM students")
    students_data = mycursor.fetchall()
    return render_template('students.html', students=students_data)

@app.route('/view_details/<int:id>', methods=['GET'])
def view_details(id):
    # Fetch student details from the database based on the given id
    # Replace the following lines with your actual database query logic
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    student_data = mycursor.fetchone()

    return render_template('view_details.html', student=student_data)

@app.route('/edit_student/<int:id>')
def edit_student(id):
    # Fetch the student details from the database based on the given id
    # Replace the following lines with your actual database query logic
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    student_data = mycursor.fetchone()

    if not student_data:
        return redirect(url_for('students'))

    return render_template('edit_student.html', student=student_data)

@app.route('/update_student/<int:id>', methods=['POST'])
def update_student(id):
    # Update the student details in the database based on the given id
    mycursor = mydb.cursor()
    mycursor.execute("UPDATE students SET name=%s, email=%s, reg_number=%s WHERE id=%s",
                     (request.form['student_name'], request.form['student_email'], request.form['reg_number'], id))
    mydb.commit()

    return redirect(url_for('students'))

@app.route('/delete_student/<int:id>', methods=['GET', 'POST'])
def delete_student(id):
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    student_data = mycursor.fetchone()

    if not student_data:
        return redirect(url_for('students'))

    if request.method == 'POST':
        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM students WHERE id = %s", (id,))
        mydb.commit()
        return redirect(url_for('students'))

    return render_template('confirm_delete.html', student=student_data)

if __name__ == '__main__':
    app.run(debug=True, port=5009)
