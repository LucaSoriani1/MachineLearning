
from module.assistant.vocal_assistant import VocalAssistant
from module.string_factory.string_factory import StringFactory
from module.date_time.date_time_calculator import DateAndTimeCalculator
from utils.configurations import LANGUAGE
"""
# Call the function that takes and analyzes the user's audio.
"""
def get_message():
        va = VocalAssistant()
        return va.listen_and_processing()

"""
# This function analyses the message and returns a reply.
# The parameters are:
#   1) sentence: the user's message [STRING].
#   2) speech: boolean used to tell whether the response should be said [BOOLEAN].
# Logic:
#   1) Call the vocal assistant method to elaborate_message
# This returns:
#   1) the random answer from the list of possible answers for that [STRING] tag
#   2) the referential tag of the user's message [STRING]
#   3) the function to call for that tag [STRING]
"""
def elaborate_message(message, speech=True):
    va = VocalAssistant()
    return va.elaborate_message(message)

"""
# Call up the function of the Vocal Assistant module that makes it speak.
# Parameters 
#   1) message: the message to be played [STRING]
"""
def speaker_say(message):
    VocalAssistant().speaker_say(message)

"""
# Restituisce l'orario della città chiamata.
# I parametri sono:
#   1) Il messaggio dell'utente [STRING]
#   2) il tag di riferimento [STRING]
# La logica è:
#   1) cerca di estrarre la città
#   2) se trova la città costriusce l'inizio della risposta
#   3) poi estrae il timezone della città
#   4) se lo trova, da la risposta
#   5) se non trova la città, restituisce l'orario corrente
"""
def get_time_by_city(message, tag):
    
    sf = StringFactory()

    message_list = sf.message_to_list(message)
    
    # Extracting the city from the message.
    city = sf.strip_message_from_pattern(message_list, tag)

    if len(city)!=0 and message_list[message_list.index(city[0])-1] == "la":
        city.insert(0, 'La')
        
    # Getting the time of a city, if the city is not specified it gets the time of the current city.
    if len(city) != 0:

        city = sf.list_to_message(city).title()

        # initialAnswer = sf.get_answer_by_city(message, city, LANGUAGE)

        timezone = DateAndTimeCalculator().get_timezone_by_city(city)
        if timezone == None:
            answer = 'Mi dispiace, non conosco {}, prova con qualcos\'altro'.format(
                city.title())
        else:
            answer = sf.get_answer_by_city_and_time(message, timezone, city, LANGUAGE)

    else:
        answer = sf.get_answer_by_city_and_time(message, None, "", LANGUAGE)

    speaker_say(answer)

def get_date(message):

    sf = StringFactory()

    message_list = sf.message_to_list(message)

    _, date = DateAndTimeCalculator().extract_date(message_list)

    answrer = sf.get_answer_by_date(date, message)

    speaker_say(answrer)

"""
# activates the assistant so that it can take the message
# is useful if you want to leave it active but not take messages
# to activate it, say something containing 'computer'
"""
def activate():
    global actived
    actived = True

"""
# Disable the assistant so that it does not take messages
# but remains listening to be called
"""
def deactivate():
    global actived
    actived = False

"""
# Close the program. To call it say 'quit' or
# 'stop program'
"""
def shutdown():
    global done
    done = True

def main(d, a, t):

    global actived
    actived = a

    global done
    done = d
        
    while not done and not t:
        
        message = get_message()
        print("1) Message:", message)

        if message != "":

            answer, target, function_to_call = elaborate_message(message, speech=False)

            if target == "active":

                eval(function_to_call)

                speaker_say(answer)

                while actived:
                    
                    message = get_message()
                    print("2) Message:", message)
                    
                    if message != "":

                        answer, tag, function_to_call = elaborate_message(message)
                        
                        # try:
                        speaker_say(answer)
                        eval(function_to_call)
                        # except:
                        #     speaker_say(answer)
                        if tag == 'shutdown':
                            actived = False


            elif target == "shutdown":
                speaker_say(answer)
                eval(function_to_call)
                
if __name__ == '__main__':
    
    # done = False, the loop continues.
    # done = True, the loop stops.
    done = False

    # active = True, the assistant takes messages.
    # active = False, the assistant doesn't take messages.
    actived = False

    # test = False, the loop starts.
    # test = True, the loop doesn't start.
    test = False
    
    main(done, actived, test)
