import cv2
import mediapipe as mp
import time

class FaceMeshDetector():
    def __init__(self, staticmode=False,maxFaces=1,minDetectionCon=0.5,minTrackCon=0.5 ):
        self.staticmode=staticmode
        self.maxFaces=maxFaces
        self.minDetectionCon=minDetectionCon
        self.minTrackCon=minTrackCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.staticmode,self.maxFaces,False,
                                                 self.minDetectionCon,self.minTrackCon)
        self.drawSpec = self.mpDraw.DrawingSpec(color=(0, 255, 0),
                                                thickness=2,circle_radius=2)

    def findFaceMesh(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results= self.faceMesh.process(imgRGB)
        faces = []
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                print(faceLms)
                if draw:
                    self.mpDraw.draw_landmarks(img,faceLms,self.mpFaceMesh.FACEMESH_CONTOURS,
                                               self.drawSpec,self.drawSpec)
                face = []
                for id,lm in enumerate(faceLms.landmark):
                    #print(lm.x,lm.y)
                    ih,iw,ic = img.shape
                    x,y = int(lm.x*iw),int(lm.y*ih)
                    #print(id,x,y)
                    face.append((x,y))
                faces.append(face)
        return img,faces

def main():
    cap = cv2.VideoCapture(1)
    cap.set(3, 800)
    cap.set(4, 600)
    pTime = 0
    detector = FaceMeshDetector()
    while cap.isOpened():
        ret, img = cap.read()
        img,faces = detector.findFaceMesh(img)
        if len(faces)!=0:
            print(len(faces))
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS:{int(fps)}', (20, 40), cv2.FONT_HERSHEY_PLAIN,
                    3, (0, 255, 0), 2)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()