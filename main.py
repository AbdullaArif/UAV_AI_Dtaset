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
