from typing import List, Dict
import cv2
from fer import FER

_face_coords = List[int]
_emotion_dict = Dict[str, float]

CAM: cv2.VideoCapture = cv2.VideoCapture(0)

FRAME_WIDTH: int = int(CAM.get(cv2.CAP_PROP_FRAME_WIDTH))
FRAME_HEIGHT: int = int(CAM.get(cv2.CAP_PROP_FRAME_HEIGHT))

prev_emotion: str = ''
while True:
    ret, frame = CAM.read()
    frame = cv2.flip(frame, 1)

    detector = FER()
    
    metrics: List[Dict[str, _face_coords|_emotion_dict]] = detector.detect_emotions(frame)
    if metrics:
        mx: float = 0.0
        curr_emotion: str|None = None
        for emotion, percent in metrics[0]['emotions'].items():
            if percent > mx:
                mx = percent
                curr_emotion = emotion
        
        # if curr_emotion != prev_emotion:
        frame = cv2.putText(
            img = frame, 
            text = curr_emotion, 
            org = (50, 50), 
            fontFace = cv2.FONT_HERSHEY_PLAIN, 
            fontScale = 1,
            color = (0, 255, 0), 
            thickness = 2, 
            lineType = cv2.LINE_AA
        )
        
        print(curr_emotion)
        prev_emotion = curr_emotion


    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) == ord('q'): # Press 'q' to exit the loop
        break

CAM.release()
cv2.destroyAllWindows()