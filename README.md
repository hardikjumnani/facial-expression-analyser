# Technical Challenge: Build a Feature for the Smart Mirror

[For more info](https://docs.google.com/document/d/1V6fS0x77ThQfvjP7TFSBcTVrIYgCKFowFTQO0VWNbeM/edit?tab=t.0#heading=h.vx7skgheux9k)

## Problem Statement
You are tasked with building a personalized compliment generator based on facial analysis. The feature should:
1. Detect the user’s face in an image or live feed.
2. Analyze their facial expression (e.g., smile, neutral).
3. Generate and display a compliment (e.g., “Your smile is glowing today!”) based on the detected expression.

## Overview of the Solution
The program captures your camera feed and the library 'fer' is used to detect emotions. The random module then picks a compliment according to the emotion and compliments the user on the video output.

## Libraries and tools used
**Libraries**
OpenCV
FER Library
pyttsx3

**Tools**
[ChatGPT](https://chatgpt.com/share/67592122-6a88-8013-b563-d57f5a1af674)
StackOverflow


## Challenges faced and how they were addressed
**ModuleNotFoundError: No module named 'moviepy.editor'**
[reference](https://stackoverflow.com/questions/41923492/cant-import-moviepy-editor)
Fixed this by installing specific version of moviepy

**Rapid change of compliment random compliments, even without change of emotion**
Fixed this by having a record of previous emotion (prev_emotion) and change compliment only when current emotion (curr_emotion) is not same as the previous one.

**Compliment's length was longer than the width of screen**
Fixed this by splitting the lines of the compliment and putting text one line at a time.

**Rapid change in compliments**
This was faced because the model is considering the current frame, without taking previousframe into account, which is causing rapid changes in guessed emotions. To fix this, I have eased out the switch so that a new compliment is picked, only when there is more than 20% change in the emotion.

**Get dimensions taken by a word on the camera frame**
A static method named getTextSize exist in cv2 which gives the size that text takes on screen.


## Instructions to run the code
Clone the Repo (Ensure Python is >=3.10.6)
```
git clone https://github.com/hardikjumnani/facial-expression-analyser
```

Create a virtual environment
```
# Windows
python -m venv .venv

# MacOS/Linux
python3 -m venv .venv
```

Activate the virtual environment
```
# Windows
source .venv/Scripts/activate

# MacOS/Linux
source .venv/bin/activate
```

Install all dependencies
```
# Windows
pip install -r requirements.txt

# MacOS/Linux
pip3 install -r requirements.txt
```

Run the program
```
# Windows
python main.py

# MacOS/Linux
python3 main.py
```