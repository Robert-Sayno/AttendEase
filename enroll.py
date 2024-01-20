import gradio as gr
import mysql.connector  # Import MySQL connector
import cv2  # Import OpenCV for camera access
import os
import tempfile
import shutil

# Connect to your database (replace placeholders with your credentials)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="AttendEase"
)

def upload_images(student_name, student_email, reg_number, image1, image2, image3):
    """Processes student information and images, saves them to the database,
       and initiates face recognition and attendance recording."""

    mycursor = mydb.cursor()

    try:
        # Create a temporary directory and save images
        temp_dir = tempfile.mkdtemp()
        image_paths = []
        for i, img in enumerate([image1, image2, image3]):
            image_path = os.path.join(temp_dir, f"image_{i+1}.jpg")
            img.save(image_path)
            image_paths.append(image_path)

        # Insert student data and image paths into the database
        sql = "INSERT INTO students (name, email, reg_number, image_paths) VALUES (%s, %s, %s, %s)"
        val = (student_name, student_email, reg_number, ",".join(image_paths))
        mycursor.execute(sql, val)
        mydb.commit()

        # Start face recognition and attendance recording
        start_face_recognition(mycursor)

    except mysql.connector.Error as err:
        print("Database error:", err)
    except Exception as e:
        print("Unexpected error:", e)
    finally:
        # Clean up temporary files
        shutil.rmtree(temp_dir, ignore_errors=True)

def start_face_recognition(mycursor):
    """Accesses webcam, performs face detection and recognition,
       and records attendance if a match is found."""

    # ... (Implement face recognition logic here)

iface = gr.Interface(
    fn=upload_images,
    inputs=[
        gr.Textbox(lines=1, placeholder="Enter student name"),
        gr.Textbox(lines=1, placeholder="Enter student email"),
        gr.Textbox(lines=1, placeholder="Enter registration number"),
        gr.Image(type="numpy", label="Upload Image 1"),
        gr.Image(type="numpy", label="Upload Image 2"),
        gr.Image(type="numpy", label="Upload Image 3"),
        gr.Button("Submit"),
    ],
    outputs=None,
    title="Student Information and Image Upload",
    live=True,
)

iface.launch(share=True)