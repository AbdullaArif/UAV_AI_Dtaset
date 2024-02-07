import imageio
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
cap = imageio.get_reader('/dev/video1', 'ffmpeg')

# FPS ölçümü için zamanı başlat
start_time = time.time()
frames_processed = 0

for frame in cap:
    # Kare boyutunu azalt
    frame = imageio.core.image_as_uint(frame)
    frame = imageio.core.image_as_pil(frame)
    frame = frame.resize((600, 340))

    # Kareyi Roboflow API'sine gönder
    img_encoded = imageio.core.base64_as_binary(imageio.core.array_to_base64(frame))
    m = MultipartEncoder(fields={'file': ("imageToUpload", img_encoded, "image/jpeg")})
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
        frame.paste(color, (int(start_x), int(start_y), int(end_x), int(end_y)))

        # Etiketi ve güven değerini ekle
        label = f"{className}: {confidence:.2f}"
        frame.text((int(start_x), int(start_y) - 10), label, fill=color)

    # Sonucu göster
    frame.show()

    # FPS'i hesapla
    frames_processed += 1
    elapsed_time = time.time() - start_time
    if elapsed_time > 1:
        fps = frames_processed / elapsed_time
        print(f"FPS: {fps:.2f}")
        start_time = time.time()
        frames_processed = 0
