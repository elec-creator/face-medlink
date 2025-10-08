from deepface import DeepFace
import cv2

# List of available models and distance metrics
models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
metrics = ["cosine", "euclidean", "euclidean_l2"]

# Path foto yang mau dicek (misalnya hasil upload)
test_img = "uploads/user_upload.jpg"

def check_face(image_path):
    try:
        # Cari wajah di database
        people = DeepFace.find(
                        img_path=image_path, 
                        db_path="Data/",   # database wajah referensi
                        model_name=models[2],     # Facenet512
                        distance_metric=metrics[2], # euclidean_l2
                        enforce_detection=False
                    )
        
        if not people[0].empty:
            # Ambil nama identitas pertama yang cocok
            identity = people[0]['identity'][0]
            name = identity.split('/')[1]   # ambil nama folder
            print("Wajah cocok dengan:", name)

            # tampilkan gambar hasil deteksi (opsional)
            img = cv2.imread(image_path)
            cv2.imshow("Detected Face", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        else:
            print("Tidak ada kecocokan ditemukan.")

    except Exception as e:
        print("Error:", str(e))


# Jalankan pengecekan
check_face(test_img)
