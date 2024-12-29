import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

import cv2
from fer import FER
import json
import pyttsx3

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import random

import ST7735 as TFT

from threading import Thread, Lock
import time
from typing import List, Dict, Tuple

_face_coords = List[int]
_emotion_dict = Dict[str, float]
_face_data = Dict[str, _face_coords|_emotion_dict]
_frame = cv2.typing.MatLike

CAMERA_IP = 'http://192.168.6.149:4747/video'

WIDTH = 128
HEIGHT = 160
SPEED_HZ = 16000000

# Raspberry Pi configuration.
DC = 24
RST = 25
SPI_PORT = 0
SPI_DEVICE = 0

# ENGINE = pyttsx3.init()
# ENGINE.setProperty('voice', ENGINE.getProperty('voices')[1].id)
# ENGINE.setProperty('rate', 175)

with open('compliments_formatted.json', 'r', encoding='utf-8') as compliments:
    COMPLIMENTS = json.load(compliments)

def box_face(frame: _frame, face_box: _face_coords) -> _frame:
    frame = cv2.rectangle(
        img = frame,
        pt1 = (face_box[0], face_box[1]),
        pt2 = (face_box[0] + face_box[2], face_box[1] + face_box[3]),
        color = (0, 155, 255),
        thickness = 2
    )

    return frame

def analyse_curr_emotion(emotions_metrics: Dict[str, float]) -> Tuple[str|float]:
    curr_emotion_percent: float = 0.0
    curr_emotion: str|None = None
    for emotion, percent in emotions_metrics:
        if percent > curr_emotion_percent:
            curr_emotion_percent = percent
            curr_emotion = emotion
    
    return curr_emotion, curr_emotion_percent

def display_text(DISPLAY: TFT.ST7735, compliment: List[str]) -> Image:
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    draw.rectangle((0, 0, 128, 160), (128, 128, 128))
    draw.text((0, 0), '\n'.join(compliment), font=font, fill=(255, 255, 255))

    return img

def stop_and_speak(new_text: List[str]) -> None:
    # ENGINE.say(''.join(new_text))
    # try: ENGINE.runAndWait()
    # except RuntimeError: pass

    ...

if __name__ == '__main__':

    CAM: cv2.VideoCapture = cv2.VideoCapture(CAMERA_IP)
    FRAME_WIDTH: int = int(CAM.get(cv2.CAP_PROP_FRAME_WIDTH))
    FRAME_HEIGHT: int = int(CAM.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create TFT LCD display class.
    DISPLAY: TFT.ST7735 = TFT.ST7735(
                        DC,
                        rst=RST,
                        spi=SPI.SpiDev(
                            SPI_PORT,
                            SPI_DEVICE,
                            max_speed_hz=SPEED_HZ))
    DISPLAY.begin()

    DETECTOR: FER = FER()

    prev_emotion_percent: float = 0.0
    prev_emotion: str = ''
    compliment: List[str] = ['']
    while True:
        ret, frame = CAM.read()
        frame = cv2.flip(frame, 1)
        
        metrics: List[_face_data] = DETECTOR.detect_emotions(frame)
        face_found = True if metrics else False

        if face_found:
            face_box = metrics[0]['box']
            # frame = box_face(frame, face_box)

            curr_emotion_percent: float = 0.0
            curr_emotion: str|None = None
            curr_emotion, curr_emotion_percent = analyse_curr_emotion(metrics[0]['emotions'].items())
            
            emotion_changed: bool = curr_emotion != prev_emotion and abs(prev_emotion_percent - curr_emotion_percent) > 0.2
            if emotion_changed:
                compliment = random.choice(COMPLIMENTS[curr_emotion])
                
                # thread = Thread(target=stop_and_speak, args=(compliment, ))
                # thread.daemon = True
                # thread.start()

                prev_emotion = curr_emotion
                prev_emotion_percent = curr_emotion_percent
            
            DISPLAY.display(display_text(DISPLAY, compliment))

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