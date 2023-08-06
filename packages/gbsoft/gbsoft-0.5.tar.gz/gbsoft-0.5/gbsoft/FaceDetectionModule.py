"""
Face Detection Module
By: GB Softronics Solution
Website: https://www.gbsoftronics.com/
"""

import cv2
import mediapipe as mp
import time

class FaceDetector():
    """
        Finds Faces using the mediapipe library. Exports the landmarks
        in faces. Adds extra functionalities as draw face using fancyDraw Function.
        """
    def __init__(self,minDetectionCon=0.5):
        """
        :param minDetectionCon: MinimumDetection Confidance. Range between 0-1
        """
        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)

    def findFaces(self,img,draw=True):
        """
        :param img: input Image in BGR Format
        :param draw: Flag to draw the face bounding box. Default: True
        """
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results= self.faceDetection.process(imgRGB)
        #print(results)
        bboxs = []
        if self.results.detections:
            for id,detection in enumerate(self.results.detections):
                #mpDraw.draw_detection(img,detection)
                #print(id,detection)
                bboxC = detection.location_data.relative_bounding_box
                ih,iw,ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                bboxs.append([bbox,detection.score])
                #print(bbox)
                if draw:
                    #cv2.rectangle(img,bbox,(255,0,255),5)
                    self.fancyDraw(img,bbox)
                    confidance_score = int(detection.score[0] * 100)
                    #print(confidance_score)
                    cv2.putText(img, str(confidance_score) + '%', (bbox[0],bbox[1]-20), cv2.FONT_HERSHEY_PLAIN, 4,
                                (0, 0, 255), 2)
        return img, bboxs

    def fancyDraw(self, img, bbox, l=50, t=10, rt=1):
        """
        :param img: input Image in BGR Format
        :param bbox: bounding box as tuple (x,y,w,h)
        :param l: Length of Line for fancy Rect Draw
        :param t: Thickness of Line for Fancy Rect Draw. Max value, thicker line
        :param rt: Rectangle Thickness
        """
        x, y, w, h = bbox
        x1, y1 = x + w, y + h

        cv2.rectangle(img, bbox, (255, 0, 255), rt)
        # Top Left x,y
        cv2.line(img, (x, y), (x + l, y), (255, 0, 255), t)
        cv2.line(img, (x, y), (x, y + l), (255, 0, 255), t)
        # Top Right x1,y
        cv2.line(img, (x1, y), (x1 - l, y), (255, 0, 255), t)
        cv2.line(img, (x1, y), (x1, y + l), (255, 0, 255), t)
        # Bottom Left x,y1
        cv2.line(img, (x, y1), (x + l, y1), (255, 0, 255), t)
        cv2.line(img, (x, y1), (x, y1 - l), (255, 0, 255), t)
        # Bottom Right x1,y1
        cv2.line(img, (x1, y1), (x1 - l, y1), (255, 0, 255), t)
        cv2.line(img, (x1, y1), (x1, y1 - l), (255, 0, 255), t)
        return img

def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = FaceDetector()
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            continue

        img,bboxs = detector.findFaces(img)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 0, 255), 4)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()