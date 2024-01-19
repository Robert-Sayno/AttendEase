import tkinter as tk
from tkinter import filedialog
import face_recognition
import mysql.connector
from mysql.connector import Error

def enroll_individual():
    name = name_entry.get()

    # Use file dialog to select an image for enrollment
    image_path = filedialog.askopenfilename(title="Select Image",
                                            filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

    if not image_path:
        return

    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(host='localhost',
                                             database='attendease_database',
                                             user='your_username',
                                             password='your_password')

        if connection.is_connected():
            cursor = connection.cursor()

            # Load the facial image for enrollment
            image = face_recognition.load_image_file(image_path)

            # Find face locations and face encodings
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            if len(face_encodings) == 1:
                # Convert the face features to a string for storage
                face_features_str = ','.join(map(str, face_encodings[0]))

                # Insert the data into the database
                cursor.execute("INSERT INTO individuals (name, face_features) VALUES (%s, %s)", (name, face_features_str))
                connection.commit()
                result_label.config(text=f"Enrolled {name} successfully.", fg='green')
            else:
                result_label.config(text=f"Error: More or less than one face found.", fg='red')

    except Error as e:
        result_label.config(text=f"Error: {e}", fg='red')

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()

# Create the main application window
app = tk.Tk()
app.title("AttendEase Enrollment")

# UI Components
name_label = tk.Label(app, text="Name:")
name_entry = tk.Entry(app)
enroll_button = tk.Button(app, text="Enroll", command=enroll_individual)
result_label = tk.Label(app, text="", fg='green')

# Place UI Components
name_label.grid(row=0, column=0, padx=10, pady=10)
name_entry.grid(row=0, column=1, padx=10, pady=10)
enroll_button.grid(row=1, column=0, columnspan=2, pady=10)
result_label.grid(row=2, column=0, columnspan=2, pady=10)

# Start the GUI event loop
app.mainloop()
