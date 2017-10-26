#!/usr/bin/python
# -*- coding: utf-8 -*-


import speech_recognition as sr
import serial
import csv
import time

ser = serial.Serial('/dev/tty.usbserial', 9600)


classToInt = {
    'umido': 1,
    'carta': 2,
    'plastica': 3,
    'na': 4
}


"""
    Stop words init
"""
with open('stopwords.txt') as f:
    stopWords = f.readlines()
stopWords = [x.strip() for x in stopWords]


"""
    database init
"""
database = list()
with open('wasteDB.csv') as db:
    reader = csv.reader(db, delimiter=';', quotechar='|')
    for row in reader:
        database.append({'tags': row[0].split(' '), 'class': row[1]})



#    removes stop words
def stopWordFilter(l):
    filtered = [x for x in l if x not in stopWords]
    return filtered


# recognize audio from Google
def recognizeAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        return r.recognize_google(audio, language='it-IT')
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "ERR SPEECH_RECOGNITION"
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return "ERR REQUEST"
 

def classify(string):

    if string == "ERR SPEECH_RECOGNITION" or string == "ERR REQUEST":
        return -1
    else:
        listString = string.split(' ')

        for stringa in listString:
            stringa.replace('u\'', '')

        print listString

        listString = stopWordFilter(listString)

        print listString

        classMatches = dict()
        for dbEntry in database:

            entryClass = dbEntry['class']

            if entryClass not in classMatches.keys():
                classMatches[entryClass] = 0

            entryScore = classMatches[entryClass]

            tags = dbEntry['tags']

            for tag in tags:
                if tag in listString:
                    entryScore += 1

            classMatches[entryClass] += entryScore

            print classMatches

        classMatches = sorted(classMatches, key=classMatches.get, reverse=True)

        winner = classMatches[:1]

        return winner


while True:

    if ser.readLine() == "PUSHED":

        raw_string = recognizeAudio();
        waste_class = classify(string = raw_string)[0]

        ser.write(classToInt[waste_class])

    else:
        time.sleep(1)

