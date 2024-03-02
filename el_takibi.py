import cv2
import mediapipe as mp

# MediaPipe Hands sınıfını başlatma
mpHands = mp.solutions.hands
hands = mpHands.Hands()

# MediaPipe Drawing Utils sınıfını başlatma
mpDraw = mp.solutions.drawing_utils

# Elleri bulan fonksiyon
def FindHands(frame):
    # Görüntüyü RGB formatına dönüştürme
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Elleri tespit etme işlemi
    results = hands.process(frame_rgb)

    # Görüntü boyutlarını alma
    h, w, c = frame.shape
    
    # Eğer bir veya daha fazla el tespit edilirse
    if results.multi_hand_landmarks:

        # Her bir el için döngü
        for handLms in results.multi_hand_landmarks:

            # Her bir eldeki 21 landmark noktası için döngü
            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)

            # Ellerin üzerine çizgiler ve noktalar çizme
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

    return frame

# Ana fonksiyon
def main():
    # Kamera bağlantısını açma
    cap = cv2.VideoCapture(0)

    while True:
        # Kameradan bir kare okuma
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)  # Aynalama

        # Elleri bulma fonksiyonunu çağırma
        frame = FindHands(frame)
    
        # Ekran üzerinde canlı görüntüyü gösterme
        cv2.imshow('Canlı Görüntü', frame)

        # 'x' tuşuna basılınca döngüyü sonlandırma
        if cv2.waitKey(20) & 0xFF == ord('x'):
            break

    # Pencereyi kapatma ve kamera bağlantısını serbest bırakma
    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()
