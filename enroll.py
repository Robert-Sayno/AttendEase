import face_recognition
import mysql.connector
from mysql.connector import Error

# Connect to MySQL database
try:
    connection = mysql.connector.connect(host='localhost',
                                         database='AttendEase',
                                         user='root',
                                         password='')

    if connection.is_connected():
        cursor = connection.cursor()

        # Create a table to store face features
        cursor.execute('''CREATE TABLE IF NOT EXISTS individuals
                        (id INT AUTO_INCREMENT PRIMARY KEY,
                         name VARCHAR(255) NOT NULL,
                         face_features TEXT NOT NULL)''')
        connection.commit()

        def enroll_individual(name, image_path):
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
                print(f"Enrolled {name} successfully.")
            else:
                print(f"Error: Could not enroll {name}. More or less than one face found.")

except Error as e:
    print("Error:", e)

finally:
    # Close the database connection
    if connection.is_connected():
        cursor.close()
        connection.close()
