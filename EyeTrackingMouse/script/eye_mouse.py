import cv2
import mediapipe as mp
import pyautogui

# Initialize camera object
camera = cv2.VideoCapture(0)

# Set frames per second to 60
camera.set(cv2.CAP_PROP_FPS, 60)

# Initialize FaceMesh model with refined landmarks
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# Get width and height of screen
screen_width, screen_height = pyautogui.size()

# Infinite loop to track face movements and clicks
while True:
    # Read a frame from the camera
    _, frame = camera.read()

    # Flip the frame horizontally to mirror it
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect facial landmarks in the RGB frame
    output = face_mesh.process(rgb_frame)

    # Extract the landmark points
    landmark_points = output.multi_face_landmarks

    # Get width and height of the frame
    frame_height, frame_width, _ = frame.shape

    # Loop over the landmark points and draw circles on them
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            
            # Calculate cursor position based on the position of the second landmark
            if id == 1:
                screen_x = screen_width / frame_width * x
                screen_y = screen_height / frame_height * y
                pyautogui.moveTo(screen_x, screen_y)

        # Check if the user is blinking and clicking on a button
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            cv2.circle(frame, (x, y), 3, (255, 0, 0))

        if (left[0].y - left[1].y) < 0.0004:
            pyautogui.click()
            pyautogui.sleep(1)

    # Show the frame with landmarks on a window named "Eye mouse"
    cv2.imshow('Eye mouse', frame)
    
    # Wait for the user to press a key for 1 millisecond before continuing the loop
    cv2.waitKey(1)