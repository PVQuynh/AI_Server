import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import logging
logging.getLogger('tensorflow').setLevel(logging.ERROR)

import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math

from pytube import YouTube


def textDetection(videoUrl):
    try:
        # Thay đổi đường dẫn tới video của bạn hoặc đường dẫn URL
        # video_path = "AI_HandSign/videos/video.mp4"
        cap = cv2.VideoCapture(videoUrl)

        # URL của video trên YouTube
        # try:
        #     yt = YouTube(videoUrl)
        #     videoStream = yt.streams.get_highest_resolution()
        # except Exception as e:
        #     print("Lỗi đường dẫn video!")
        #     return None
        # cap = cv2.VideoCapture(videoStream.url)

        detector = HandDetector(maxHands=1)
        classifier = Classifier("ai/models/mymodel.h5", "ai/models/labels.txt")
        offset = 20
        imgSize = 300

        detectedTexts = ""

        labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        while True:
            success, img = cap.read()
            if not success:
                break

            # imgOutput = img.copy()

            hands, img = detector.findHands(img)

            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']

                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
                imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

                # imgCropShape = imgCrop.shape

                aspectRatio = h / w

                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    # imgResizeShape = imgResize.shape
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)

                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    # imgResizeShape = imgResize.shape
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)

                # cv2.rectangle(imgOutput, (x - offset, y - offset-50),
                #             (x - offset+90, y - offset-50+50), (255, 0, 255), cv2.FILLED)
                # cv2.putText(imgOutput, labels[index], (x, y -26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
                # cv2.rectangle(imgOutput, (x-offset, y-offset),
                #             (x + w+offset, y + h+offset), (255, 0, 255), 4)
                
                # Text detection
                text_tmp = str(labels[index])
                if len(detectedTexts) == 0 or str(text_tmp) != detectedTexts[-1]:
                    detectedTexts += text_tmp


            # cv2.imshow("Image", imgOutput)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break

        cv2.destroyAllWindows()
        cap.release()

        return detectedTexts
    
    except Exception as e:
        print("Có lỗi xảy ra trong quá trình sử dụng!")
        return None
    
