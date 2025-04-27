# Flask Facial Recognition App

Welcome to the **Flask Facial Recognition App** repository!  
This project demonstrates a lightweight web application for real-time facial recognition using Flask, OpenCV, and deep learning models.

## Table of Contents
- [About the Project](#about-the-project)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## About the Project

This project creates a simple, user-friendly web interface where users can upload an image and recognize faces.  
It is useful for quickly prototyping face recognition systems, learning Flask development.

## Features

- Face detection and recognition
- Upload and process images
- Pre-trained Machine learning models integration
- Simple and responsive web UI

## Getting Started

These instructions will help you set up the project on your local machine.

### Prerequisites

Make sure you have the following installed:
- Python 3.8+ (Python3.10 recommended)
- pip
- virtualenv (recommended)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/gsphanitalpak/facial-recognition-flask-app.git
    cd facial-recognition-flask-app
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **SVM Pre-trained model** is saved inside the `/models` directory.  

### Running the Application

Run the Flask app:

```bash
python app.py
```

Navigate to `http://127.0.0.1:5000/` in your browser.

---

## Project Structure

```plaintext
flask-facial-recognition/
│
├── app.py                  # Main Flask application
├── requirements.txt         # Python dependencies
├── README.md                # Project overview
├── static/                  # Static files (CSS, JS, images)
├── templates/               # HTML templates (Jinja2)
└── models/                  # Pre-trained model

```

---

## Usage

- **Upload Image**: Upload an image to detect and recognize faces.
- **Extend Models**: Integrate better models like FaceNet, DeepFace, or your own trained models.

> **Note:** This app is intended for learning and prototyping purposes. For production use, ensure security, optimization, and ethical AI practices.

---

## Contributing

Contributions are welcome!  
Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on the code of conduct, and the process for submitting pull requests.

If you have any suggestions or improvements, feel free to open an issue or a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

Created and maintained by **Santhosh Phanitalpak Gandhala (https://github.com/gsphanitalpak)**.  
For any questions, feel free to reach out!
