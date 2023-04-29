##################### VOCAL_ASSISTANT######################
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

import utils.configurations as cfg

# Getting the list of the allowed users from the configurations file.
USERS_JSON = "module/assistant/utils/dictionary/user.json"

# Getting the language of the assistant from the configurations file.
LANGUAGE = cfg.LANGUAGE


# Getting the language of the assistant from the configurations file and then it is
# setting the language of the recognizer.
if LANGUAGE == 'ITALIAN':
    RECOGNIZER_LANG = 'it-IT'
else:
    RECOGNIZER_LANG = 'en-US'

# Getting the path of the intents files.
INTENTS_PATH = cfg.INTENTS_PATH

# Getting the path of the dictionary file.
DICTIONARY_PATH = cfg.DICTIONARY_PATH

# Setting the speaker rate to 200.
SPEAKER_RATE = 200

# The threshold of the energy of the voice.
ENERGY_THRESHOLD=1800

# The path of the audio file that is recorded by the assistant.
AUDIO_PATH = 'module/assistant/utils/audio/audioRecord/AUDIO_{}.wav'

# The path of the audio file that is recorded by the assistant.
AUDIO_RECORD_PATH = "module/assistant/utils/audio/audioRecord/"

# The path of the audio file that is used to test the model.
TEST_VOICE_PATH = "module/assistant/utils/audio/testVoice/test.wav"

# The path of the model that is used to recognize the voice.
VOICE_RECONITION_MODEL_PATH = "module/assistant/utils/model/voice_reconition/"

PREDICTOR_MODEL_PATH = "module/assistant/utils/model/predictor/"

WORD_MAPPING_PATH = "utils/words_mapping.json"

#THRESHOLD FOR RESPONSE
ERROR_THRESHOLD = 0.2

FINAL_ERROR_THRESHOLD = 0.45

if LANGUAGE == 'ITALIAN':
    DUMMY_WORDS = ['con', 'alla', 'di', 'la', 'le', 'un', 'una', 'gli', 'per']
else:
    DUMMY_WORDS = ['with', 'to', 'of', 'a', 'the', 'for']


WEIGHT_LOGICAL_RESPONSE = 0.5

WEIGHT_RESPONSE = 1 - WEIGHT_LOGICAL_RESPONSE

TAG_FUNCTION_MAPPING = "utils/mapping.json"

CHAR_TO_IGNORE = cfg.CHAR_TO_IGNORE