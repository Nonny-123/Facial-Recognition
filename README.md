🎓 Student Identification and Exam Eligibility System

This project is an AI-powered application that combines a Student Registration System and Facial Recognition System to ensure only eligible students can access exam rooms. It registers student details and identifies students in real-time through facial recognition, enhancing security and streamlining exam processes.

📜 Table of Contents

Installation

Usage

System Features

Technologies Used

Future Improvements

Contributing

License

⚙️ Installation

Clone the repository:

git clone https://github.com/Nonny-123/Student-Identification-System.git
cd Student-Identification-System

Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

🚀 Usage

Run the Streamlit app:

streamlit run student_identification_app.py

Access the app:
The app will run locally at:

http://localhost:8501

🔍 System Features

Student Registration:

Register students by entering their name, contact information, student ID, and uploading an image.

Save student details and photos for future identification.

Facial Recognition:

Identify students in real-time through a live video feed.

Check student eligibility for exams and raise alerts for unregistered students.

Security Features:

Accurate identification powered by DeepFace with the Facenet model.

Alerts for unrecognized students to prevent unauthorized access.

🏠 Technologies Used

Python 🐍

Streamlit ⚡

DeepFace 🤖

OpenCV 🖼️

JSON 📂

📌 Future Improvements

Implement a secure student database.

Add multi-factor authentication.

Improve the UI with more detailed student information.

🤝 Contributing

Contributions are welcome! Feel free to fork the repo, open issues, and submit a pull request.

🐝 License

This project is licensed under the MIT License.

👨‍💻 Developed by Okonji Chukwunonyelim Gabriel.

