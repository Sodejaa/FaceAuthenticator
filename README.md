# Face Recognition App

This is a simple PyQt-based application that performs face recognition using the DeepFace library. The application captures video from the user's camera, allows them to add new faces to the dataset, and toggles face recognition on/off.

## Features

- **Start/Stop Face Recognition:** Toggle the face recognition system on and off.
- **Add New Face:** Capture a single frame and save it as a new face image in the 'faces' folder.
- **Quit:** Close the application.

## Requirements

- Python 3
- PyQt5
- OpenCV
- DeepFace

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Sodejaa/FaceAuthenticator
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    python main.py
    ```

## Usage

- Click the "Add New Face" button to capture and save a new face image. **Only works with the 'test1.jpg' at the moment (you can upload your own test1.jpg)**.
- Click the "Start/Stop Face Recognition" button to toggle the face recognition system.
- Click the "Quit" button to close the application.

## Notes

- Make sure to have a compatible camera connected to your system.
- Face images are saved in the 'faces' folder.

## Credits

- This application uses the [DeepFace](https://github.com/serengil/deepface) library for face recognition.

## License

This project is licensed under the [MIT License](LICENSE).

