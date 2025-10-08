# 🧠 Face-Medlink: Face Recognition Access System for Raspberry Pi

Face-Medlink is a **Flask-based face recognition system** using the **DeepFace** and **OpenCV** libraries.  
It supports both **static image recognition** and **real-time webcam recognition**, optimized for use on **Raspberry Pi** (e.g., for automatic gate access, attendance, or identity verification systems).

---

## 🚀 Features
- Face recognition using DeepFace (supports multiple models)
- Real-time detection via USB or Pi Camera
- Easy integration with hardware (e.g., Arduino / ESP32 via serial)
- Lightweight Flask web interface
- Compatible with Raspberry Pi 3/4/5

---

## 🧩 Requirements

### 🔧 Hardware
- Raspberry Pi 3 B+ / 4 / 5  
- USB webcam or Pi Camera  
- Stable internet connection (for installing dependencies)

### 🧠 Software
- Python 3.8+  
- pip (Python package manager)  
- Git (for cloning this repo)

---

## 🛠 Installation (Raspberry Pi)

Open your Pi terminal and run the following commands:

```bash
# 1️⃣ Update and install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git libatlas-base-dev -y

# 2️⃣ Clone this repository
git clone https://github.com/elec-creator/face-medlink.git
cd face-medlink

# 3️⃣ Install Python libraries
pip3 install -r requirements.txt

# 4️⃣ Run the application
python3 main.py
