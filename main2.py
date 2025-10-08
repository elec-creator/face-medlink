from deepface import DeepFace
import matplotlib.pyplot as plt
import cv2
import time

# List of available backends, models, and distance metrics
backends = ["opencv", "ssd", "dlib", "mtcnn", "retinaface"]
models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
metrics = ["cosine", "euclidean", "euclidean_l2"]

# Path to the image for face recognition
img = "Data/hendra/hendra.jpg"


def realtime_face_recognition():
    # Define a video capture object
    vid = cv2.VideoCapture(0)

    # variabel buat FPS
    prev_time = 0

    while True:
        # Capture the video frame by frame
        ret, frame = vid.read()
        if not ret:
            break

        # Hitung waktu sekarang
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
        prev_time = curr_time

        # Perform face recognition on the captured frame
        people = DeepFace.find(
                        img_path=frame, db_path="Data/",
                        model_name=models[2],
                        distance_metric=metrics[2],
                        enforce_detection=False)

        for person in people:
            if not person.empty:
                x = person['source_x'].iloc[0]
                y = person['source_y'].iloc[0]
                w = person['source_w'].iloc[0]
                h = person['source_h'].iloc[0]
            else:
                continue   # lewati frame kalau kosong

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            name = person['identity'][0].split('/')[1]
            cv2.putText(frame, name, (x, y-10), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)

        # Tampilkan FPS di kiri atas
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        # Display the resulting frame
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', 960, 720)
        cv2.imshow('frame', frame)

        # Check if the 'q' button is pressed to quit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()


# Run real-time recognition
realtime_face_recognition()
