import speech_recognition as sr
from langdetect import detect

r = sr.Recognizer()
print("Speak now!")

# with sr.WavFile("F:\\PyCharmProjects\\Voice\\test4.wav") as source:
#     audio = r.listen(source)

with sr.Microphone() as source:
    audio = r.listen(source)

try:
    text = r.recognize_google(audio)
    print("You said: {}".format(text))
    if detect(text) == 'en':
        print(" in: English")
    if detect(text) == 'de':
        print(" in: German")
except sr.UnknownValueError:
    print("Cannot recognize what you said")
