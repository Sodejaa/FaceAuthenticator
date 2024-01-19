import sys
import cv2
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
from deepface import DeepFace

class FaceRecognitionApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize variables for face recognition
        self.face_recognition_active = True
        self.face_found = False
        self.counter = 0
        self.facenum = 0

        # Initialize video capture using OpenCV
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Set up the user interface
        self.init_ui()

    def init_ui(self):
        # Create buttons, labels, and layout
        self.startStop_button = QPushButton('Start/Stop Face Recognition', self)
        self.startStop_button.clicked.connect(self.toggle_face_recognition)
        
        self.newFace_button = QPushButton('Add New Face', self)
        self.newFace_button.clicked.connect(self.take_picture)

        self.quit_button = QPushButton('Quit', self)
        self.quit_button.clicked.connect(self.close_application)

        self.status_label = QLabel('Face Recognition Status: Active', self)

        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.newFace_button)
        layout.addWidget(self.startStop_button)
        layout.addWidget(self.quit_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.video_label)

        self.setLayout(layout)

        # Set up timer for updating the frame
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)  # Update frame every ~30 milliseconds (about 30 FPS)

        self.show()
    
    def take_picture(self):
        # Capture a single frame
        ret, frame = self.capture.read()

        if ret:
            # Save the captured frame as an image file in the 'faces' folder
            cv2.imwrite(f'faces/face{self.facenum}.jpg', frame)
            print(f"Picture taken and saved as 'faces/face{self.facenum}.jpg'")

            self.facenum += 1
            self.load_faces()

    def toggle_face_recognition(self):
        # Toggle face recognition status
        self.face_recognition_active = not self.face_recognition_active
        status = 'Active' if self.face_recognition_active else 'Inactive'  
        self.status_label.setText(f'Face Recognition Status: {status}')

    def close_application(self):
        # Release video capture and stop the timer when the application is closed
        self.capture.release()
        self.timer.stop()
        self.close()

    def update_frame(self):
        # Update frame and perform face recognition if active
        ret, frame = self.capture.read()

        if ret:
            if self.face_recognition_active and self.counter % 30 == 0:
                try:
                    self.check_face(frame)
                except ValueError:
                    pass
            self.counter += 1

            # Display "Face Found" or "Face Not Found" text on the frame
            if self.face_found:
                cv2.putText(frame, "Face Found", (5, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
            else:
                cv2.putText(frame, "Face Not Found", (5, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)

            # Display the frame in the GUI
            self.display_frame(frame)
            

    def check_face(self, frame):
        # Iterate over all faces dynamically loaded during runtime
        for userface in self.faces:
            try:
                if DeepFace.verify(frame, userface)['verified']:
                    self.face_found = True
                    return  # Exit the loop if a face is found
            except ValueError:
                pass  # Continue to the next face if there is an error
        self.face_found = False
            
    def load_faces(self):
    # Load faces from the 'faces' folder dynamically
        faces_folder = 'faces'
        self.faces = []

        for face_filename in os.listdir(faces_folder):
            if face_filename.endswith(('.jpg', '.jpeg', '.png')):
                face_path = os.path.join(faces_folder, face_filename)
                face = cv2.imread(face_path)
                if face is not None:
                    self.faces.append(face)

    def display_frame(self, frame):
        # Convert the OpenCV frame to a QImage and display it in the GUI
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_img)
        self.video_label.setPixmap(pixmap)

if __name__ == '__main__':
    # Initialize the PyQt application, load a test face image, and create the main application window
    app = QApplication(sys.argv)
    main_window = FaceRecognitionApp()
    main_window.load_faces()  # Load faces at the beginning
    sys.exit(app.exec_())