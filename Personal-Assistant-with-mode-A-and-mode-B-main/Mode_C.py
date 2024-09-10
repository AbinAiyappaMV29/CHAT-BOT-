import os
import smtplib
import speech_recognition as sr
import datetime
import os
import cv2
import random
from requests import get
import wikipedia
import webbrowser
import pywhatkit
import sys
import time
import pyjokes
import psutil
import speedtest
import bs4
from email.message import EmailMessage
import pyttsx3
import requests
from bs4 import BeautifulSoup

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices)-1].id)
engine.setProperty('rate', 175)

# Retrieve email credentials from environment variables
email_address = os.getenv('EMAIL_ADDRESS')
email_password = os.getenv('EMAIL_PASSWORD')

# Text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# Voice into text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("listening...")
        r.pause_threshold = 3
        audio = r.listen(source, timeout=7, phrase_time_limit=10)

    try:
        speak("recognizing...")
        query = r.recognize_google(audio, language='en-in')
        speak(f"user said: {query}")
    except Exception as e:
        speak("say that again please.....")
        return "none"
    return query

# To wish
def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour <= 12:
        speak("good morning")
    elif hour >= 12 and hour <= 18:
        speak("good afternoon")
    else:
        speak("good evening")
    speak("please tell me your request")

# To send email
def send_email(to, subject, body):
    msg = EmailMessage()
    msg['From'] = email_address
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(body)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

def get_news():
    # Send a GET request to the news website
    url = 'https://www.bbc.com/news/world'  # Replace with the URL of the news website you want to scrape
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the news headlines on the website
    news_headlines = soup.find_all('h3', class_='gs-c-promo-heading__title')  # Adjust the selector based on the structure of the website

    # Extract the text from the news headlines
    headlines = [headline.text for headline in news_headlines]

    return headlines

def get_temperature():
    api_key = "1fb89f80427f4b60a6d160647230406"  # Replace with your own API key
    base_url = "http://api.weatherapi.com/v1/current.json?"
    city = "Bangalore"  # Default city (you can change it to the user's location)
    complete_url = base_url + "key=" + api_key + "&q=" + city
    response = requests.get(complete_url)
    data = response.json()
    if "error" not in data:
        current_data = data["current"]
        temperature = current_data["temp_c"]
        return temperature
    else:
        return None

if __name__ == "__main__":
    wish()
    while True:
        if 1:
            query = takecommand().lower()

            # Logic building for tasks

            
            if "yourself" in query or "what can u do" in query:
                speak("i am zeno.v, a personal ai assistant, i am designed to make ur work easy by performing some simple tasks in this device")
            elif "how are you" in query:
                speak("i will always be fine to hear your commands")
            elif "play music" in query:
                music_dir = "C:\songs music"
                songs = os.listdir(music_dir)
                # rd=random.choice(songs)
                for song in songs:
                    if song.endswith('.mp3'):
                        os.startfile(os.path.join(music_dir, song))
            elif "wikipedia" in query:
                speak("searching wikipedia...")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak(results)
                print(results)
            elif "open google" in query:
                speak("sir, what should I search on google")
                cm = takecommand().lower()
                webbrowser.open(f"{cm}")
            elif "send message" in query:
                speak("to whom you want me to send a message")
                cm1 = takecommand().lower()
                pywhatkit.sendwhatmsg("+1234567890", "Hi", 9, 5)
            elif "play song on youtube" in query:
                cm = takecommand().lower()
                pywhatkit.playonyt(cm)
            elif "email" in query:
                try:
                    speak("what should I say?")
                    content = takecommand().lower()
                    to = "venumadathil72@gmail.com"
                    send_email(to, "Subject", content)
                    speak("email sent")
                except Exception as e:
                    print(e)
                    speak("sorry sir, I'm not able to send this email")
            elif "alarm" in query:
                speak("what time should I set the alarm for, tell like this 'set alarm to' and 'time'")
                tt = takecommand()
                tt = tt.replace("set alarm to ", "")
                tt = tt.replace(".", "")
                import Myalarm
                Myalarm.alarm(tt)
            elif "tell me a joke" in query:
                joke = pyjokes.get_joke()
                speak(joke)
            elif "shut down" in query:
                os.system("shutdown /s /t 5")
            elif "restart" in query:
                os.system("shutdown /r /t 5")
            elif "sleep man" in query:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            elif "where are we" in query:
                speak("wait sir, let me check")
                try:
                    ipAdd = get('https://api.ipify.org').text
                    print(ipAdd)
                    url = f'https://get.geojs.io/v1/ip/geo/{ipAdd}.json'
                    geo_request = get(url)
                    geo_data = geo_request.json()
                    city = geo_data['city']
                    speak(f"sir, I'm not sure, but I think we are in {city} city of {geo_data['country_name']}")
                except Exception as e:
                    speak("Sorry, I'm not able to find your location.")
                    pass
            elif "how much power left" in query or "how much power we have" in query or "battery" in query:
                battery = psutil.sensors_battery()
                percentage = battery.percent
                speak(f"sir our system has {percentage} percent battery")
                if percentage >= 75:
                    speak("we have enough power to continue work")
                elif percentage >= 40 and percentage < 75:
                    speak("we should connect our system to charging point to charge our battery")
                elif percentage < 40 and percentage > 15:
                    speak("we don't have much power to work, please connect charger")
                else:
                    speak("we have very low power, please connect charger or connect to a power source")
            
            elif "latest news" in query or "news headlines" in query:
                speak("Sure, fetching the latest news headlines.")
                news = get_news()
    
                if news:
                    speak("Here are some of the latest news headlines from BBC News:")
                    for i, headline in enumerate(news):
                        if i < 5:  # Adjust the number of headlines you want to read aloud
                            speak(headline)
                else:
                    speak("Sorry, I couldn't retrieve the latest news headlines.")
    
            elif "temperature" in query or "weather" in query:
                    temperature = get_temperature()
                    if temperature is not None:
                        speak(f"The current temperature is {temperature} degrees Celsius.")
                    else:
                        speak("Sorry, I couldn't retrieve the temperature at the moment.")
            elif "detect object" in query or "object detection" in query:
                text_speech= pyttsx3.init() 
                cap=cv2.VideoCapture(0)
                cap.set(3,640)
                cap.set(4,480)

                classNames= []
                classFile = "coco.names"
                with open(classFile,'rt') as f: 
                    classNames =f.read().rstrip('\n').split('\n')
                
                configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
                weightsPath = 'frozen_inference_graph.pb'
                
                net = cv2.dnn_DetectionModel(weightsPath,configPath)

                net.setInputSize (320,320)
                net.setInputScale(1.0/ 127.5) 
                net. setInputMean ((127.5, 127.5, 127.5))
                net.setInputSwapRB(True)

                while True:
                     success,img=cap.read()
                     classIds, confs, bbox = net.detect(img, confThreshold=0.5)
                     print(classIds, bbox)
     
                     if len(classIds) != 0:
                        for classId, confidence, box in zip(classIds.flatten(),confs.flatten(),bbox):
                            cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                            cv2.putText(img, classNames[classId-1].upper(), (box [0]+10,box[1]+30),
                                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255.0),2) 
                     cv2.imshow("output",img)
                     cv2.waitKey(40)
                     answer= classNames[classId-1]
                     newVoiceRate =80
                     text_speech.setProperty('rate',newVoiceRate)
                     text_speech.say(answer)
                     text_speech.runAndWait()

            elif "introduce yourself" in query:
                speak("I am zeno.v. Your personal AI Assistant. I am here to assist you with various tasks. How can I help you?")
            elif "goodbye" in query or "bye" in query or "stop" in query:
                speak("Goodbye!")
                sys.exit() 