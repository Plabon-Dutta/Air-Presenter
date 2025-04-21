# Air-Presenter (🖐️Hand Gesture-Controlled PowerPoint Presenter)

Control your Microsoft PowerPoint slides using hand gestures via webcam! This project uses computer vision and hand tracking to let you:
- Navigate slides forward/backward
- Control a pointer on screen
- Annotate/draw on a transparent overlay
- Undo annotations

## 🚀 Features

| Gesture | Description |
|--------|-------------|
| 👉 Index Finger | Move pointer on screen |
| ✌️ Index + Middle | Draw mode |
| 👍 Thumb Only | Previous Slide |
| 🤙 Pinky Only | Next Slide |
| 🤘 Index + Middle + Ring | Undo Last Annotation |

## 📷 Webcam Selection

- Internal Webcam = `cv2.VideoCapture(0)`
- External Webcam = `cv2.VideoCapture(1)` or `cv2.VideoCapture(2)` depending on your setup.

## 🔧 Requirements

Install the dependencies:

```bash
pip install opencv-python cvzone numpy pyautogui mediapipe

```

## 📝 How to Use
Connect your external webcam (if using one).

Open your .pptx file in Microsoft PowerPoint.

Start the slide show (F5).

Run the Python script. 
```bash
python Main.py

```

Use gestures in front of your webcam to control the presentation.

## 🖼️ Modes Explained
Pointer Mode: Raise only your index finger to move a red dot (pointer) on screen.

Draw Mode: Raise both index and middle fingers to draw lines on screen.

Slide Navigation: Raise thumb (left) or pinky (right) above the green line to navigate slides.

Undo Drawing: Raise index, middle, and ring fingers to undo the last annotation.

## 🧠 Powered By
- OpenCV

- CVZone

- PyAutoGUI

## ⚠️ Limitations
Drawing and pointer are visual-only (they do not interact with PowerPoint inking tools).

Ensure lighting and background contrast is good for accurate hand tracking.
