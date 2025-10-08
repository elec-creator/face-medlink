from flask import Flask, render_template, request, jsonify
from deepface import DeepFace
import cv2, os, base64, numpy as np, time

app = Flask(__name__)

UPLOAD_PATH = "uploads"
DB_PATH = "Data"
os.makedirs(UPLOAD_PATH, exist_ok=True)
os.makedirs(DB_PATH, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/save_face', methods=['POST'])
def save_face():
    try:
        data = request.get_json()
        name = data['name']
        img_data = data['image'].split(',')[1]
        img_bytes = base64.b64decode(img_data)
        img_array = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # buat folder baru untuk user jika belum ada
        user_folder = os.path.join(DB_PATH, name)
        os.makedirs(user_folder, exist_ok=True)

        # hitung jumlah file agar tidak overwrite
        count = len(os.listdir(user_folder))
        file_path = os.path.join(user_folder, f"{count+1}.jpg")

        # simpan foto
        cv2.imwrite(file_path, img)
        return jsonify({"status": "ok", "message": f"Foto {count+1} tersimpan"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/recognize', methods=['POST'])
def recognize():
    try:
        start = time.time()

        data = request.get_json()
        img_data = data['image'].split(',')[1]
        img_bytes = base64.b64decode(img_data)
        img_array = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        image_path = os.path.join(UPLOAD_PATH, "user_upload.jpg")
        cv2.imwrite(image_path, img)

        people = DeepFace.find(
            img_path=image_path,
            db_path=DB_PATH,
            model_name="Facenet512",
            distance_metric="cosine",
            enforce_detection=False
        )

        duration = time.time() - start
        print(f"🔍 Pencocokan selesai dalam {duration:.2f} detik")

        if not people[0].empty:
            identity = people[0]['identity'][0]
            name = os.path.basename(os.path.dirname(identity))
            return jsonify({"status": "match", "name": name})
        else:
            return jsonify({"status": "no_match", "name": None})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
