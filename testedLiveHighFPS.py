import cv2
import time
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

# Roboflow API anahtarınız
api_key = "GiGwZjBmOMekt0xkE95u"

# Roboflow proje adı ve versiyon numarası
project_name = "bluefriendorenemy"
version_number = "3"

# API endpoint URL'si
url = f"https://detect.roboflow.com/{project_name}/{version_number}?api_key={api_key}"

# Kamera bağlantısını başlat
cap = cv2.VideoCapture(0)

# FPS ölçümü için zamanı başlat
start_time = time.time()
frames_processed = 0

while True:
    # Kameradan bir kare al
    ret, frame = cap.read()

    # Kare boyutunu azalt
    frame = cv2.resize(frame, (600, 340))

    # Kareyi Roboflow API'sine gönder
    _, img_encoded = cv2.imencode('.jpg', frame)
    m = MultipartEncoder(fields={'file': ("imageToUpload", img_encoded.tobytes(), "image/jpeg")})
    response = requests.post(url, data=m, headers={'Content-Type': m.content_type})

    # Yanıttan sonuçları al
    data = response.json()

    # İlk tahminin bilgilerini çıkar
    if 'predictions' in data and len(data['predictions']) > 0:
        prediction = data['predictions'][0]
        imWidth = int(prediction['width'])
        imHeight = int(prediction['height'])
        xp = int(prediction['x'])
        yp = int(prediction['y'])
        className = prediction['class']
        confidence = float(prediction['confidence'])

        # Dikdörtgen koordinatlarını hesapla
        start_x = xp - (imWidth / 2)
        start_y = yp - (imHeight / 2)
        end_x = xp + (imWidth / 2)
        end_y = yp + (imHeight / 2)

        # Sınıfa göre renk belirle
        if className == 'Human':
            color = (0, 255, 255)  # Sarı
        elif className == 'Friend':
            color = (0, 255, 0)  # Yeşil
        elif className == 'Enemy':
            color = (0, 0, 255)  # Kırmızı

        # Dikdörtgeni çiz
        cv2.rectangle(frame, (int(start_x), int(start_y)), (int(end_x), int(end_y)), color=color, thickness=2)

        # Etiketi ve güven değerini ekle
        label = f"{className}: {confidence:.2f}"
        cv2.putText(frame, label, (int(start_x), int(start_y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Sonucu göster
    cv2.imshow('Object Detection', frame)

    # FPS'i hesapla
    frames_processed += 1
    elapsed_time = time.time() - start_time
    if elapsed_time > 1:
        fps = frames_processed / elapsed_time
        print(f"FPS: {fps:.2f}")
        start_time = time.time()
        frames_processed = 0

    # 'q' tuşuna basıldığında döngüyü kır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamera bağlantısını kapat
cap.release()
cv2.destroyAllWindows()
