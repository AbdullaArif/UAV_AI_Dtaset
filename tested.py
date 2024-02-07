#bu kod bilgisayar kamerasindan ilk gordugu goruntuyu 1 kere detect edecek sekilde yazildi
import io
import cv2
import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder

# Roboflow API anahtarınız
api_key = "GiGwZjBmOMekt0xkE95u"

# Roboflow proje adı ve versiyon numarası
project_name = "bluefriendorenemy"
version_number = "3"

# API endpoint URL'si
url = f"https://detect.roboflow.com/{project_name}/{version_number}?api_key={api_key}"

# Kameradan bir kare al
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

# Kareyi Roboflow API'sine gönder
_, img_encoded = cv2.imencode('.jpg', frame)
m = MultipartEncoder(fields={'file': ("imageToUpload", img_encoded.tobytes(), "image/jpeg")})
response = requests.post(url, data=m, headers={'Content-Type': m.content_type})

# Yanıttan sonuçları al
data = response.json()

# İlk tahminin bilgilerini çıkar
imWidth = int(data['predictions'][0]['width'])
imHeight = int(data['predictions'][0]['height'])
xp = int(data['predictions'][0]['x'])
yp = int(data['predictions'][0]['y'])
className = data['predictions'][0]['class']
confidence = float(data['predictions'][0]['confidence'])

# Dikdörtgen koordinatlarını hesapla
start_x = xp - (imWidth / 2)
start_y = yp - (imHeight / 2)
end_x = xp + (imWidth / 2)
end_y = yp + (imHeight / 2)

# Dikdörtgeni çiz
cv2.rectangle(frame, (int(start_x), int(start_y)), (int(end_x), int(end_y)), color=(0, 255, 0), thickness=2)

# Etiketi ve güven değerini ekle
label = f"{className}: {confidence:.2f}"
cv2.putText(frame, label, (int(start_x), int(start_y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Sonucu göster
cv2.imshow('Object Detection', frame)
cv2.waitKey(0)

# Kamera bağlantısını kapat
cap.release()
cv2.destroyAllWindows()
