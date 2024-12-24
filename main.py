from typing import List, Dict
import cv2
from fer import FER

_face_coords = List[int]
_emotion_dict = Dict[str, float]

# Initialize camera
CAM: cv2.VideoCapture = cv2.VideoCapture(1)

FRAME_WIDTH: int = int(CAM.get(cv2.CAP_PROP_FRAME_WIDTH))
FRAME_HEIGHT: int = int(CAM.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Initialize FER detector
detector = FER()

while True:
    ret, frame = CAM.read()
    frame = cv2.flip(frame, 0)  # Flip frame for mirror effect
    
    # Detect emotions for all faces
    metrics: List[Dict[str, _face_coords | _emotion_dict]] = detector.detect_emotions(frame)
    if metrics:
        for face_data in metrics:
            # Extract bounding box
            bounding_box = face_data["box"]
            frame = cv2.rectangle(
                frame,
                (bounding_box[0], bounding_box[1]),
                (bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                (0, 155, 255),  # Bounding box color
                2
            )

            # Find the emotion with the highest probability
            mx: float = 0.0
            curr_emotion: str | None = None
            for emotion, percent in face_data['emotions'].items():
                if percent > mx:
                    mx = percent
                    curr_emotion = emotion

            # Annotate the emotion on the frame
            if curr_emotion:
                frame = cv2.putText(
                    img=frame,
                    text=curr_emotion,
                    org=(bounding_box[0], bounding_box[1] - 10),  # Position above the bounding box
                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=2,
                    color=(0, 255, 0),  # Text color
                    thickness=2,
                    lineType=cv2.LINE_AA
                )

    # Display the frame
    cv2.imshow('Camera', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources
CAM.release()
cv2.destroyAllWindows()
