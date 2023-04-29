import os

# Language to speech
LANGUAGE = "ITALIAN"

# The path to the intents.json file.
if LANGUAGE == 'ITALIAN':
    INTENTS_PATH = "utils/intents_it.json"
else:
    INTENTS_PATH = "utils/intents_eng.json"

DICTIONARY_PATH = "utils/dictionary.json"

MAIN_PATH = os.path.dirname(os.path.dirname(__file__))

CHAR_TO_IGNORE = ['?', '!', '.', ',', "'"]
