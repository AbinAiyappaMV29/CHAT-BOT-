import pyttsx3
import speech_recognition as sr
import subprocess

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice' , voices[len(voices)-1].id)

#text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()
    
# Function to recognize voice input
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand your voice.")
        except sr.RequestError as e:
            print("Sorry, I encountered an error while processing your request. Error:", str(e))
    return None

# Main function
def main():
    # Prompt user to choose between two files
    speak("Choose between 'mode a' and 'mode b'")
    choice = None
    while choice not in ['normal', 'blind']:
        choice = recognize_speech()
        
    # Execute the chosen file
    if choice == 'normal':
        file_path = 'Mode_A.py'  # Replace with the actual file path for 'made.py'
    elif choice == 'blind':
        file_path = 'Mode_C.py'  # Replace with the actual file path for 'mode.py'
    
    try:
        subprocess.run(['python', file_path])
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except Exception as e:
        print("An error occurred while executing the file. Error:", str(e))

if __name__ == "__main__":
    main()

