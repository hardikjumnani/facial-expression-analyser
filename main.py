import cv2
from fer import FER
import random
from typing import List, Dict

_face_coords = List[int]
_emotion_dict = Dict[str, float]

COMPLIMENTS = {
    'angry': (
        'You\'re passionate and stand up for\nwhat you believe in—don\'t lose that\nfire!',
        'Your intensity shows your strength;\nyou\'re capable of overcoming\nanything.', 
        'Your courage to express emotions is\ninspiring.'
    ), 
    'disgust': (
        'Your sharp instincts show how\ndiscerning you are—it\'s impressive.',
        'Your ability to set boundaries is\nsomething many people admire.',
        'You have a refined sense of what\'s\nright for you, and that\'s powerful.'
    ),
    'fear': (
        'Even when you\'re uncertain, your\nstrength shines through.',
        'Your courage to face challenges,\neven when scared, is amazing.',
        'You\'re resilient, and I know you\'ll\ncome out stronger from this.'
    ),
    'happy': (
        'Your laughter is contagious and\nbrings joy to everyone around you!', 
        'You radiate positivity, and it\'s so\nuplifting to be around you.', 
        'Your happiness is like sunshine—it\nbrightens up everyone\'s day.'
    ),
    'sad': (
        'You\'re incredibly strong for\ncarrying this weight—I believe in\nyou.', 
        'It\'s okay to feel this way; your\nvulnerability makes you even more\nadmirable.', 
        'Even in tough times, your\nresilience is inspiring.'
    ),
    'surprise': (
        'Your curiosity and enthusiasm make\nlife exciting for those around you!',
        'The way you embrace surprises shows\nyour open-mindedness and\nadaptability.',
        'Your ability to find joy in\nunexpected moments is truly\nrefreshing.'
    ),
    'neutral': (
        'Your calm and steady presence is so\nreassuring.',
        'You have a groundedness that makes\npeople feel safe and comfortable\naround you.',
        'Your composure is admirable—it\'s a\ntrait that many aspire to have.'
    )
}

CAM: cv2.VideoCapture = cv2.VideoCapture(0)

prev_emotion_percent: float = 0.0
prev_emotion: str = ''
compliment: str = ''
while True:
    ret, frame = CAM.read()
    frame = cv2.flip(frame, 1)

    detector = FER()
    
    metrics: List[Dict[str, _face_coords|_emotion_dict]] = detector.detect_emotions(frame)
    if metrics:
        curr_emotion_percent: float = 0.0
        curr_emotion: str|None = None
        for emotion, percent in metrics[0]['emotions'].items():
            if percent > curr_emotion_percent:
                curr_emotion_percent = percent
                curr_emotion = emotion
        
        emotion_changed: bool = curr_emotion != prev_emotion and abs(prev_emotion_percent - curr_emotion_percent) > 0.2
        if emotion_changed:
            compliment = random.choice(COMPLIMENTS[curr_emotion])
            prev_emotion = curr_emotion
            prev_emotion_percent = curr_emotion_percent
        
        compliment_lines: List[str] = compliment.split('\n')
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

    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) == ord('q'): # Press 'q' to exit the loop
        break

CAM.release()
cv2.destroyAllWindows()