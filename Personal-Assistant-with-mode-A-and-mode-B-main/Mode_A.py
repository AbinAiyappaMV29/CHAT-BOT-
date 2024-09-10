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
        print("listening...")
        r.pause_threshold = 3
        audio = r.listen(source, timeout=7, phrase_time_limit=10)

    try:
        print("recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
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

if __name__ == "__main__":
    wish()
    while True:
        if 1:
            query = takecommand().lower()

            # Logic building for tasks

            if "open notepad" in query:
                npath = "C:\\Windows\\SysWOW64\\notepad.exe"
                os.startfile(npath)
            elif "close notepad" in query:
                speak("ok sir closing")
                os.system("taskkill /f /im notepad.exe")
            elif "yourself" in query or "what can u do" in query:
                speak("i am zeno.v, a personal ai assistant, i am designed to make ur work easy by performing some simple tasks in this device")
            elif "how are you" in query:
                speak("i will always be fine to hear your commands")
            elif "open command prompt" in query:
                os.system("start cmd")
            elif "close command prompt" in query:
                speak("ok sir closing")
                os.system("taskkill /f /im cmd.exe")
            elif "open camera" in query:
                cap = cv2.VideoCapture(1)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()
            elif "play music" in query:
                music_dir = "C:\songs music"
                songs = os.listdir(music_dir)
                # rd=random.choice(songs)
                for song in songs:
                    if song.endswith('.mp3'):
                        os.startfile(os.path.join(music_dir, song))
            elif "ip address" in query:
                ip = get('https://api.ipify.org').text
                speak(f"your IP address is {ip}")
            elif "wikipedia" in query:
                speak("searching wikipedia...")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak(results)
                print(results)
            elif "open youtube" in query:
                webbrowser.open("www.youtube.com")
            elif "open instagram" in query:
                webbrowser.open("www.instagram.com")
            elif "open stackoverflow" in query:
                webbrowser.open("www.stackoverflow.com")
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

            elif "introduce yourself" in query:
                speak(
                    "I am zeno.v. Your personal AI Assistant. I am here to assist you with various tasks. How can I help you?")
            elif "goodbye" in query or "bye" in query or "stop" in query:
                speak("Goodbye!")
                sys.exit()