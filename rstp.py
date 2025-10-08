import cv2

# Ganti dengan alamat RTSP IP Webcam
rtsp_url = "rtsp://10.173.31.141:8080/h264_ulaw.sdp"

cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Gagal membuka RTSP stream!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Tidak bisa membaca frame dari stream.")
        break

    cv2.imshow("IP Webcam Stream", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
