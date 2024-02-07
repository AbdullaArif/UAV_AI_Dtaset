import cv2
import pandas as pd
import pickle
import requests
import matplotlib.pyplot as plt
import os

def fetch_predictions(base_url, frame, timestamp, dataset_id, version_id, api_key, confidence=0.5):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    numpy_data = pickle.dumps(frame)
    res = requests.post(
        f"{base_url}/{dataset_id}/{version_id}",
        data=numpy_data,
        headers=headers,
        params={"api_key": api_key, "confidence": confidence, "image_type": "numpy"}
    )
    predictions = res.json()

    df_rows = []
    for pred in predictions['predictions']:
        row = {
            "timestamp": timestamp,
            "time": predictions['time'],
            "x": pred["x"],
            "y": pred["y"],
            "width": pred["width"],
            "height": pred["height"],
            "pred_confidence": pred["confidence"],
            "class": pred["class"]
        }
        df_rows.append(row)

    df = pd.DataFrame(df_rows)
    return df

def plot_and_save(data, title, filename, ylabel):
    plt.style.use('dark_background')
    data.plot(kind='bar', figsize=(15, 7))
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel('Timestamp')
    plt.tight_layout()
    plt.savefig(filename)

def main():
    base_url = "http://localhost:9001"
    dataset_id = "bluefriendorenemy"
    version_id = "4"
    api_key = "B3pPR0IaMyT9bhXkjuFP"

    cap = cv2.VideoCapture(0)  # Webcam'den video al

    if not cap.isOpened():
        print("Hata: Kamera açılamadı!")
        return

    while True:
        ret, frame = cap.read()  # Kameradan bir kare al

        if not ret:
            print("Hata: Kare alınamadı!")
            break

        timestamp = pd.Timestamp.now()  # Kare zamanını al

        df = fetch_predictions(base_url, frame, timestamp, dataset_id, version_id, api_key)

        # Sonuçları ekrana yazdırma yerine istediğiniz işlemleri yapabilirsiniz

        # İşlenmiş kareyi göster
        cv2.imshow('Frame', frame)

        # Çıkış için 'q' tuşuna basılmasını bekleyin
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Kullanılan kaynakları serbest bırak
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
