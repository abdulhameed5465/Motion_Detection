# Motion Detection System

A Python-based computer vision application designed to detect real-time movement of objects or people using a camera feed. The system monitors the video stream and logs detected movements dynamically.

## 🚀 Features
* **Real-Time Detection:** Smooth monitoring of objects and human movement via camera input.
* **Activity Logging:** Automatically documents motion events with timestamps in a dedicated log file (`motion_log.txt`).
* **Web UI / Application Entry:** Configured via an accessible interface script (`app.py`).

## 📁 Repository Structure
* **`app.py`** – The main execution script managing the application logic and potential interface.
* **`motion_log.txt`** – Automatically generated log tracking the timestamps of detected motion.
* **`recording/`** – Directory placeholder for saved clips or captured frames of detected activity.
* **`README.md`** – Project overview, setup guidelines, and documentation.
* **`LICENSE`** – Permissive open-source usage terms (MIT License).

## 🛠️ Prerequisites & Installation

### 1. Prerequisites
Ensure you have a working Python installation on your local machine.

### 2. Clone the Repository
Clone this repository to your local computer using Git or PyCharm:
```bash
git clone https://github.com/abdulhameed5465/Motion_Detection.git
cd Motion_Detection
```

### 3. Set Up Your Environment
Create and activate a fresh virtual environment within your project folder:
```bash
# Create a virtual environment
python -m venv .venv

# Activate on Windows (Command Prompt)
.venv\Scripts\activate
```

### 4. Install Dependencies
Make sure you have OpenCV installed in your virtual environment:
```bash
pip install opencv-python
```

## 💻 Usage
Run the main script to start the motion detection engine:
```bash
python app.py
```
* **Camera Access:** Grant camera permissions if prompted by your operating system.
* **Exit Application:** Press the designated close key (typically `q`) on your keyboard while focusing on the video frame window to safely stop the application.

## 📄 License
This project is licensed under the terms of the MIT License.
