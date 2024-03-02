import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, mode=False, maxHands=1, modcomplex=1, DetectCon=0.5, TrackCon=0.5):
        """
        Elleri algılamak ve izlemek için bir HandDetector nesnesi oluşturur.

        Parameters:
            - mode: Elleri algılama modu (Varsayılan değer: False)
            - maxHands: Algılanacak maksimum el sayısı (Varsayılan değer: 1)
            - modcomplex: Modüler komplekslik (Varsayılan değer: 1)
            - DetectCon: Algılama güvenilirlik eşiği (Varsayılan değer: 0.5)
            - TrackCon: İzleme güvenilirlik eşiği (Varsayılan değer: 0.5)
        """
        self.mode = mode
        self.maxHands = maxHands
        self.modcomplex = modcomplex
        self.DetectCon = DetectCon
        self.TrackCon = TrackCon

        # MediaPipe Hands modülünü kullanarak elleri algılamak için gerekli nesneleri oluşturur.
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modcomplex, self.DetectCon, self.TrackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def FindHands(self, frame, draw=True):
        """
        Verilen bir görüntü çerçevesinde elleri bulur ve isteğe bağlı olarak çizer.

        Parameters:
            - frame: Görüntü çerçevesi
            - draw: Elleri çizme modu (Varsayılan değer: True)

        Returns:
            - frame: Elleri çizilmiş görüntü çerçevesi
        """
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frameRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)

        return frame

    def FindPositions(self, frame, HandNo=0):
        """
        Belirli bir elin landmark pozisyonlarını bulur.

        Parameters:
            - frame: Görüntü çerçevesi
            - HandNo: Bulunacak elin indeksi (Varsayılan değer: 0)

        Returns:
            - lm_list: Landmark pozisyonlarını içeren liste
        """
        self.lm_list = []
        h, w, c = frame.shape

        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[HandNo]
            for id, lm in enumerate(Hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lm_list.append([id, cx, cy])

        return self.lm_list

    def FindGesture(self):
        """
        Ellerdeki parmak durumunu belirler.

        Returns:
            - fingers: Parmağın açık (1) veya kapalı (0) durumlarını içeren liste
        """
        fingers_id = [8, 12, 16, 20]
        fingers = []

        for id in fingers_id:
            if self.lm_list[id][2] < self.lm_list[id - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

def main():
    # Kamera bağlantısını başlatır
    cap = cv2.VideoCapture(0)

    # Elleri tespit etmek ve izlemek için HandDetector nesnesi oluşturur
    detector = HandDetector()

    while True:
        # Kameradan bir çerçeve alır
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # Elleri tespit eder ve çerçeveye çizer
        frame = detector.FindHands(frame, True)

        # Landmark pozisyonlarını bulur
        lm_list = detector.FindPositions(frame, 0)

        if len(lm_list):
            # Parmak durumunu bulur ve ekrana yazar
            fingers = detector.FindGesture()
            print(fingers)

        # Çerçeveyi gösterir
        cv2.imshow('Live', frame)

        # Çıkış tuşunu kontrol eder
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    # Pencereleri kapatır ve kamera bağlantısını serbest bırakır
    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()
