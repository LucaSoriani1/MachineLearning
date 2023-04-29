# Importing the Natural Language Toolkit (NLTK) library.
import nltk

# Importing the WordNetLemmatizer class from the nltk.stem module.
from nltk.stem import WordNetLemmatizer

import pickle

import random

import numpy as np

import json

from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Dropout
from tensorflow.python.keras.optimizer_v2 import gradient_descent

# Importing the load_model function from the tensorflow.python.keras.models module.
from tensorflow.python.keras.models import load_model


# It's just importing the `os` module.
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

from module.assistant.utils.va_cfg import PREDICTOR_MODEL_PATH, WORD_MAPPING_PATH, ERROR_THRESHOLD, WORD_MAPPING_PATH, DUMMY_WORDS, WEIGHT_LOGICAL_RESPONSE, WEIGHT_RESPONSE, FINAL_ERROR_THRESHOLD, CHAR_TO_IGNORE

class Predictor():

    """
    # Initialise Predictor class
    # Logic:
    #   1) Initialise the lemmatizer
    #   2) Load the intents file
    #   3) List of answers for not understanding
    #   4) List of useless words at the end of the message
    #   5) The mapping file with the intents
    #   6) The mapping file with words
    #   7) The pickle file of the words produced by the training
    #   8) The pickle file of the classes produced by the training
    #   9) The model produced by the training
    #   10) The StringFactory class
    """
    def __init__(self, intents):
        
        # Initializing the WordNetLemmatizer class.
        self.lemmatizer = WordNetLemmatizer()

        # Assigning the value of the `intents` parameter to the `self.intents` attribute.
        self.intents = intents

        self.char_to_ignore = CHAR_TO_IGNORE

        self.words = pickle.load(open(PREDICTOR_MODEL_PATH + "words.pkl", 'rb'))

        self.classes = pickle.load(open(PREDICTOR_MODEL_PATH + "classes.pkl", 'rb'))

        self.model = load_model(PREDICTOR_MODEL_PATH + 'predictor_trained_model.h5')

        self.words_map = json.loads(open(WORD_MAPPING_PATH, 'r', encoding='utf-8').read())

        self.dummy_words = DUMMY_WORDS

    """
    # Returns the response for the user's message
    # Parameters:
    #   1) sentence: The user's message [STRING].
    # Logic:
    #   1) Takes the message and puts all characters in lower case.
    #   2) Takes the response from the neural network
    #   3) Takes the logical response
    #   4) From the logical and neural network response, returns the weighted average
    #   5) If the probability is greater than the threshold:
    #       5.1) then takes the tag, the list of responses
    #       5.2) takes a random answer
    #   6) Otherwise try taking the tag for which the user's message matches
    #       6.1) If it doesn't, then unrecognised message
    # Returns:
    #   1) the response message [STRING]
    """
    def get_tag(self, sentence):

        sentence = sentence.lower()

        responses = self.predict_class(sentence)

        logical_respones = self.get_logical_response(sentence)

        intents_list = self.get_weighted_mean(responses, logical_respones)

        if float(intents_list[0]['probability']) >= FINAL_ERROR_THRESHOLD:

            return intents_list[0]['intents']
        
        else:
            
            tag = self.search_tag(intents_list, sentence)
            if tag:
                return tag
            else:
                return 'not_understand'

    """
    # Last attempt to give an answer by searching for the sentence in the patterns
    # Parameters:
    #   1) intents_list: List of intents-probability dictionaries [LIST({'intents':STRING, 'probability':FLOAT})
    #   2) sentence: The user's message [STRING].
    # Logic:
    #   1) Takes all tags from the list of dictionaries
    #   2) Takes the phrase and checks if it is present in the patterns for each expected tag
    #   3) If it finds it, it assigns the random response and reference tag
    # Returns:
    #   1) The reference tag [STRING]
    """
    def search_tag(self, intents_list, sentence):

        intents = [intent['intents'] for intent in intents_list]

        for intent in self.intents['intents']:
            if intent['tag'] in intents:
                if any(sentence in pattern.lower() for pattern in intent['patterns']):
                    return intent['tag']
        return None

    """
    # Returns the response of the message passed
    # Parameters:
    #   1) responses: List of dictionaries coming out of the neural network [LIST({'intents':STRING, 'probability':FLOAT})
    #   2) logical_responses: List of dictionaries which comes out of the logical response [LIST({'intents':STRING, 'probability':FLOAT})
    # Logic:
    #   1) If the length of the neural network's list of dictionaries is 0, then the answer will only be the logical one
    #   2) I create a list of all the intents in logical and nlp
    #   3) For each intents, it sums the weighted logical response and the weighted neural network response
    #   4) Creates the intents-probability list sorted by probability
    # Returns:
    #   1) List of intents-probability dictionaries [LIST({'intents':STRING, 'probability':FLOAT})
    """
    def get_weighted_mean(self, responses, logical_respones):
        # If the response by the model returns an empty list, it means that it didn't find any intent. In this
        # case, the logical classifier is used.
        if not responses:

            # It sorts the list of dictionaries by the value of the key "probability".
            return sorted(logical_respones, key=lambda x: x['probability'], reverse=True)
        
        else:
            ret=[]

            # Creating a list of intents that are in both the logical and the NLP.
            ints = []
            for el in logical_respones:
                if el['intents'] not in ints:
                    ints.append(el['intents'])

            for el in responses:
                if el['intents'] not in ints:
                    ints.append(el['intents'])

            # Taking the top intents from the NLP and the top intents from the logical and combines
            # them into a single list of intents, sorted by probability.
            for i in ints:
                temp = {}

                # Getting the probability of the intent from the logical classifier and the NLP
                # engine.
                prob_L = 0
                prob_N = 0
                for el in logical_respones:
                    if i in el['intents']:
                        prob_L = el['probability']
                        break
                for el in responses:
                    if i in el['intents']:
                        prob_N = el['probability']
                        break
                    
                # Creating a list of dictionaries, each dictionary containing the intent and the
                # probability of the intent.
                temp['intents'] = i
                temp['probability'] = str(float(prob_L)*WEIGHT_LOGICAL_RESPONSE + float(prob_N)*WEIGHT_RESPONSE)
                ret.append(temp)

            # It sorts the list of dictionaries by the value of the key "probability".
            return sorted(ret, key=lambda x: x['probability'], reverse=True)

    """
    # Returns the logical response for the message passed
    # Parameters:
    #   1) sentence: The user's message [STRING].
    # Logic:
    #   1) Removes special characters from the message
    #   2) From the message, takes the list of words contained in the message
    #   3) Creates a dictionary with key a word from the message and value the tags in which the word appears
    #   4) Creates a dictionary with key the reference tag and value the tags in which the word appears:
    #       4.1) TOT: the total value of all words belonging to that tag
    #       4.2) REC: the number of words belonging to that tag
    #   5) Get the total number of words in the message
    #   6) If the words are all 'dummyWords', then the probability is 0
    #   7) Construct a list of intents/probability where the prob is the REC/sum of all words in the message
    # Returns:
    #   1) tag_probabilities: List of dictionaries with tag-probability [LIST({'intents':STRING, 'probability':FLOAT})
    """
    def get_logical_response(self, sentence):

        for letter in self.char_to_ignore:
            sentence = sentence.replace(letter, ' ')

        # It splits the sentence into words and removes all the empty strings from the list.
        words = list(filter(None, list(sentence.lower().split(" "))))

        # Creating a dictionary with the words of the sentence as keys and the values are the intents
        # that the word is associated with.
        diz = {}
        for w in words:
            if w in self.words_map:
                diz[w] = self.words_map[w]

        # Creating a dictionary with the intents as keys and the values are dictionaries with the keys
        # "tot" and "rec". The value of "tot" is the sum of the probabilities of the words that are
        # associated with the intent, while the value of "rec" is the number of words that are
        # associated with the intent.
        inte = {}
        for w in diz:
            for el in diz[w]:
                if el in inte:
                    inte[el]["tot"] += diz[w][el]
                    inte[el]["rec"] += 1
                else:
                    inte[el] = {}
                    inte[el]["tot"] = diz[w][el]
                    inte[el]["rec"] = 1
        
        sum_word = len(list(diz.keys()))

        # Check if all words in sentence are classified as dummy words
        if set(list(diz.keys())).issubset(self.dummy_words):
            sum_word = 10 ** 6
            
        # Creating a list of dictionaries, each containing the tag and probability.
        tag_probabilities = []

        for w in inte:
            temp = {}
            temp['intents'] = w
            temp['probability'] = inte[w]['rec']/sum_word
            tag_probabilities.append(temp)
        
        return tag_probabilities

    """
    # Predicts the user's message class
    # Parameters:
    #   1) The user's message
    # Logic:
    #   1) Takes the 0/1 list to predict the class
    #   2) Predicts the result for the passed 0/1 list
    #   3) Sorts the results by probability, putting the most likely one first
    # Returns:
    #   1) List of dictionaries with probabilities [LIST({'itents':STRING, 'probability':FLOAT})
    """
    def predict_class(self, sentence):

        bow = self.bag_of_words(sentence)

        response = self.model.predict(np.array([bow]))[0]

        result = [[i,r] for i, r in enumerate(response) if r>ERROR_THRESHOLD]
        result.sort(key=lambda x: x[1], reverse=True)

        return_list = []

        for r in result:
            return_list.append({'intents': self.classes[r[0]], 'probability':str(r[1])})

        return return_list

    """
    # Create a list of integers representing words. The list will be given to the model to make predictions
    # Parameters:
    #   1) The user's message [STRING].
    # Logic:
    #   1) Takes the list of lemmanized words
    #   2) Creates the list of integers
    # Returns:
    #   1) List of integers [LIST[INT]]
    """
    def bag_of_words(self, sentence):

        # Calling the `cleanup_sentence` method and passing the `sentence` parameter.
        sentence_words = self.cleanup_sentence(sentence)

        bag = [0]*len(self.words)

        for w in sentence_words:
            for index, word in enumerate(self.words):
                if word == w:
                    bag[index] = 1
        
        return np.array(bag)

    """
    # Takes a message and returns the list of lemmatised words
    # Parameters:
    #   1) sentence: the message [STRING]
    # Logic:
    #   1) Extracts the tokenized word list of the message
    #   2) Extracts the list of lemmatised words from the list of tokenized words
    # Returns:
    #   1) sentence_words: The list of lemmatised words [LIST[STRING]]
    """
    def cleanup_sentence(self, sentence):

        # Tokenizing the sentence into words.
        sentence_words = nltk.word_tokenize(sentence)

        # Lemmatizing the word of sentence_words
        sentence_words = [self.lemmatizer.lemmatize(word) for word in sentence_words]

        return sentence_words

    """
    # Function for creating and training the intent recognition system
    # Logic:
    #   1) Loads the intents file
    #   2) For each tag, analyses the patterns and processes them by tokenizing and lemmatising them
    #   3) Creates two pickle documents: one for words and one for classes
    #   4) Creates a list of 0/1 representing words
    #   5) Mixes the data to train the model
    #   6) Divide the words into trains and tests
    #   7) Create the model
    #   8) Compile and feed the model
    #   9) Saves the model
    #   10) Create and save the word-tag dictionary
    """
    def training_model(self):

        words = []
        documents = []
        classes = []

        # Creating a list of words and classes.
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:

                # Tokenizing the words in the pattern.
                word_list = nltk.word_tokenize(pattern)

                # Adding the words in the `word_list` to the `words` list.
                words.extend(word_list)

                # Appending the word_list and the intent tag to the documents list.
                documents.append((word_list, intent['tag']))
                
                # Adding the intent tag to the classes list.
                if intent['tag'] not in classes:
                    classes.append(intent['tag'])
        
        # Lemmatizing the words in the words list.
        words = [self.lemmatizer.lemmatize(word) for word in words if word not in self.char_to_ignore]

        # Sorting the words in the words list and removing the duplicates.
        words = sorted(set(words))

        # Sorting the classes list and removing the duplicates.
        classes = sorted(set(classes))

        os.makedirs(PREDICTOR_MODEL_PATH, exist_ok=True)

        # Saving the words list to a file called words.pkl. "wb"="write in binary mode" 
        pickle.dump(words, open(PREDICTOR_MODEL_PATH + 'words.pkl', "wb"))

        # Saving the classes list to a file called classes.pkl.
        pickle.dump(classes, open(PREDICTOR_MODEL_PATH + 'classes.pkl', "wb"))

        # Creating an empty list.
        training = []

        # Creating a list of zeros with the length of the classes list.
        output_empty = [0]*len(classes)
        
        # The above code is creating a bag of words model.
        #Converting word to number in order to feed the neural network
        for doc in documents:
            bag=[]
            word_pat = doc[0]
            word_pat = [self.lemmatizer.lemmatize(word.lower()) for word in word_pat]
            for word in words:
                bag.append(1) if word in word_pat else bag.append(0)

            output_row = list(output_empty)
            output_row[classes.index(doc[1])] = 1
            training.append([bag, output_row])

        # Shuffling the training data.
        random.shuffle(training)

        # Converting the list to a numpy array.
        training = np.array(training)

        # Splitting the training data into two lists.
        train_x = list(training[:, 0])
        train_y = list(training[:, 1])


        model = Sequential()
        model.add(Dense(256, input_shape=(len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))

        sgd = gradient_descent.SGD(learning_rate=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        hist = model.fit(np.array(train_x), np.array(train_y), epochs=1000, batch_size=10, verbose=1)

        model.save(PREDICTOR_MODEL_PATH + 'predictor_trained_model.h5', hist)

        temp = {}

        for element in documents:
            for el in element[0]:
                el = el.lower()
                if el not in self.char_to_ignore:
                    if el in temp.keys():
                        if element[1] in temp[el].keys():
                            temp[el][element[1]] += 1
                        else:
                            temp[el][element[1]] = 1
                    else:
                        temp[el.lower()] = {
                            element[1] : 1
                        }
                        
        word_mapping={}
        for el in temp:
            sum=0
            dic = temp[el]
            for tag in dic:
                sum += dic[tag]
            
            word_mapping[el] = {}
            for tag in dic:
                word_mapping[el][tag] = dic[tag]/sum

        with open (WORD_MAPPING_PATH, "w+", encoding="utf-8") as f:
            json.dump(word_mapping, f, ensure_ascii=False)

        print('Done')
