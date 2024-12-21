from compliments import COMPLIMENTS
import cv2
from fer import FER
import random
from typing import List, Dict, Tuple

_face_coords = List[int]
_emotion_dict = Dict[str, float]

def analyse_curr_emotion(emotions_metrics: Dict[str, float]) -> Tuple[str|float]:
    curr_emotion_percent: float = 0.0
    curr_emotion: str|None = None
    for emotion, percent in emotions_metrics:
        if percent > curr_emotion_percent:
            curr_emotion_percent = percent
            curr_emotion = emotion
    
    return curr_emotion, curr_emotion_percent


def show_text(frame: cv2.typing.MatLike, compliment_lines: List[str]) -> cv2.typing.MatLike:
    for i, line in enumerate(compliment_lines):
        frame = cv2.putText(
            img = frame,
            text = line,
            org = (5, (i+1)*30),
            fontFace = cv2.FONT_HERSHEY_PLAIN,
            fontScale = 2,
            color = (0, 255, 0),
            thickness = 2,
            lineType = cv2.LINE_AA
        )
    
    return frame

if __name__ == '__main__':

    CAM: cv2.VideoCapture = cv2.VideoCapture(0)
    DETECTOR: FER = FER()

    prev_emotion_percent: float = 0.0
    prev_emotion: str = ''
    compliment: str = ''
    while True:
        ret, frame = CAM.read()
        frame = cv2.flip(frame, 1)
        
        metrics: List[Dict[str, _face_coords|_emotion_dict]] = DETECTOR.detect_emotions(frame)
        if metrics:

            curr_emotion_percent: float = 0.0
            curr_emotion: str|None = None
            curr_emotion, curr_emotion_percent = analyse_curr_emotion(metrics[0]['emotions'].items())
            
            emotion_changed: bool = curr_emotion != prev_emotion and abs(prev_emotion_percent - curr_emotion_percent) > 0.2
            if emotion_changed:
                compliment = random.choice(COMPLIMENTS[curr_emotion])
                prev_emotion = curr_emotion
                prev_emotion_percent = curr_emotion_percent
            
            compliment_lines: List[str] = compliment.split('\n')
            frame = show_text(frame, compliment_lines)

        else:
            frame = cv2.putText(
                img = frame,
                text = 'No Face Found',
                org = (5, 30),
                fontFace = cv2.FONT_HERSHEY_PLAIN,
                fontScale = 2,
                color = (0, 0, 255),
                thickness = 2,
                lineType = cv2.LINE_AA
            )


        cv2.imshow('Facial Expression Analyser', frame)

        if cv2.waitKey(1) == ord('q'): # Press 'q' to exit the loop
            break

    CAM.release()
    cv2.destroyAllWindows()