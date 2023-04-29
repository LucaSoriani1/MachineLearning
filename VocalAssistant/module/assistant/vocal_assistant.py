# Importing the pyttsx3 module and renaming it to tts.
import pyttsx3 as tts

# It's importing the `speech_recognition` module.
import speech_recognition

# It's importing the `json` module.
import json

# It's importing the `noisereduce` module and renaming it to `nr`.
import noisereduce as nr

# It's just importing the `soundfile` module and renaming it to `sf`.
import soundfile as sf

# It's just importing the `librosa` module.
import librosa

import random

# It's just preventing the creation of the `.pyc` files.
import sys
sys.dont_write_bytecode = True

# It's just importing the `os` module.
import os

# It's just importing the `datetime` module.
from datetime import datetime

try:
    # It's just importing the `va_cfg.py` configuration file fpr vocal_assistant.
    from module.assistant.utils.va_cfg import *

    # It's importing the `VoiceReconition` class from the `voice_recognition.py` file.
    from module.assistant.utils.voice_recognition import VoiceReconition

    # It's importing the `Predictor` class from the `p  redictor.py` file.
    from module.assistant.utils.predictor import Predictor
except:
    # It's just importing the `va_cfg.py` configuration file fpr vocal_assistant.
    from utils.va_cfg import *

    # It's importing the `VoiceReconition` class from the `voice_recognition.py` file.
    from utils.voice_recognition import VoiceReconition

    # It's importing the `Predictor` class from the `p  redictor.py` file.
    from utils.predictor import Predictor


class VocalAssistant():
    
    """
    # Initialization of the voice assistant
    # Logic:
    #     1) Initialization of the speaker and setting its properties
    #     2) Initialization of the recognizer
    #     3) Definition of authorized users
    #     4) Definition of vocabulary for tag-responses
    """
    def __init__(self):

        # It's initializing the speaker.
        self.speaker = tts.init("sapi5")

        # It's just setting the language of the speaker.
        voices = self.speaker.getProperty('voices')
        if LANGUAGE == 'ITALIAN':
            for v in voices:
                if 'ita' in v.name.lower():
                    id = v.id
                    break
        else:
            for v in voices:
                if 'eng' in v.name.lower():
                    id = v.id
                    break

        # It's setting the speaker's rate.
        self.speaker.setProperty('rate', SPEAKER_RATE)

        # Setting the voice property of the speaker object to the id of the voice.
        self.speaker.setProperty('voice', id)
        
        # It's initializing the recognizer.
        self.recognizer = speech_recognition.Recognizer()
        
        # Loading the allowed user file into a dictionary.
        try:
            self.users = json.loads(open(USERS_JSON, encoding='utf-8').read())
        except:
            self.users = {}
        
        self.intents = json.loads(open(INTENTS_PATH, encoding='utf-8').read())

        # Loading the dictionary file and converting it into a dictionary.
        self.dictionary = json.loads(open(DICTIONARY_PATH, encoding='utf-8').read())[LANGUAGE]

        # It's just initializing the `self.ans` dictionary.
        self.answer = {}

        for el in self.intents['intents']:
            
            self.answer[el['tag']] = el['responses']

        self.function_mapping = json.loads(open(TAG_FUNCTION_MAPPING, 'r', encoding='utf-8').read())
            
        # Creating an object of the class VoiceRecognition.
        self.vr = VoiceReconition()

        self.pr = Predictor(self.intents)


    """
    # Phrase to be said by the speech synthesiser
    # Parameters:
    #   1) sentence: The sentence the synthesiser is to say [STRING].
    # Logic:
    #   1) It writes the sentence and who said it to the log file.
    #   2) The synthesiser says the sentence
    """
    def speaker_say(self, sentence):

        # Saying the sentence.
        self.speaker.say(sentence)

        # A method of the pyttsx3 module that makes the speaker say the sentence.
        self.speaker.runAndWait()

    
    """
    # Converts speech to text. It takes the audio from the user and transforms it into a message.
    # Logic:
    #   1) Opens the microphone
    #   2) Sets the energy threshold
    #   3) Records the audio
    #   4) Saves the audio and cleans it from noise and silence
    #   5) User recognition
    #   6) If the user is allowed, it saves the audio with the appropriate prefix, otherwise '0'
    # Returns:
    #   1) path: the path of the audio [STRING]
    #   2) audio: the audio recorder [AUDIODATA] 
    """
    def get_audio(self):
        
        # It's just initializing the `message` variable.
        path = "" 
        audio = None
        
        try:
            with speech_recognition.Microphone() as mic:
                
                # It's setting the energy threshold.
                self.recognizer.energy_threshold = ENERGY_THRESHOLD
                
                # It's just printing the message "I'm listening" in the language that the user has
                # chosen.
                print(self.dictionary["listening"][0])

                # Listening to the user.
                audio = self.recognizer.listen(mic, timeout=10)
                
                # It's just creating the path to the audio file.
                path=AUDIO_PATH.format(self.get_date())
                               
                # It's just opening the file in write binary mode.
                with open(path, 'wb') as file:
                
                    # It's just writing the audio data in the file.
                    file.write(audio.get_wav_data())
                    
                # It's just removing the noise and the silence from the audio file.
                self.noise_silence(path)
                
                        
        except speech_recognition.exceptions.UnknownValueError:
            pass
        except speech_recognition.exceptions.WaitTimeoutError:
            pass
        
        return path, audio
    
    """
    Takes today's date and time as a string
    Returns:
        1) Today's date and time as a string ('Ymd_HMS') [STRING]
    """
    def get_date(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    """
    # Removes noise and silence from an audio file
    # Parameters:
    #   1) path: the path of the audio file [STRING]
    # Logic:
    #   1) reads the audio file, obtaining its values and sample rate
    #   2) reduces both stationary and non-stationary noise
    #   3) removes the noise from both channels
    #   4) writes the processed file with stationary and non-stationary noise removed
    """
    def noise_silence(self, path):
        
        # It's just reading the audio file and returning the data and the sample rate.
        data, rate = sf.read(path)
        
        # It's just reducing the stationary noise.
        reduced_noise_s = nr.reduce_noise(y=data, sr=rate, n_std_thresh_stationary=1.5, stationary=True)
        
        # It's just reducing the non-stationary noise.
        reduced_noise_ns = nr.reduce_noise(y = data, sr=rate, thresh_n_mult_nonstationary=2,stationary=False)
        
        # It's just trimming the audio file.
        trimmed_s = librosa.effects.trim(reduced_noise_s, top_db=75)

        # It's just trimming the audio file.
        trimmed_ns = librosa.effects.trim(reduced_noise_ns, top_db=75)
        
        # It's just writing the audio file with the stationary noise removed.
        sf.write(path, trimmed_s[0], samplerate=rate)
        
        # It's just writing the audio file with the non-stationary noise removed.
        sf.write(path.replace('.wav', '_ns.wav'), trimmed_ns[0], samplerate=rate)
  
    """
    # From the audio identifies the user who spoke and the message of what was said
    # Parameters:
    #   1) path: The path of the audio [STRING].
    #   2) audio: The audio itself [AUDIODATA]
    # Logic:
    #   1) The audio is analysed
    #   2) The user is recognised
    #   3) If the user is among those authorised, returns the message as text
    # Returns:
    #   1) message: the message as text [STRING].
    #   2) user: the user id [STRING]
    """
    def get_user(self, path, audio):

        # It's just initializing the `message` variable.
        message = ""

        # It's just getting the user from the audio file.
        user = self.vr.get_user(path)

        # It's just checking if the user is in the list of the allowed users. If it is, it's just
        # returning the message and the user.
        if user in list(self.users.keys()):
            
            try:
                # It's just recognizing the message from the audio file.
                message = self.recognizer.recognize_google(audio, language=RECOGNIZER_LANG)
            except:
                pass

        return message, user

    """
    # It add a allowed user to the system:
    # Logic:
    #   1) The system will print 10 sentences that the user will pronunce
    #   2) Each audio will be saved in the specific folder for that user
    #   3) The system ask to digit the name for that user
    """
    def add_user(self):
        
        # It's just saying the message for adding user in the language that the user has
        # chosen.
        self.speaker_say(self.dictionary['add_user_start'])

        # Checking if the list is empty. If it is empty, it assigns the value of 1 to the variable id.
        # If it is not empty, it assigns the value of the length of the list to the variable id.
        if len(self.users)==0:
            id = "1"
        else:
            id = str(len(self.users))

        # For each sentence, taking the audio from the user and saving it in a folder.
        for sentence in self.dictionary['add_user_sentences']:

            # It's just printing the sentence that the user has to say.
            print('-------> ', sentence)

            # Getting the audio from the user
            path, audio = self.get_audio()

            # Writing the audio data to a file.
            with open(path, "wb") as file:
                file.write(audio.get_wav_data())
            
            abs_path = os.path.abspath(path.replace(path[path.index("audioRecord/"):], f"audioRecord/voice_{id}/")) + "\\"

            # Creating a new directory for the new user.
            os.makedirs(abs_path, exist_ok=True)
            
            # Recall the move_and_rename_audio method
            self.move_and_rename_audio(path, id)
        # It's just saying the message for inserting the name of the new user in the language that the user has
        # chosen.
        self.speaker_say(self.dictionary['add_user'])

        # Asking the user to input a name.
        name = input("--->  ")
        
        # Creating a dictionary with the key being the user id and the value being a dictionary with
        # the keys path, name, and allowed.
        self.users[id] = {
            "path":abs_path,
            "name": name,
            "allowed":"True"
        }

        # Creating the folder if not exists
        os.makedirs(USERS_JSON.replace("user.json", ""), exist_ok=True)

        # Writing the users dictionary to a file called users.json.
        with open(USERS_JSON, "w", encoding='utf-8') as file:
            json.dump(self.users, file)

    """
    # It takes the background noise
    # Parameters:
    #   1) cicles: The number of cicles. DEFAULT=10 [INT]
    # Logic:
    #   1) The For-cycle starts and take the noise for the number of cycles specified.
    #   2) Each audio is processed, and moving to the noise path
    """
    def take_some_noise(self, cicles=10):

        # It just saying that it will take the noise in the leanguage chosen.
        self.speaker_say(self.dictionary['initial_load_noise_start'])

        # Recording audio from the microphone and saving it to a file.
        for i in range(cicles):

            # Print the progressive
            print(f"---> {i+1}/{cicles}")

            # Get the background noise
            path, audio = self.get_audio()

            # Writing the audio data to a file.
            with open(path, "wb") as file:
                file.write(audio.get_wav_data())
            
            abs_path = os.path.abspath(path.replace(path[path.index("audioRecord/"):], "audioRecord/noise/")) + "\\"

            # Creating a new directory for the new user.
            os.makedirs(abs_path, exist_ok=True)

            # Renaming and moving the path for audio
            self.move_and_rename_audio(path, "0", noise=True)
        
        # Creating a dictionary with the key '0' and the value is a dictionary with the keys 'path',
        # 'name', and 'allowed'.
        self.users['0'] = {
            "path": abs_path,
            "name": "Other",
            "allowed": "False"
        }

        # Writing the users dictionary to a file called users.json.
        with open(USERS_JSON, "w", encoding='utf-8') as file:
            json.dump(self.users, file)
    
    """
    # It just take the messave from the user voice.
    # Logic:
    #   1) It gets the audio
    #   2) It recognizes the user
    #   3) if it is not, then start the initial load
    #   4) else, return the message
    # Returns:
    #   1) message: The message that the user says [STRING]
    """
    def listen_and_processing(self):

        # Creating a variable called message and assigning it an empty string.
        message = ""

        # It recall the get_audio method
        path, audio = self.get_audio()

        if path and audio:
            # It recall the get_user method
            message, user = self.get_user(path, audio)        
            
            # If the user if not define, then start the initial load, else getting the message
            if not user:
                # Calling the add_user method
                self.add_user()

                # Calling the take_some_noise method
                self.take_some_noise()

                # Moving the audio file to the new directory and renaming it.
                path = self.move_and_rename_audio(path, '1')
                
                # Building the model
                self.vr.build_model()

                # Getting the user's message and audio.
                message, _ = self.get_user(path, audio)
            else:

                # Moving the audio file to the new directory and renaming it.
                self.move_and_rename_audio(path, user)

        return message

    """
    # It simple move the audio created in the correct folder. 
    # Parameters:
    #   1) path: The path of the audio di move [STRING]
    #   2) user: The id for the user, in order to move in the right directory [STRING]
    #   3) noise: If the audio is the noise or not. DEFAULT False [BOOLEAN]
    # Logic:
    #   1) It creates the path for the non-stationary audio
    #   2) If creates the new path, i.e. the path in which move the audio
    #   3) It moves the audio
    # Returns:
    #   1) new_path: The new path for the audio [STRING]
    """
    def move_and_rename_audio(self, path, user, noise=False):
        
        # Replacing the .wav extension with _ns.wav
        other = path.replace(".wav", "_ns.wav")
        
        # Replacing the path of the file with a new path.
        if noise or user =='0':
            new_path = path.replace(path[path.index("AUDIO"):],f"/noise/" + user + '_' + path[path.index("AUDIO"):])
        else:
            new_path = path.replace(path[path.index("AUDIO"):],f"/voice_{user}/" + user + '_' + path[path.index("AUDIO"):])
        
        # Replacing the .wav extension with _ns.wav
        new_other_path = new_path.replace(".wav", "_ns.wav")

        # Moving the audios
        os.rename(path, new_path)
        os.rename(other, new_other_path)
        return new_path
    
    def elaborate_message(self, message, speech=True):
        
        tag = self.pr.get_tag(message)

        answer = random.choice(self.answer[tag])

        function_to_call = self.function_mapping[tag]

        return answer, tag, function_to_call

if __name__ == '__main__':
    # VocalAssistant().take_some_noise()
    # VocalAssistant().vr.build_model()
    VocalAssistant().pr.training_model()
