import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
from deep_translator import GoogleTranslator
from module.date_time.utils.date_time_cfg import *
from word2number import w2n

class DateAndTimeCalculator():

    def __init__(self):
        
        self.weekday = STRING_TO_DAY

        self.days=DAY_TO_STRING

        self.months=MON_TO_STRING

        self.numbers=NUM_TO_STRING

        self.wrong = WRONG_RESULT_FROM_DAY_COMPUTATION
    
    def get_timezone_by_city(self, city):

        geolocator = Nominatim(user_agent='geoapiExercises')

        location = geolocator.geocode(city)

        try: 

            timezone = TimezoneFinder().timezone_at(lng=location.longitude, lat=location.latitude)

            return pytz.timezone(timezone)
        except:
            return None
        
    def extract_date(self, message_list):

        day = 0
        weekday = ""
        month = 0
        year = 0
        monthName = ""

        if 'oggi' in message_list:
            day = datetime.datetime.today().day
            month = datetime.datetime.today().month
            year = datetime.datetime.today().year
        else:
            day, month, year, days = self.extract_day(message_list)
            print(1, day, month, year)
            if day!=0 and month==0:
                month, year = self.extractMonth(message_list, day)
            print(2, day, month, year)
        if day not in self.wrong and month not in self.wrong:
            year = self.checkYear(message_list, day, month, year, days)
            print(3, day, month, year)
        if day not in self.wrong and month not in self.wrong and year not in self.wrong:
            weekday = self.weekday[str(datetime.datetime(year, month, day).weekday()+1)]
            monthName = self.months[str(month)]
        if day not in self.wrong:
            if str(day) in message_list:
                message_list.remove(str(day))
            if weekday.lower() in message_list:
                message_list.remove(weekday.lower())
            if weekday.lower().replace('ì', 'i') in message_list:
                message_list.remove(weekday.lower().replace('ì', 'i'))
        if month not in self.wrong:
            if str(month) in message_list:
                message_list.remove(str(month))
            if monthName.lower() in message_list:
                message_list.remove(monthName.lower())
        if year not in self.wrong:
            if str(year) in message_list:
                message_list.remove(str(year))
        ret = [day, weekday, month, monthName, year, days]
        return message_list, ret

    
    def extract_day(self, message_list):

        d=0
        m=0
        y=0
        days=0

        for el in message_list:
            if el.isnumeric():
                days = int(el)
        if 'giorni' in message_list or 'tra':
            if days == 0:
                t=""
                for el in message_list:
                    t = GoogleTranslator(source='italian', target='english').translate(el)
                    try:
                        days = w2n.word_to_num(t)
                    except:
                        pass


            if days < 1000000 and days!=0:
                if 'era' in message_list:
                    y = (datetime.datetime.today() - datetime.timedelta(days=days)).year
                    m = (datetime.datetime.today() - datetime.timedelta(days=days)).month
                    d = (datetime.datetime.today() - datetime.timedelta(days=days)).day
                else:
                    y = (datetime.datetime.today() + datetime.timedelta(days=days)).year
                    m = (datetime.datetime.today() + datetime.timedelta(days=days)).month
                    d = (datetime.datetime.today() + datetime.timedelta(days=days)).day
            else:
                if days>=1000000:
                    d=-1
                    m=-1
                    y=-1
                else:
                    d=-10
                    m=-10
                    y=-10
        elif d==0 and 'domani' in message_list:
            #CASO 1: se c'è 'domani' nella frase
            #EX: aggiungi all'agenda per domani
            if ('dopo' in message_list and 'domani' in message_list) or 'dopodomani' in message_list:
                d = (datetime.datetime.today() + datetime.timedelta(days=2)).day
                m = (datetime.datetime.today() + datetime.timedelta(days=2)).month
                y = (datetime.datetime.today() + datetime.timedelta(days=2)).year
            #CASO 2: se c'è 'dopo domani' nel messaggio
            #EX: aggiungi all'agenda per dopo domani
            else:
                d = (datetime.datetime.today() + datetime.timedelta(days=1)).day
                m = (datetime.datetime.today() + datetime.timedelta(days=1)).month
                y = (datetime.datetime.today() + datetime.timedelta(days=1)).year
        elif d==0 and 'ieri' in message_list:
            if ("l'altro" and "ieri" in message_list) or ("altro" and  "ieri" in message_list):
                d = (datetime.datetime.today() - datetime.timedelta(days=2)).day
                m = (datetime.datetime.today() - datetime.timedelta(days=2)).month
                y = (datetime.datetime.today() - datetime.timedelta(days=2)).year
            #CASO 2: se c'è 'dopo domani' nel messaggio
            #EX: aggiungi all'agenda per dopo domani
            else:
                d = (datetime.datetime.today() - datetime.timedelta(days=1)).day
                m = (datetime.datetime.today() - datetime.timedelta(days=1)).month
                y = (datetime.datetime.today() - datetime.timedelta(days=1)).year

        else:
            #CASO 3: cerca se c'è un numero nella frase:
            #EX: aggiungi all'agenda per il 20
            for i in range(1, 32):
                temp = str(i)
                if temp in message_list:# or self.numbers[str(i)] in message:
                    d = i
            if d == 0:
                #CASO 4: CI SIA UN GIORNO DELLA SETTIMANA
                #EX aggiungi in agenda per lunedì
                day_of_week =-1
                for el in list(self.days.keys()):
                    if el in message_list:
                        day_of_week = int(self.days[el])
                        break
                #SE LO TROVA, ELABORA IL GIORNO, IL MESE, L'ANNO CORRISPONDENTE
                if day_of_week != -1:
                    my_day = datetime.datetime.today().weekday()
                    if my_day > day_of_week:
                        diff = my_day-day_of_week
                    else:
                        diff = 7-(day_of_week-my_day)
                    
                    if "era" in message_list:
                        d = (datetime.datetime.today() - datetime.timedelta(days=diff)).day
                    else:
                        d = (datetime.datetime.today() + datetime.timedelta(days=diff)).day

        return d, m, y, days
    

    """
    # Estrae il mese in base al messaggio e il giorno estratto nel passaggio precedente
    # Parametri
    #   1) La lista di parole del messaggio dell'utente [LIST(STRING)]
    #   2) Il giorno estratto nei passaggi precedenti [INT]
    # Logica:
    #   1) Se trova un numero nel messaggio, il mese è quel numero
    #   2) Se non ha trovato niente, il mese è quello corrente.
    #   3) Se ha trovato un mese, calcola l'anno come
    #       3.1) se il mese corrente è maggiore di quello estratto e 'sarà' è nel messaggio. Allora sarà l'anno prossimo
    #       3.2) se il mese corrente è minore di quello estratto. Allora l'anno sarà quello corrente
    #       3.3) se 'era' è nel messaggio e il mese corrente è maggiore di quello estratto allora l'anno è il corrente
    #       3.4) se 'era' è nel messaggio e il mese corrente è minore di quello estratto allora l'anno è il passato
    #       3.5) se il giorno di oggi è maggiore di quello estratto, l'anno è quello tra un anno
    #       3.6) sennò l'anno è quello corrente
    # Ritorna:
    #   1) il mese estratto oppure 0 [INT]
    #   2) l'anno estratto oppure 0 [INT]
    """
    def extractMonth(self, message, day):

        m = 0
        y = 0

        for i in range(1, 13):
            if self.months[str(i)].lower() in message:
                m = i
                break
        if m == 0:
            if "era" in message:
                if day > datetime.datetime.today().day:
                    m = (datetime.datetime.today() - datetime.timedelta(days=30)).month
                    y = (datetime.datetime.today() - datetime.timedelta(days=30)).year
                else:
                    m = datetime.datetime.today().month
                    y = datetime.datetime.today().year
            else:
                if day > datetime.datetime.today().day:
                    m = datetime.datetime.today().month
                    y = datetime.datetime.today().year
                else:
                    m = (datetime.datetime.today() + datetime.timedelta(days=30)).month
                    y = (datetime.datetime.today() + datetime.timedelta(days=30)).year

        else:
            my_day = datetime.datetime.today().day
            my_month = datetime.datetime.today().month
            if m < my_month and 'sarà' in message:
                y = (datetime.datetime.today() + datetime.timedelta(days=365)).year
            elif m>my_month:
                y= datetime.datetime.today().year
            elif m<my_month and 'era' in message:
                y = datetime.datetime.today().year
            elif m>my_month and 'era' in message:
                y = (datetime.datetime.today() - datetime.timedelta(days=365)).year
            else:
                if my_day>=day:
                    y = (datetime.datetime.today() + datetime.timedelta(days=365)).year
                else:
                    y= datetime.datetime.today().year

        return m, y

    """
    # Controlla che l'anno estratto sia quello corretto
    # Parametri:
    #   1) la lista di parole del messaggio dell'utente [LIST(STRING)]
    #   2) il giorno estratto [INT]
    #   3) il mese estratto [INT]
    #   4) l'anno estratto [INT]
    # Logica:
    #   1) estrae tutti i numeri presenti nel messaggio
    #   2) controlla che i numeri non corrispondano al giorno e al mese estratto e che l'anno sia diverso da quello estratto
    #   3) se è diverso, l'anno sarà quello corretto
    # Ritorna:
    #   1) l'anno estratto o quello calcolato [INT]
    """
    def checkYear(self, message, day, month, year, days):
        # Estraiamo tutti i numeri presenti nella stringa message
        nums = [int(x) for x in message if x.isnumeric()]

        # Filtriamo la lista dei numeri per tenere solo quelli che non sono uguali a day, month o year
        nums = list(filter(lambda x: x != day and x != month and x != year and x!=days, nums))

        # Se non ci sono numeri rimasti, restituiamo l'anno originale
        if not nums:
            return year

        # Altrimenti, restituiamo il primo elemento della lista filtrata
        return nums[0]

    """
    # Prende l'anno corrente.
    # Ritorna
    #   1) L'anno corrente [DATETIME]
    """
    def getCurrentYear(self):
        return datetime.datetime.today().year