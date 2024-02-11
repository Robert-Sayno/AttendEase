# Import necessary libraries
from flask import Flask, render_template, request, flash
import mysql.connector
import os
import tempfile
import shutil


# Create a Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Add a secret key for flash messages

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
            # Create a temporary directory and save images
            temp_dir = tempfile.mkdtemp()
            image_paths = []
            for i, img in enumerate([request.files['image1'], request.files['image2'], request.files['image3']]):
                image_path = os.path.join(temp_dir, f"image_{i+1}.jpg")
                img.save(image_path)
                image_paths.append(image_path)

            # Insert student data and image paths into the database
            sql = "INSERT INTO students (name, email, reg_number, image_paths) VALUES (%s, %s, %s, %s)"
            val = (request.form['student_name'], request.form['student_email'],
                   request.form['reg_number'], ",".join(image_paths))
            mycursor.execute(sql, val)
            mydb.commit()

            flash('Student details successfully uploaded!', 'success')  # Add this line for notification

        except mysql.connector.Error as err:
            print("Database error:", err)
            flash('Failed to upload student details!', 'error')  # Add this line for notification
        except Exception as e:
            print("Unexpected error:", e)
            flash('Failed to upload student details!', 'error')  # Add this line for notification
        finally:
            # Clean up temporary files
            shutil.rmtree(temp_dir, ignore_errors=True)

    return render_template('upload.html')

@app.route('/students')
def students():
    # Fetch student details from the database (modify this based on your actual database schema)
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM students")
    students_data = mycursor.fetchall()

    return render_template('students.html', students=students_data)

@app.route('/view_details/<int:id>', methods=['GET'])
def view_details(id):
    # Your logic to fetch student details from the database based on the id goes here

    # For now, let's pass a dummy data to the template
    dummy_student_data = {
        'id': id,
        'name': 'Dummy Name',
        'email': 'dummy@example.com',
        'reg_number': '12345'
        # Add other fields as needed
    }

    return render_template('view_details.html', student=dummy_student_data)

@app.route('/edit_student/<int:id>')
def edit_student(id):
    # Fetch the student details from the database based on the given id
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    student_data = mycursor.fetchone()

    if not student_data:
        # If the student does not exist, redirect to the students list
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

@app.route('/delete_student/<int:id>')
def delete_student(id):
    # Fetch the student details from the database based on the given id
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    student_data = mycursor.fetchone()

    if not student_data:
        # If the student does not exist, redirect to the students list
        return redirect(url_for('students'))

    if request.method == 'GET':
        return render_template('confirm_delete.html', student=student_data)
    elif request.method == 'POST':
        # Delete the student from the database based on the given id
        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM students WHERE id = %s", (id,))
        mydb.commit()

        return redirect(url_for('students'))

if __name__ == '__main__':
    app.run(debug=True, port=5009)
