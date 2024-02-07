import cv2
import threading

class VideoCaptureWithThread:
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        self.frame = None

    def update(self):
        while True:
            if self.capture.isOpened():
                (status, frame) = self.capture.read()
                if status:
                    self.frame = frame
            else:
                print("Kamera açılamıyor.")
                break

    def read(self):
        return self.frame

    def release(self):
        self.capture.release()

# Kamera indeksi veya yolunu belirtin
video_source = "/dev/video1"

# VideoCaptureWithThread sınıfını kullanarak kamera erişimi
cap = VideoCaptureWithThread(video_source)
while True:
    frame = cap.read()

    # Burada frame üzerinde işlemler yapabilirsiniz

    if frame is not None:
        cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
