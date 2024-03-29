<<<<<<< HEAD
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
=======
import cv2
import tempfile
from roboflow import Roboflow

# Roboflow API anahtarınızı buraya ekleyin
roboflow = Roboflow(api_key="B3pPR0IaMyT9bhXkjuFP")

# Roboflow'dan modeli al
project = roboflow.workspace().project("bluefriendorenemy")
model = project.version(3).model

# Kamera bağlantısını başlat
cap = cv2.VideoCapture(0)

while True:
    # Kameradan bir çerçeve al
    ret, frame = cap.read()

    # Geçici bir dosyaya kareyi kaydet
    temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    temp_filename = temp_file.name
    cv2.imwrite(temp_filename, frame)

    # Modeli geçici dosya yoluyla çağır
    result = model.predict(temp_filename)

    # Geçici dosyayı sil
    temp_file.close()
    # Algılanan nesneleri çerçeve üzerine çiz
    for prediction in result.predictions:
        class_name = prediction.class_name
        confidence = prediction.confidence

        prediction.class_name
        box = prediction.bbox
        (startX, startY, endX, endY) = box
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
        cv2.putText(frame, f"{class_name}: {confidence:.2f}", (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Görüntüyü göster
    cv2.imshow("Nesne Tespiti", frame)

    # 'q' tuşuna basıldığında döngüyü kır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamera bağlantısını kapat
cap.release()
cv2.destroyAllWindows()
>>>>>>> a4d29233af734e4dd0dbe9b30e96e1b2257f6248
