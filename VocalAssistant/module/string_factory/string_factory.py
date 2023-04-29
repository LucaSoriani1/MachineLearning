from module.string_factory.utils.string_cfg import *

import json

import datetime

class StringFactory():

    def __init__(self):

        self.char_to_ignore = CHAR_TO_IGNORE
        intents = json.loads(open(INTENTS_PATH, encoding='utf-8').read())
        self.tag_pattern = {}
        for el in intents['intents']:
            self.tag_pattern[el['tag']] = []
            for e in el['patterns']:
                temp = self.message_to_list(e)
                for t in temp:
                    if t not in self.tag_pattern[el['tag']]:
                        self.tag_pattern[el['tag']].append(t)



    """
    # Constructs the list of words contained in the message.
    # Parameters:
    #   1) message: The user's message [STRING].
    # Logic:
    #   1) Remove special characters if it must remove them
    #   2) Splits the message into words
    #   3) Takes the list of words without blanks
    #   4) For each word, makes it lower case
    # Returns:
    #   1) List of words in the message in lower case [LIST(STRING)]
    """
    def message_to_list(self, message):

        message = self.customize_message(message)

        message = list(message.split(" "))

        message = list(filter(None, message))

        return [el.lower() for el in message]



    """
    # Make the message custom by adding spaces instead of special characters.
    # Parameters:
    # 1) The user's message [STRING].
    # Logic:
    # 1) Replaces special characters with a space
    # Returns:
    # 1) the message without special characters [STRING]
    """
    def customize_message(self, message):
        # Replace all letters to be ignored with spaces
        # using a regular expression to match them all at once
        for char in self.char_to_ignore:
            while char in message:
                message = message.replace(char, "")


        return message
    
    """
    # Removes words that are present in the patterns for that respective tag
    # Parameters:
    #   1) message_list: List of words in the message [LIST(STRING)].
    #   2) tag: The reference tag [STRING]
    # Logic:
    #   1) Takes the list of words appearing in the intents for that tag
    #   2) For each word, if it is contained in the message word list
    #   3) Adds it to a temporary list
    #   4) For each word in the temporary list, removes it from the message word list
    # Returns:
    #   1) List of words that are NOT part of the pattern of that tag [LIST(STRING)]
    """
    def strip_message_from_pattern(self, message_list, tag):
        
        # Creates a temporary set that contains the words that appear in the intents for that tag
        # and are present in the message word list
        temp = {el for el in self.tag_pattern[tag] if el in message_list}

        # Removes any words in the temporary set from the message word list
        # Returns the list of words that are NOT part of the pattern of that tag
        return [el for el in message_list if el not in temp]
    
    """
    # Constructs the sentence from the word list
    # Parameters:
    #   1) message The message word list [LIST(STIRNG)].
    # Logic:
    #   1) Takes the list and constructs the sentence
    #   2) Removes spaces at the end
    # Returns:
    #   1) The constructed message [STRING]
    """
    def list_to_message(self, message):

        # Merge list elements into a single string, using a space as separator
        return " ".join(message)
    
    """
    # Constructs the first part of the message to be returned for a specific city.
    # Parameters:
    #   1) message: The user's message [STRING]
    #   2) city: The extracted city [STRING]
    # Logic:

    # Returns:
    #   1) The first part of the message with the city [STRING]
    """

    def get_answer_by_city_and_time(self, message, timezone, city, language):

        dtn = datetime.datetime.now(timezone) if timezone else datetime.datetime.now()

        hours = dtn.strftime("%H")
        minutes = dtn.strftime("%M")

        if language == 'ITALIAN':

            return self.get_answer_by_city_and_time_ita(message, hours, minutes, city)
        else:
            return self.get_answer_by_city_and_time_eng(hours, minutes, city)

    def get_answer_by_city_and_time_ita(self, message, hours, minutes, city):

        answer = self.get_answer_by_city_it(message, city)

        answer += ' è mezzanotte' if hours == '00' else " è l'una" if hours == '01' else f' sono le {str(int(hours))}'

        answer += " in punto" if minutes == '00' else ' e un minuto' if minutes == '01' else f' e {minutes} minuti'

        return answer.capitalize()
    
    def get_answer_by_city_it(self, message, city):
        if city:
            city_index = message.lower().find(city.lower())

            if city.lower().startswith('a'):

                return 'Ad ' + city
            elif city_index != -1 and message[city_index-2] == 'a':
                return 'A ' + city
            else:
                return 'In ' + city
        return ''

    def get_answer_by_city_and_time_eng(self, hours, minutes, city):

        answer = 'in ' + city

        hours = int(hours)
        minutes = int(minutes)

        suffix = 'a.m.' if 0 < hours <= 12 else 'p.m.'

        hours = 12 if hours == 0 else hours - 12 if hours > 12 else hours

        answer = f"It's {hours}:{minutes} {suffix} " + answer

        return answer
    
    def get_answer_by_date(self, date, message):

        message_list = self.message_to_list(message)

        if date[0] not in WRONG_DATE_RESULTS:

            wd = date[1]

            if wd.lower() in message or wd.lower().replace('ì', 'i') in message:

                if 'è' in message or 'sarà' in message:
                    ans = wd + ' sarà il ' + str(date[0]) + ' ' + date[3] + ' ' + str(date[4])
                else:
                    ans = wd + ' era il ' + str(date[0]) + ' ' + date[3] + ' ' + str(date[4])
            elif "domani" in message:
                if "dopo domani" in message or 'dopodomani' in message:
                    ans = 'Dopo domani sarà ' + wd + ' ' + str(date[0]) + ' ' + date[3] + ' ' + str(date[4])
                else:
                    ans = 'Domani sarà ' + wd + ' ' + str(date[0]) + ' ' + date[3] + ' ' + str(date[4])
            elif 'oggi' in message:
                ans = 'Oggi è ' + wd + ' ' + str(date[0]) + ' ' + date[3] + ' ' + str(date[4])
            elif 'giorni' in message:
                g=0
                for el in message_list:
                    if el.isnumeric():
                        g=el
                        break
                if g==0:
                    g = date[-1]
                g=str(g)
                        
                if 'era' in message:
                    ans = g + ' giorni fa era ' + date[1] + ' ' + str(date[0]) + ' ' + date[3] + ' ' + str(date[4])
                else:
                    ans = 'Tra ' + g + ' giorni sarà ' + date[1] + ' ' + str(date[0]) + ' ' + date[3] + ' ' + str(date[4])
            else:
                ans = "Il " + str(date[0]) + ' ' + date[3] + ' ' + str(date[4])
                curr = datetime.datetime.today().strftime("%d-%m-%Y").split("-")
                curr.insert(1, "")
                curr.insert(3, "")
                computer_date = self.from_date_to_string(date)
                current_date = self.from_date_to_string(curr)
                if computer_date < current_date:
                    ans += " era " + date[1]
                else:
                    ans += ' sarà ' + date[1]
            
        else:
            if date[0] == 0 or date[0]==-10:
                ans = "Mi dispiace, credo di non aver capito bene"
            elif date[0] == -1:
                ans = "Mi dispiace, non sono così potente!"
        return ans

    def from_date_to_string(self, date):

        temp = str(date[0]) + '-' + str(date[2]) + '-' + str(date[4])

        return datetime.datetime.strptime(temp, '%d-%m-%Y')