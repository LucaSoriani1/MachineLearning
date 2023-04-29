import os
import datetime

# Setting the thickness of the brush.
BRUSH_THICKNESS = 30

# A constant that is used to set the timer for the countdown.
TIMER = 3

# A constant that is used to set the path of the header folder.
HEADER_FOLDER = 'img/header'

extension = ".jpg"

def save(folder_path="img/saves"):
    """
    It creates a folder if it doesn't exist, then it finds the last file in the folder, and increments
    the number in the filename by one
    
    :param folder_path: The folder where the images will be saved, defaults to img/saves (optional)
    :return: a string.
    """
    # It creates a folder if it doesn't exist.
    os.makedirs(folder_path, exist_ok=True)
    
    dt = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")   
        
    return f"{folder_path}/{dt}{extension}"
