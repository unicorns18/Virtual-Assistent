import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia

warnings.filterwarnings('ignore')

def recordAudio():

    # record the Audio
    r = sr.Recognizer()

    # Open the microphone & start recording
    with sr.Microphone() as source:
        print('Say something.')
        audio = r.listen(source)

    # Use Google's speech recognition
    data = ''
    try:
        data = r.recognize_google(audio)
        print('You said: ' + data)
    except sr.UnknownValueError: # Check for unknown error
        print('Google Speech Recognition could not understand, unknown error.')
    except sr.RequestError as e:
        print('Request Results from Google Speech Recognition service error ' + e)

    return data

# A function to get the Assistant's response
def assistantResponse(text):

    print(text)

    # Convert the text to speech
    myObj = gTTS(text=text, lang='en', slow=False)

    # Save the converted audio to a file. (MP3)

    myObj.save('assistant_response.mp3')

    # Play the converted file
    os.system('mpg321 assistant_response.mp3')

# A function for wake words for phrase
def wakeWord(text):
    WAKE_WORDS = ['hey siri', 'ok siri', 'hello test', 'hey test'] # A list of wake words, can be unlimited (why would you want unlimited words) lol

    text = text.lower() # Converting a text to all lower cases

    # Check to see if the users command OR text contains a wake word/phrase
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True

    # If the wake word isn't found in the text from the loop and so it returns False.
    return False

# A function to get us the current date
def getDate():

    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()] # e.g Tuesday
    monthNum = now.month
    dayNumber = now.day

    # A list of months
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                   'October', 'November', 'December']

    # A list of ordinal numbers
    ordinalNums = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th',
                   '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd',
                   '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']

    return 'The date today is ' + weekday + ' the ' + ordinalNums[dayNumber - 1] + '. '

# A function to return a random greeting response
def greet(text):

    # Greeting inputs
    GREETING_INPUT = ['hello', 'hi', 'bonjour', 'good day', 'howdy']

    # Greeting responses
    GREETING_RESPONSES = ['hello', 'hi', 'bonjour', 'good day', 'howdy', 'hey there']

    # If the user's input is a greeting then return a randomly chosen greeting response
    for word in text.split():
        if word.lower() in GREETING_INPUT:
            return random.choice(GREETING_RESPONSES) + '.'

    # If no greetings were detected then return an empty string
    return ''

# A function to get a person's first & last name from text
def getPerson(text):

    wordList = text.split() # Splitting the text into a list of words

    for i in range(0, len(wordList)):
        if i < 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i+1].lower() == 'is':
            return wordList[i + 2] + ' ' + wordList[i+3]

while True:

    # Record the audio
    text = recordAudio()
    response = ''

    # Checking for the wake word/phrase
    if(wakeWord(text) == True):

        # Check for greetings by the user
        response = response + greet(text)

        # Check to see if the user had anything to do with the date
        if('date' in text):
            get_date = getDate()
            response = response + ' ' + get_date

        if('time' in text):
            now = datetime.datetime.now()
            meridiem = ''
            if now.hour >= 12:
                meridiem = 'PM'
                hour = now.hour - 12
            else:
                meridiem = 'AM'
                hour = now.hour

            # Convince minute into a proper string
            if now.minute < 10:
                minute = '0'+str(now.minute)
            else:
                minute = str(now.minute)

            response = response + ' ' + 'It is ' + str(hour) + ':' + minute + ' ' + meridiem + '.'


        # Check to see if the user said 'who is'
        if('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences=2, chars=None, auto_suggest=None, redirect=False)
            response = response + ' ' + wiki

        # Have the assistant respond back using audio & text from response.
        assistantResponse(response)