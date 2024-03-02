# OpenCV ve diğer modüllerin import edildiği kısım
import cv2
import os
import numpy as np
from PIL import Image
import el_takibinde_hareket_tanima as hgm

# Renk, ana sayfa ve boyutlar klasör yolları
colorsPath = "navBar\\renkler"
homepagePath = "navBar\\ana_sayfa"
sizesPath = "navBar\\Boyutlar"

# Klasörlerdeki resim listeleri
imListColors = os.listdir(colorsPath)
imListHomepage = os.listdir(homepagePath)
imListSizes = os.listdir(sizesPath)

# Resim listelerini tutacak listeler
colors = []
homepage = []
sizes = []

# Renk resimlerini yükleme
for imPath in imListColors:
    image = cv2.imread(f'{colorsPath}/{imPath}')
    colors.append(image)

# Ana sayfa resimlerini yükleme
for imPath in imListHomepage:
    image = cv2.imread(f'{homepagePath}/{imPath}')
    homepage.append(image)

# Boyut resimlerini yükleme
for imPath in imListSizes:
    image = cv2.imread(f'{sizesPath}/{imPath}')
    sizes.append(image)

# Canvas üzerine çizim yapma fonksiyonu
def drawOnFeed(frame, canvas):
    # Canvas üzerine çizim yapmak için gerekli işlemler
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, ImgInv = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    ImgInv = cv2.cvtColor(ImgInv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, ImgInv)
    frame = cv2.bitwise_or(frame, canvas)
    return frame

# Ana program fonksiyonu
def main():
    # Ekran genişliği ve yüksekliği tanımlamaları
    width, height = 1280, 720

    # Fırça renkleri, boyutları ve silgi boyutları
    brushColor = [(0, 0, 255), (0, 255, 0), (255, 0, 80)]
    brushSize = [10, 20, 30]
    eraserSize = [25, 45, 60]

    # Başlangıç değerleri
    currNavBar, currNavBarid, currColor, currBrushsize, currEraserSize = homepage[0], 0, brushColor[2], brushSize[1], eraserSize[1]
    canvas = np.zeros((height, width, 3), dtype='uint8')

    # Kamera bağlantısı
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)

    # Fare koordinatları
    xp, yp = 0, 0

    # El takibi yapacak sınıfın tanımlanması
    detector = hgm.HandDetector()

    # Ana döngü
    while True:
        # Kamera görüntüsünün alınması
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # El takibi
        frame = detector.FindHands(frame, True)
        lm_list = detector.FindPositions(frame, 0)

        # Eğer el tespit edilirse
        if len(lm_list):
            # Parmak sayısının belirlenmesi
            # Ellerin durumunu tespit etme
            fingers = detector.FindGesture()

            # İşaret parmağı ve orta parmağın koordinatları
            xi, yi = lm_list[8][1:]
            xm, ym = lm_list[12][1:]

            # İşaret parmağı
            if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0:
                # Başlangıç noktası
                if xp == 0 and yp == 0:
                    xp, yp = xi, yi
                # Çizgi çizme
                cv2.line(canvas, (xp, yp), (xi, yi), currColor, currBrushsize)
                xp, yp = xi, yi

            # İşaret ve orta parmaklar
            elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0:
                xp, yp = 0, 0
                # Ana menüdeyken kontrol
                if currNavBarid == 0:
                    if ym < 100:
                        if 100 < xm < 280:
                            currNavBar, currNavBarid = colors[0], 1
                        elif 400 < xm < 620:
                            currNavBar, currNavBarid = sizes[1], 2
                        elif 780 < xm < 940:
                            currNavBar, currNavBarid = sizes[0], 3
                # Renk seçimi yapılırken kontrol
                elif currNavBarid == 1:
                    if ym < 100:
                        if 100 < xm < 280:
                            currNavBar, currColor = colors[0], brushColor[2]
                        elif 400 < xm < 620:
                            currNavBar, currColor = colors[2], brushColor[0]
                        elif 780 < xm < 940:
                            currNavBar, currColor = colors[1], brushColor[1]
                        elif 1080 < xm < 1200:
                            currNavBar, currNavBarid = homepage[0], 0
                # Fırça boyutu seçimi yapılırken kontrol
                elif currNavBarid == 2:
                    if ym < 100:
                        if 100 < xm < 280:
                            currNavBar, currBrushsize = sizes[2], brushSize[0]
                        elif 400 < xm < 620:
                            currNavBar, currBrushsize = sizes[1], brushSize[1]
                        elif 780 < xm < 940:
                            currNavBar, currBrushsize = sizes[0], brushSize[2]
                        elif 1080 < xm < 1200:
                            currNavBar, currNavBarid = homepage[0], 0
                # Silgi boyutu seçimi yapılırken kontrol
                elif currNavBarid == 3:
                    if ym < 100:
                        if 100 < xm < 280:
                            currNavBar, currEraserSize = sizes[2], eraserSize[0]
                        elif 400 < xm < 620:
                            currNavBar, currEraserSize = sizes[1], eraserSize[1]
                        elif 780 < xm < 940:
                            currNavBar, currEraserSize = sizes[0], eraserSize[2]
                        elif 1080 < xm < 1200:
                            currNavBar, currNavBarid = homepage[0], 0

            # İşaret, orta ve yüzük parmaklar
            elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
                xp, yp = 0, 0

            # İşaret, orta, yüzük ve serçe parmaklar
            elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:
                # Silgi olarak kullanılan daire çizme
                cv2.circle(frame, (xm, ym), currEraserSize, (0, 0, 0), -1)
                cv2.circle(canvas, (xm, ym), currEraserSize, (0, 0, 0), -1)
                xp, yp = 0, 0


            else:
                xp, yp = 0, 0

        # Canvas üzerine çizim yapma fonksiyonu
        frame = drawOnFeed(frame, canvas)
        frame[0:100, 0:1280] = currNavBar
        cv2.imshow('Canli Görüntü', frame)

        # Çıkış tuşu kontrolü
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    # Pencerelerin kapatılması ve kamera bağlantısının serbest bırakılması
    cv2.destroyAllWindows()
    cap.release()

# Programın ana fonksiyonunu çağırma
if __name__ == "__main__":
    main()
