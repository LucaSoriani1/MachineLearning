# AirCanva
This is a Python script that allows you to draw on your computer screen with your hand. It uses the OpenCV library for image processing and the hand_tracking module to detect the position of the hand in the video feed.

The program has the following features:

* Hand detection: It detects the position of the hand in the video frame.
* Drawing: It allows the user to draw on a canvas by moving their hand in front of the camera.
* Brush and eraser thickness: The brush and eraser thickness can be adjusted.
* Color: The color of the brush can be changed.
* Saving: The user can save their drawing to a file.
* Menu: A menu can be displayed by making a specific gesture with their hand.

### How to use
1. Run the program in a Python environment.
2. Hold your hand up in front of the webcam.
3. Move your index finger and your middle finger together to change the color of the brush. The color is set to blue by default.
4. Use your index finger to draw on the canvas.
5. Move your index finger and your thumb together to erase. The thickness of the eraser can be adjusted using the variable named "eraserThickness" from the file named "utils.py" or just zoomming in or zoomming out with the thumb and forefinger.
6. Move your index finger and your ring finger together to open the menu. The menu allows you to save your drawing .
7. To save your drawing, choose the "Save" option from the menu. The image will be saved in the folder named "images" with the name that you specify. The original image and the image with a white background will be saved. Alternativelly, rise up the thumb, forefinger and the middle finger.
8. To exit the program, rise up all the fingers.

### Requirements

* mediapipe
* numpy
* opencv_python

### Usage
To run the script, move to the main directory and execute the following command in a terminal:

```
python main.py
```

The script will capture the video feed from your default webcam and display it on the screen. You can use your hand to draw on the screen. The app detects the position of your hand and draws a line wherever your hand moves.

### Drawing
To draw, simply lift your index finger. You can change the colour of the brush by selecting from the drop-down menu a colour between blue red and green while lifting your index and middle finger and keeping your other fingers closed. The default colour is blue.

### Brush Thickness
To increase or decrease the width of the brush, zoom in with thumb and forefinger. In this way you can increase the width by up to 500 units and decrease it by up to 1 unit.

### Erasing
To erase, select the eraser from the drop-down menu. You can erase in the same way as you draw, i.e. by holding your index finger up. As seen with the drawing, you can increase or decrease the thickness of the eraser using your thumb and forefinger. 

To clean the entire canva, you can go to the drop-down menu and click on the red 'x'. 

### Saving
To save the drawing, select the save symbol from the drop-down menu. The drawing will be saved in two modes: one with the background and one without. You will find the saved images in the 'img/saves' folder in the main directory saved with the current timestamp. In addition, to save images you can raise your thumb, index and middle finger: this will trigger the timer to save the images.

You can also save the image by pressing the letter 's' from your keyboard.

### Stop the program
To stop the programme execution you can click the 'x' button on the Air Canva window or raise all five fingers of your hand. Alternatively, you can click the letter 'q' from the keyboard.