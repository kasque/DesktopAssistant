import smtplib
from idlelib import browser
import speech_recognition as sr
from time import ctime
import webbrowser
import time
import os
import playsound
import random
from gtts import gTTS
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import wikipedia
import re
import urllib.request #used to make requests
import urllib.parse #used to parse values into the url
import pyaudio


r=sr.Recognizer() #initialising recogniser, responsible for recognising speech
def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            donna_speak(ask)

        audio = r.listen(source) #get what we say in microphone
        voice_data = r.recognize_google(audio) #capture the voice data
        print(voice_data) #prints what we say
        try:
            voice_data = r.recognize_google(audio)

        except sr.UnknownValueError:
             donna_speak('Sorry, I did not get that')
        except sr.RequestError:
            donna_speak('sorry,my speech service is down')
        return voice_data

def donna_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 1000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)




def respond(voice_data):
    if 'what is your name' in voice_data:
        donna_speak('My name is alexis')
    if 'what time is it' in voice_data:
        donna_speak(ctime())
    if 'search' in voice_data:
        search= record_audio('What do you want to search')

        url='https://www.google.com/search?q=' + search
        webbrowser.get().open(url)
        donna_speak('Here is what I found for '+search)
    if 'find location' in voice_data:
        location= record_audio('What is the location')
        url='https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        donna_speak('Here is the location of '+location)
    if "email" in voice_data:
        donna_speak("What is the subject?")
        time.sleep(3)
        subject = record_audio()
        donna_speak("What should I say?")
        message = record_audio()
        content = "Subject: {}\n\n{}".format(subject, message)
        # init gmail SMTP
        mail = smtplib.SMTP("smtp.gmail.com", 587)
        # identify to server
        mail.ehlo()
        # encrypt session
        mail.starttls()
        # login
        mail.login("18bcs1416.cse@gmail.com", "##########")
        # send message
        mail.sendmail("18bcs1416.cse@gmail.com", "cu.18bcs1416@gmail.com", content)
        # end mail connection
        mail.close()
        donna_speak("Email sent.")

    if "play on YouTube" in voice_data:
        donna_speak("Which music would you like me to play")
        text = record_audio()
        text = text.split(" ")
        search_5 = str(text[0:])
        record_audio("Hold on")
        webbrowser.open("https://www.youtube.com/results?search_query= " + search_5)
        browser.switch_to.frame( browser.find_element_by_xpath('//iframe[starts-with(@src, "https://www.youtube.com/embed")]'))
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Play"]'))).click()
    if "weather in" in voice_data:
        city = voice_data.split("in", 1)[1]
        #openweathermap API
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=a2c94ee8591fa32f0eedf0a32a7a03c1&units=metric'.format(city)
        response = requests.get(url)
        data = response.json()
        #print(data)
        if data["cod"] != "404":
            # store the value of "main"
            # key in variable y
            y = data["main"]

            # store the value corresponding
            # to the "temp" key of y
            current_temperature = y["temp"]
            donna_speak('It is {} degree celcius in {}'.format(current_temperature, city))
            time.sleep(3)
        else:
            donna_speak("city not found")



    if "play songs" in voice_data:
        songs_dir = "F:\Punjabi music"
        songs =os.listdir(songs_dir)
        os.startfile(os.path.join(songs_dir, songs[0]))

    if "Wikipedia" in voice_data:
        donna_speak("Searching")
        voice_data = voice_data.replace("wikipedia", "")
        result = wikipedia.summary(voice_data, sentences = 2)
        donna_speak(result)


    '''if "YouTube" in voice_data:
        donna_speak("What should i show")
        reg_ex = re.search("youtube (.+)", voice_data)
        if reg_ex:
            domain = voice_data.split("youtube", 1)[1]
            query_string = urllib.parse.urlencode({"search_query": domain})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            search_results = re.findall(r"href=\"\/watch\?v=(.{11})", html_content.read().decode())
            # print("http://www.youtube.com/watch?v=" + search_results[0])
            webbrowser.open("http://www.youtube.com/watch?v={}".format(search_results[0]) )
            pass'''
    if 'exit' in voice_data:
        exit()


time.sleep(1)
donna_speak('Hello Mam, How can I help you?')
while 1:
    voice_data=record_audio() #recording the audio and use it to pass to respond command
    respond(voice_data)