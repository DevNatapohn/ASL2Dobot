# ASL2Dobot - Installation Guide
**ASL2Dobot** is a Python 3.x project for real-time Hand Gesture recognition and controlling a Dobot robotic arm. It supports **Windows, Linux, Raspberry Pi** and connects with **Dobot**.

## 0️⃣ Git Clone Project
```bash
git clone https://github.com/YourUsername/ASL2Dobot.git
cd ASL2Dobot
```

## 1️⃣ System Setup
🔹 **Linux / Raspberry Pi**
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3-pip python3-dev
```
🔹 **Windows** — Make sure Python 3.x is installed and added to PATH.

## 2️⃣ Create Virtual Environment
```bash
python3 -m venv venv
# Activate
# Linux / Raspberry Pi
source venv/bin/activate
# Windows
venv\Scripts\activate
```

## 3️⃣ Install Dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4️⃣ Verify Installation
```bash
python -c "import cv2, mediapipe, tensorflow as tf; print(tf.__version__)"
```
- TensorFlow should be `2.16.1`
- OpenCV and Mediapipe should import without errors

## 5️⃣ Run
```bash
python main.py
```
