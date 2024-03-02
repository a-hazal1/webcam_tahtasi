import cv2
import mediapipe as mp

# MediaPipe Hands sınıfını başlatma
mpHands = mp.solutions.hands
# Tek bir elin tespit edilmesi için değerleri ayarlayarak Hands sınıfını başlatma
hands = mpHands.Hands(False, 1, 1, 0.5, 0.5)
# MediaPipe Drawing Utils sınıfını başlatma
mpDraw = mp.solutions.drawing_utils

# FindPositions fonksiyonu, el için landmark listesini almak için kullanılır
def FindPositions(frame):
    lm_list = []

    # Görüntüyü RGB formatına dönüştürme
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Ellerin tespit edilmesi işlemi
    results = hands.process(frame_rgb)
    h, w, c = frame.shape
    
    # Eğer bir el tespit edilirse
    if results.multi_hand_landmarks:
        # Sadece bir elin tespit edildiğinden emin olduğumuz için
        Hand = results.multi_hand_landmarks[0]

        # Ellerin landmark'larını döngüyle gezerek koordinatları lm_list'e eklemek
        for id, lm in enumerate(Hand.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            lm_list.append([id, cx, cy])

    return lm_list

# FindGesture fonksiyonu, hangi parmakların uzatıldığını tespit eder ve hareketi geri döndürür
def FindGesture(lm_list):
    # Baş parmak hariç parmak uçları id'leri
    fingers_id = [8, 12, 16, 20]
    fingers = []

    # Parmak uçlarının, altlarındaki bir landmark noktasına göre göreceli konumunu kontrol etme
    for id in fingers_id:
        if lm_list[id][2] < lm_list[id - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

def main():
    # Kamera bağlantısını açma
    cap = cv2.VideoCapture(0)

    while True:
        # Kameradan bir kare okuma
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # Ellerin landmark'larını bulma
        lm_list = FindPositions(frame)
        if len(lm_list):
            # Hareketi ekrana yazdırma
            print(FindGesture(lm_list))
    
        cv2.imshow('Canlı Görüntü', frame)

        # 'x' tuşuna basıldığında döngüyü sonlandırma
        if cv2.waitKey(20) & 0xFF == ord('x'):
            break

    # Pencereyi kapatma ve kamera bağlantısını serbest bırakma
    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()
