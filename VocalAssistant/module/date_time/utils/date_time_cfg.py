
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

LANGUAGE = cfg.LANGUAGE

if LANGUAGE == 'ITALIAN':
    STRING_TO_DAY = {
        '1':'Lunedì',
        '2':'Martedì',
        '3':'Mercoledì',
        '4':'Giovedì',
        '5':'Venerdì',
        '6':'Sabato',
        '7':'Domenica'
    }

    NUM_TO_STRING={
                '1':'uno',
                '2':'due',
                '3':'tre',
                '4':'quattro',
                '5':'cinque',
                '6':'sei',
                '7':'sette',
                '8':'otto',
                '9':'nove',
                '10':'dieci',
                '11':'undici',
                '12':'dodici',
                '13':'tredici',
                '14':'quattordici',
                '15':'quindici',
                '16':'sedici',
                '17':'diciasette',
                '18':'diciotto',
                '19':'diciannove',
                '20':'venti',
                '21':'ventuno',
                '22':'ventidue',
                '23':'ventitre',
                '24':'ventiquattro',
                '25':'venticinque',
                '26':'ventisei',
                '27':'ventisette',
                '28':'ventotto',
                '29':'ventinove',
                '30':'trenta',
                '31':'trentuno'
            }

    MON_TO_STRING={
                "1":"Gennaio",
                "2":"Febbraio",
                "3":"Marzo",
                "4":"Aprile",
                "5":"Maggio",
                "6":"Giugno",
                "7":"Luglio",
                "8":"Agosto",
                "9":"Settembre",
                "10":"Ottobre",
                "11":"Novembre",
                "12":"Dicembre"
            }

    DAY_TO_STRING={
                    "lunedì":'0',
                    "lunedi":'0',
                    "martedì":'1',
                    "martedi":'1',
                    'mercoledì':'2',
                    'mercoledi':'2',
                    'giovedì':'3',
                    'giovedi':'3',
                    'venerdì':'4',
                    'venerdi':'4',
                    'sabato':'5',
                    'domenica':'6'
                    }
    
else:
    STRING_TO_DAY={
        '1':'Monday',
        '2':'Tuesday',
        '3':'Wednesday',
        '4':'Thursday',
        '5':'Friday',
        '6':'Saturday',
        '7':'Sunday'        
    }    

    NUM_TO_STRING={
                '1':'one',
                '2':'two',
                '3':'three',
                '4':'four',
                '5':'five',
                '6':'six',
                '7':'seven',
                '8':'eight',
                '9':'nine',
                '10':'ten',
                '11':'eleven',
                '12':'twelve',
                '13':'thirteen',
                '14':'fourteen',
                '15':'fifteen',
                '16':'sixteen',
                '17':'seventeen',
                '18':'eighteen',
                '19':'nineteen',
                '20':'twenty',
                '21':'twenty one',
                '22':'twenty two',
                '23':'twenty three',
                '24':'twenty four',
                '25':'twenty five',
                '26':'twenty six',
                '27':'twenty seven',
                '28':'twenty eight',
                '29':'twenty nine',
                '30':'thirty',
                '31':'thirty one'
            }

    MON_TO_STRING={
                "1":"January",
                "2":"Febraury",
                "3":"March",
                "4":"April",
                "5":"May",
                "6":"June",
                "7":"July",
                "8":"Agoust",
                "9":"September",
                "10":"October",
                "11":"November",
                "12":"December"
            }

    DAY_TO_STRING={
                    "monday":'0',
                    "tuesday":'1',
                    'wednsday':'2',
                    'thursday':'3',
                    'friday':'4',
                    'saturday':'5',
                    'sunday':'6'
                    }


WRONG_RESULT_FROM_DAY_COMPUTATION=[0, -1, -10]