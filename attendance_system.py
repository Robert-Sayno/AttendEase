import cv2
import face_recognition
from datetime import datetime
import mysql.connector
import os

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="AttendEase"
)

cursor = db.cursor()

# Load known faces from the database
cursor.execute("SELECT id, name, image_paths FROM students")
students_data = cursor.fetchall()

# Specify the location of the images directory
image_directory = "/opt/lampp/htdocs/AttendEase/images"

# Construct paths for known images
known_image_paths = [os.path.join(image_directory, os.path.basename(path.strip())) for data in students_data for path in data[2].split(',')]

# Load images and corresponding face encodings
known_images = []
known_face_encodings = []

for path in known_image_paths:
    try:
        image = face_recognition.load_image_file(path)
        known_images.append(image)

        # Extract face encodings
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)

    except FileNotFoundError:
        print(f"Warning: File not found at path {path}")
    except Exception as e:
        print(f"Error loading image from path {path}: {e}")

# Open the USB camera with index 2
video_capture = cv2.VideoCapture(2)

while True:
    # Capture each frame from the webcam
    ret, frame = video_capture.read()

    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop through each face found in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare the current face encoding with the known face encodings
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        # Check if there is a match
        if True in matches:
            # Get the index of the first match
            first_match_index = matches.index(True)

            # Extract student information from the matched data
            student_id = students_data[first_match_index][0]
            student_name = students_data[first_match_index][1]

            # Record attendance in the database
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO attendance (student_id, time) VALUES (%s, %s)", (student_id, current_time))
            db.commit()

            print(f"Attendance recorded for {student_name}")

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
video_capture.release()
cv2.destroyAllWindows()

# Close the database connection
cursor.close()
db.close()
