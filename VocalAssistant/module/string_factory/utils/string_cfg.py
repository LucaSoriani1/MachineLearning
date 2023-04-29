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

CHAR_TO_IGNORE = cfg.CHAR_TO_IGNORE

INTENTS_PATH = cfg.INTENTS_PATH

WRONG_DATE_RESULTS = [0, -1, -10]