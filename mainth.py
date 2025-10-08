from deepface import DeepFace
import cv2
import time
import threading
import queue

# List of models & metrics
models = ["Facenet512"]
metrics = ["euclidean_l2"]

# Shared queue untuk komunikasi antar thread
frame_queue = queue.Queue()
result_queue = queue.Queue()

def capture_frames():
    vid = cv2.VideoCapture(0)
    while True:
        ret, frame = vid.read()
        if not ret:
            break
        if not frame_queue.full():
            frame_queue.put(frame)
        # tekan q untuk keluar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    vid.release()

def process_frames():
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            try:
                people = DeepFace.find(
                    img_path=frame,
                    db_path="Data/",
                    model_name=models[0],
                    distance_metric=metrics[0],
                    enforce_detection=False
                )

                for person in people:
                    if not person.empty:
                        x = person['source_x'].iloc[0]
                        y = person['source_y'].iloc[0]
                        w = person['source_w'].iloc[0]
                        h = person['source_h'].iloc[0]
                        name = person['identity'][0].split('/')[1]
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.putText(frame, name, (x, y-10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                result_queue.put(frame)
            except Exception as e:
                print("Error:", e)

def display_frames():
    prev_time = 0
    while True:
        if not result_queue.empty():
            frame = result_queue.get()

            # hitung FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
            prev_time = curr_time

            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

# Jalankan thread paralel
t1 = threading.Thread(target=capture_frames)
t2 = threading.Thread(target=process_frames)
t3 = threading.Thread(target=display_frames)

t1.start()
t2.start()
t3.start()
