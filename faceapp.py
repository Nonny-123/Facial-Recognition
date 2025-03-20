import streamlit as st
import os
import json
from PIL import Image
from deepface import DeepFace
import cv2
import tempfile
import time

# Specify the folder where known faces are saved
KNOWN_FACES_DIR = "known_faces"
STUDENT_DB = "known_faces"
STUDENT_DATA_FILE = "student_data.json"

# Create the folder if it doesn't exist
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

# Function to save the image with the student's name
def save_student_image(student_name, img_file):
    clean_name = "".join([c if c.isalnum() else "_" for c in student_name])
    img_path = os.path.join(KNOWN_FACES_DIR, f"{clean_name}.jpg")
    
    with open(img_path, "wb") as f:
        f.write(img_file.getbuffer())

    return img_path

# Function to save student metadata to a JSON file
def save_student_data(student_name, email, receipt_number, identification_number):
    data_file = STUDENT_DATA_FILE

    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            student_data = json.load(f)
    else:
        student_data = {}

    student_data[student_name] = {
        "image": f"{student_name}.jpg",
        "email": email,
        "receipt_number": receipt_number,
        "identification_number": identification_number
    }

    with open(data_file, 'w') as f:
        json.dump(student_data, f, indent=4)

# Load student data from the JSON file
def load_student_data():
    if os.path.exists(STUDENT_DATA_FILE):
        with open(STUDENT_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# Initialize session state for controlling the video stream
if 'stop_recording' not in st.session_state:
    st.session_state['stop_recording'] = False

last_student_name = None  # Variable to store the last identified student

# Function to capture real-time video from the webcam
def capture_video_without_display():
    global last_student_name
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        st.error("Error: Could not access the webcam.")
        return

    st.write("Starting live video stream for facial recognition...")

    stop_button_placeholder = st.empty()
    if stop_button_placeholder.button("Stop Recording"):
        st.session_state['stop_recording'] = True

    while cap.isOpened():
        if st.session_state['stop_recording']:
            st.write("Video recording stopped.")
            break

        ret, frame = cap.read()
        if not ret:
            st.error("Error: Could not read frame from the webcam.")
            break
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_img:
            img_pil = Image.fromarray(frame_rgb)
            img_pil.save(temp_img.name)

        try:
            student_result = DeepFace.find(img_path=temp_img.name, db_path=STUDENT_DB, model_name="Facenet")
            student_data = load_student_data()

            if len(student_result) > 0 and not student_result[0].empty:
                best_match_student = student_result[0].iloc[0]
                image_path = best_match_student['identity']
                student_name = os.path.basename(image_path).split('.')[0]

                # Replace underscores with spaces for JSON lookup
                json_lookup_name = student_name.replace("_", " ")

                if json_lookup_name != last_student_name:
                    st.success(f"Student Identified: {json_lookup_name} ✅")
                    last_student_name = json_lookup_name
                    
                    if json_lookup_name in student_data:
                        receipt_number = student_data[json_lookup_name].get("receipt_number", "N/A")
                        email = student_data[json_lookup_name].get("email", "N/A")
                        
                        # info_message = f"""
                        #     Name: {json_lookup_name}\n
                        #     Receipt Number: {receipt_number}\n
                        #     Email: {email}
                        #     """
                        info_message = f"Student With Name: {json_lookup_name}, Receipt Number: {receipt_number}, Email: {email} Meets all the requirements to be eilgible for semester exam hence can proceed into the hall."
                        st.info(info_message)
                    else:
                        st.warning("No additional information available for this student.")
            else:
                if last_student_name is not None:
                    st.error("Student hasn't met exam requirement hence not eligible for semester exam. ❌")
                    last_student_name = None

        except Exception as e:
            print(f"Error during recognition: {e}")

        time.sleep(0.1)

    cap.release()


st.title("AI-Based Facial Recognition for Student Verification")

# Layout the Streamlit app with tabs
tab1, tab2 = st.tabs(["Student Registration", "Facial Recognition"])

# Tab 1: Student Registration
with tab1:
    st.header("Register New Student")

    with st.form("student_registration"):
        student_name = st.text_input("Enter Student Name")
        email = st.text_input("Email Address")
        receipt_number = st.text_input("Receipt Number")
        identification_number = st.text_input("Identification Number")
        img_file = st.file_uploader("Upload Student Image", type=["jpg", "jpeg", "png"])

        submit_button = st.form_submit_button("Register Student")

    if submit_button:
        if student_name and img_file and email and receipt_number and identification_number:
            saved_image_path = save_student_image(student_name, img_file)
            save_student_data(student_name, email, receipt_number, identification_number)

            st.success(f"Student {student_name} registered successfully!")
            st.image(saved_image_path, caption=f"Image saved as {student_name}.jpg")
        else:
            st.error("Please provide all the required information (name, email, receipt number, identification number, and image).")

# Tab 2: Facial Recognition
with tab2:
    st.header("Verify Student")

    if st.button("Start Live Face Recognition"):
        st.session_state['stop_recording'] = False
        capture_video_without_display()