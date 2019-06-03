import speech_recognition as sr
from langdetect import detect
from tkinter import *
from playsound import *
from shutil import copyfile
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys


class Viewer:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.speakButton = Button(frame, text="Press to speak!", command=self.recognizeSpeechAndLanguage)
        self.speakButton.pack(side=LEFT)
        self.playSound = Button(frame, text="Play recorded sound", command= self.playRecordedSound)
        self.playSound.pack(side=LEFT)
        self.saveSound = Button(frame, text= "save Sound", command= self.saveSoundToFile)
        self.saveSound.pack(side=LEFT)
        self.chartButton = Button(frame, text="Create chart", command=self.createSoundChart)
        self.chartButton.pack(side=LEFT)
        self.pathLabel = Text(frame)
        self.pathLabel.pack(side=BOTTOM)
        self.text= Label(frame, text="You said nothing yet")
        self.text.pack(side=BOTTOM)
        self.language= Label(frame, text="Your language: ")
        self.language.pack(side=BOTTOM)

    def recognizeSpeechAndLanguage(self):

        r = sr.Recognizer()
        print("Speak now!")

        with sr.Microphone() as source:
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            self.text['text']= "You said: "+format(text)
            if detect(text) == 'en':
                self.language['text']="Your language: English"
            elif detect(text) == 'de':
                self.language['text'] = "Your language: German"
            else:
                self.language['text'] = "Your language: Cannot recognize your language"
        except sr.UnknownValueError:
            self.text['text'] = "You said: Cannot recognize what you said"

        with open('recorded', 'wb') as file:
            wav_data = audio.get_wav_data()
            file.write(wav_data)

    def playRecordedSound(self):

        playsound("/home/adam/Desktop/Voice/Voice/venv/Lib/recorded")

    def saveSoundToFile(self):

        path = self.pathLabel.get("1.0", END)
        copyfile("/home/adam/Desktop/Voice/Voice/venv/Lib/recorded", "/home/adam/Desktop/Voice/Voice/"+path)

    def createSoundChart(self):

        spf=wave.open("/home/adam/Desktop/Voice/Voice/venv/Lib/recorded", 'r')
        signal = spf.readframes(-1)
        signal = np.fromstring(signal, 'Int16')

        if spf.getnchannels() == 2:
            print("Just mono files")
            sys.exit()

        plt.figure(1)
        plt.title('Signal wave chart')
        plt.plot(signal)
        plt.savefig("/home/adam/Desktop/Voice/Voice/plot.png")
        image = PhotoImage(file="/home/adam/Desktop/Voice/Voice/plot.png")
        imageGUI = Toplevel()
        imageLabel = Label(imageGUI, image=image)
        imageLabel.pack()
        imageGUI.mainloop()