import cv2
import face_recognition
from datetime import datetime
import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="AttendEase"
)

cursor = db.cursor()

# Load known faces from the database
cursor.execute("SELECT id, name, face_encoding FROM students")
students_data = cursor.fetchall()

# Extract face encodings and student IDs from the fetched data
known_face_encodings = [bytes.fromhex(data[2]) for data in students_data]
known_student_ids = [data[0] for data in students_data]

# Open the webcam
video_capture = cv2.VideoCapture(0)

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
            student_id = known_student_ids[first_match_index]
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
