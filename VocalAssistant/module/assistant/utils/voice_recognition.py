# Importing the `os` module.
import os

# Importing the `json` module.
import json

# Importing the `numpy` module and assigning it to the variable `np`.
import numpy as np

# Importing the `librosa` module.
import librosa

# Importing the `pandas` module and assigning it to the variable `pd`.
import pandas as pd

# Importing the 'to_categorical' from keras module.
from tensorflow.python.keras.utils.np_utils import to_categorical

# Importing the 'train_test_split' from the sklearn module.
from sklearn.model_selection import train_test_split

# Importing the `Sequential` class from the `keras` module.
from tensorflow.python.keras import Sequential

# Importing the `Dense`, `Activation` and `Dropout` classes from the `keras.layers` module.
from tensorflow.python.keras.layers import Dense, Activation, Dropout

# Loading the model.
from tensorflow.python.keras.models import load_model

# Importing the `speech_recognition` module.
import speech_recognition

# Importing the 'time' module.
import time

# Preventing the creation of .pyc files.
import os
import sys
sys.dont_write_bytecode = True

# The path to the main folder of the project.
MAIN_PATH = "VocalAssistant"

# Getting the path of the current file.
path = os.path.realpath(__file__)

# Getting the length of the string `MAIN_PATH` and assigning it to the variable `lenght`.
lenght = len(MAIN_PATH)

# Getting the path of the current file and then it is getting the path of the main folder of the
# project.
while path[-lenght:] != MAIN_PATH:
    path = os.path.dirname(path)

# Adding the path of the main folder of the project to the sys.path.
sys.path.append(path)

# Importing all the variables from the file `va_cfg.py`.
from module.assistant.utils.va_cfg import AUDIO_RECORD_PATH, DICTIONARY_PATH, LANGUAGE, VOICE_RECONITION_MODEL_PATH, TEST_VOICE_PATH, USERS_JSON, ENERGY_THRESHOLD


class VoiceReconition():

    """
    # Initializing the class for person recognition.
    # Logic:
    #   1) Load all necessary paths for audio
    #   2) Load the label-file list dictionary
    #   3) Load the label-user dictionary
    #   4) Load the path for the model.
    """

    def __init__(self):

        # Loading the JSON file that contains the path for the voices
        self.audio_path = {}
        self.get_audio_paths()
        
        # Setting the path to the audio file that we will be using.
        self.record = AUDIO_RECORD_PATH

        # Just loading the dictionary file and assigning it to the variable `self.dictionary`.
        self.dictionary = json.load(open(DICTIONARY_PATH))[LANGUAGE]

        # It creates a folder if it doesn't exist.
        for _, v in self.audio_path.items():
            os.makedirs(v, exist_ok=True)    
        os.makedirs(self.record, exist_ok=True)
        
        # Just assigning the path of the trained model to the variable `self.model_path`.
        os.makedirs(VOICE_RECONITION_MODEL_PATH, exist_ok=True)
        self.model_path = VOICE_RECONITION_MODEL_PATH + "voice_reconition_model.h5"

        # Just assigning the path of the test voice to the variable `self.test_voice_path`.
        self.test_voice_path = TEST_VOICE_PATH

    """
    # It gets the audio paths for training the model
    """
    def get_audio_paths(self):
        # Reading the json file and storing the data in a dictionary.
        try:
            for k,v in json.loads(open(USERS_JSON, encoding='utf-8').read()).items():
                self.audio_path[k] = v["path"]
        except:
            self.audio_path = {}

    """
    # Just computing the remainig time for the computation
    # Parameters:
    #   1) times: all times spent for each cicle [LIST[FLOAT]]
    #   2) it: progressive [INT]
    #   3) cicles: total number of iteration [INT]
    # Logic:
    #   1) Sums all elapsed partial times up to that cycle
    #   2) Compute the ramining time
    # Returns:
    #   1) remainig time in seconds [FLOAT]
    """
    def expected_time(self, times, it, cicles):
   
        # Summing the values in the array.
        sum = np.sum(times)

        # Returning the remaining time in seconds
        return (((sum/it)*cicles)/60 - sum/60)

    """
    # Print a progress bar for a process
    # Parameters:
    #   1) progress: the current number being processed [INT]
    #   2) total: The total number to be processed [INT]
    #   3) times: remainig time for complete the computation [FLOAT]
    #   4) label: The label, if it exists [STRING]
    """
    def progress_bar(self, progress, total, times, label=None):

        # Converting the time in minutes to seconds.
        minutes = int(times)
        seconds = int((times - minutes)*60)

        # Calculating the percentage of the progress.
        percent = 100*(progress/float(total))

        # Just creating a progress bar.
        bar = '█' * int(percent) + '-' * (100-int(percent))

        # Just printing a progress bar.
        if minutes > 0:
            if label:
                print(f"\033[1A\033[2K\rRemaining time: {minutes} minutes and {seconds} seconds\n|{bar}| {percent:.2f}% ({progress}/{total}) on label: '{label}'", end="\r")
            else:
                print(f"\033[1A\033[2K\rRemaining time: {minutes} minutes and {seconds} seconds\n|{bar}| {percent:.2f}% ({progress}/{total})", end="\r")
        else:
            if label:
                print(f"\033[1A\033[2K\rRemaining time: {seconds} seconds\n|{bar}| {percent:.2f}% ({progress}/{total}) on label: '{label}'", end="\r")
            else:
                print(f"\033[1A\033[2K\rRemaining time: {seconds} seconds\n|{bar}| {percent:.2f}% ({progress}/{total})", end="\r")
        
        if progress == total:
            if label:
                print(f"\033[1A\033[2K\rComplete!\n|{bar}| {percent:.2f}% ({progress}/{total}) on label '{label}'", end="\r")
                print("\n")
            else:
                print(f"\033[1A\033[2K\rComplete!\n|{bar}| {percent:.2f}% ({progress}/{total})", end="\r")
                print("\n")

    """
    # Audio processing for the normal model.
    # Logic:
    #   1) For each item in the label-list dictionary of files, load the audio and calculate its MFCC.
    #   2) Calculate the average and add it to a temporary list.
    #   3) Create and save the database.
    """

    def get_data(self):

        # Creating a dictionary with the keys being the labels and the values being the file paths.
        data = {}
        for k,v in self.audio_path.items():
            data[k]  = [v + file for file in os.listdir(v)]

        # Just printing the text "Training the model" in the language specified in the `va_cfg.py`
        # file.
        print(self.dictionary["training_model"][0])

        # Just creating an empty list.
        all_data = []

        # Just loading the audio files and calculating their MFCC.
        for label, list_of_file in data.items():

            # Just a counter.
            i = 1

            # Just calculating the length of the list of files.
            l = len(list_of_file)

            times = []

            for file in list_of_file:

                # Getting the time spent for the computation
                partial = time.time()

                # Loading the audio file and assigning it to the variable `data`. The variable `sr` is
                # the sampling rate of the audio file.
                data, sr = librosa.load(file)

                # Calculating the MFCC of the audio file.
                mfcc = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=40)

                # Calculating the average of the MFCC.
                mfcc = np.mean(mfcc.T, axis=0)

                # Appending the MFCC and the label to the list `all_data`.
                all_data.append([mfcc, label])

                times.append(time.time()-partial)

                self.progress_bar(i, l, self.expected_time(times, i, l), label = label)

                i+=1

        # Just printing the text "Saving the model" in the language specified in the `va_cfg.py` file.
        print(self.dictionary["saving_model"][0])

        # Creating a dataframe with two columns, `feature` and `class_label`. The `feature` column
        # contains the MFCC of the audio file and the `class_label` column contains the label of the
        # audio file.
        df = pd.DataFrame(all_data, columns=['feature', 'class_label'])

        df.to_pickle(VOICE_RECONITION_MODEL_PATH + "voice_reconition_processed_data.csv")

        # Printing the text "Done" in the language specified in the `va_cfg.py` file.
        print(self.dictionary["done_model"][0])

    """
    # Train the speech recognition model.
    # Logic:
    #   1) Load the processed audio database.
    #   2) Retrieve the processed values of the audio and labels.
    #   3) Prepare the data before passing it to the model.
    #   4) Split the data into 80% training and 20% testing.
    #   5) Create the model.
    #   6) Compile the model.
    #   7) Train the model with the data.
    #   8) Save the model.
    """
    def training_model(self):

        # Loading the dataframe saved in the path specified in the `va_cfg.py` file.
        df = pd.read_pickle(VOICE_RECONITION_MODEL_PATH + "voice_reconition_processed_data.csv")

        # Just retrieving the values of the column `feature` from the dataframe `df`.
        x = df['feature'].values

        # Just reshaping the data.
        x = np.concatenate(x, axis=0).reshape(len(x), 40)

        # Converting the column `class_label` of the dataframe `df` to a list and then converting it
        # to a numpy array.
        y = np.array(df['class_label'].tolist())
        
        # Converting the labels to one-hot encoding.
        y = to_categorical(y)

        # Splitting the data into 80% training and 20% testing.
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=42)

        # Creating a model with three layers. The first layer has 256 neurons, the second layer has
        # 256 neurons and the third layer has 3 neurons.
        model = Sequential([
            Dense(256, input_shape=x_train[0].shape),
            Activation('relu'),
            Dropout(0.5),
            Dense(256),
            Activation('relu'),
            Dropout(0.5),
            Dense(len(self.audio_path), activation='softmax')
        ])

        # Compiling the model.
        model.compile(
            loss="categorical_crossentropy",
            optimizer="adam",
            metrics=['accuracy']
        )
        
        # Training the model with the data.
        model.fit(x_train, y_train, epochs=100, batch_size=8,
                  validation_data=(x_test, y_test))
        
        # Saving the model to the path specified in the `va_cfg.py` file.
        model.save(self.model_path)

    """
    It is used to invoke the creation and training of the model.
    """
    def build_model(self):
        
        # Loading the audio paths for training the model
        self.get_audio_paths()
        
        # Loading the audio files and calculating their MFCC.
        self.get_data()
        
        # Training the model.
        self.training_model()
        
    """
    # Obtains the model's response from an audio file.
    # Parameters:
    #   1) file_path: The path of the audio file to be analyzed [STRING].
    # Logic:
    #   1) Load the model.
    #   2) Read the audio file and calculate its MFCC.
    #   3) Predict the user from the calculated MFCC.
    #   4) Verify if the user is known and with what probability (at least 90%).
    # Returns:
    #   1) The label of the recognized/unrecognized user [STRING].
    """
    def get_user(self, file_path):
        
        try:
            # Loading the model from the path specified in the `va_cfg.py` file.
            model = load_model(self.model_path)
            
            # Loading the audio file and assigning it to the variable `audio`. The variable `sr` is the
            # sampling rate of the audio file.
            audio, sr = librosa.load(file_path)
            
            # Calculating the MFCC of the audio file.
            mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
            
            # Calculating the average of the MFCC.
            mfcc=np.mean(mfcc.T, axis=0)
            
            # Predicting the user from the calculated MFCC.
            prediction = model.predict(np.expand_dims(mfcc, axis=0))

            # Converting the prediction from a numpy array to a list.
            prediction = prediction[0].tolist()
            
            # Just converting the index of the maximum value of the list `prediction` to a string.
            predicted_user = str(prediction.index(max(prediction)))

            # Just verifying if the user is known and with what probability (at least 90%).
            if max(prediction)>0.90:
                return predicted_user
            else:
                return '0'
        except:
            return None
    
    """
    # Function to test the model using the microphone
    # Logic:
    #   1) Opens the microphone and listens for the message
    #   2) Saves the message
    #   3) Makes the prediction
    """
    def autoTestModel(self):
        
        # Creating an object of the class `Recognizer` from the `speech_recognition` module.
        reconizer = speech_recognition.Recognizer()
        
        # Opening the microphone and listening for the message.
        with speech_recognition.Microphone() as mic:
            
            # Setting the energy threshold for the microphone.
            reconizer.energy_threshold = ENERGY_THRESHOLD
            
            # Printing the text "Listening" in the language specified in the `va_cfg.py` file.
            print(self.dictionary["listening"][0])

            # Listening to the microphone and assigning the audio to the variable `audio`.
            audio = reconizer.listen(mic)

            # Opening the file `self.test_voice_path` in write binary mode and assigning it to the
            # variable `file`.
            with open(self.test_voice_path, 'wb') as file:
                
                # Writing the audio data to the file.
                file.write(audio.get_wav_data())   
                
            # Calling the function `get_user` and passing the path of the test voice as a parameter.
            self.get_user(self.test_voice_path)
    
if __name__ == '__main__':
    VoiceReconition().build_model()