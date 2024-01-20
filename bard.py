import gradio as gr  # Import the Gradio library for creating interfaces

def upload_images(student_name, student_email, reg_number, image1, image2, image3):
    """Processes student information and images (replace with actual implementation later)"""
    # ... (Implement image processing and database integration here)
    return "Student data uploaded successfully!"  # This message won't be displayed

iface = gr.Interface(
    fn=upload_images,
    inputs=[
        gr.Textbox(lines=1, placeholder="Enter student name"),  # Textbox for student name
        gr.Textbox(lines=1, placeholder="Enter student email"),  # Textbox for student email
        gr.Textbox(lines=1, placeholder="Enter registration number"),  # Textbox for registration number
        gr.Image(type="numpy", label="Upload Image 1"),  # Button for uploading image 1
        gr.Image(type="numpy", label="Upload Image 2"),  # Button for uploading image 2
        gr.Image(type="numpy", label="Upload Image 3"),  # Button for uploading image 3
        gr.Button("Submit"),  # Submit button to trigger the upload process
    ],
    outputs=None,  # No visual output
    title="Student Information and Image Upload",  # Interface title (centered by default)
    live=True,  # Enables live updates as input values change
)

iface.launch(share=True)  # Launches and shares the interface