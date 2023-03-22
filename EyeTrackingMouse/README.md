# Eye Mouse
This Python code uses OpenCV, Mediapipe, and PyAutoGUI to track facial movements and clicks, and control the mouse cursor accordingly.

### Prerequisites
Make sure you have the following libraries installed:

* cv2 (OpenCV)
* mediapipe
* pyautogui

You can also find the required libraries in the requirements.txt file included in this repository.

To install the libraries from the requirements.txt file, run the following command in your terminal:
```
pip install -r requirements.txt
```

### How to use
1. Connect a webcam to your computer and run the code.

2. Look at your webcam and move your face around. The script will track the movement of your face and move the mouse cursor accordingly.

3. To click, blink your left eye twice in a row. This will trigger a left-click on the current mouse position.

4. To exit the script, press any key on your keyboard.

Note: The script sets the frames per second to 60, and initializes the FaceMesh model with refined landmarks. Also, the cursor position is calculated based on the position of the second landmark.