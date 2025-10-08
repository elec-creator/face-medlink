from flask import Flask
import cv2
from deepface import DeepFace
import os

app = Flask(__name__)

# RTSP URL CCTV (ubah sesuai kamera)
RTSP_URL = "rtsp://10.173.31.141:8080/h264_ulaw.sdp"

UPLOAD_PATH = r"E:\PYDBASE\face\uploads\capture.jpg"
DB_PATH = r"E:\PYDBASE\face\Data"

@app.route("/capture", methods=["GET"])
def capture_and_recognize():
    # 1. Ambil frame dari CCTV
    cap = cv2.VideoCapture(RTSP_URL)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("❌ Gagal capture dari CCTV")
        return "fail", 500

    # 2. Simpan frame ke uploads
    cv2.imwrite(UPLOAD_PATH, frame)
    print("✅ Foto disimpan:", UPLOAD_PATH)

    # 3. Face Recognition
    try:
        people = DeepFace.find(
            img_path=UPLOAD_PATH,
            db_path=DB_PATH,
            model_name="Facenet512",
            distance_metric="euclidean_l2",
            enforce_detection=False
        )
        
        if not people[0].empty:
            identity = people[0]['identity'][0]
            name = os.path.basename(os.path.dirname(identity))
            print("🎯 Wajah terdeteksi:", name)
        else:
            print("⚠️ Tidak ada kecocokan wajah di database")

    except Exception as e:
        print("❌ Error Face Recognition:", str(e))

    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
