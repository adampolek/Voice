import speech_recognition as sr
from langdetect import detect
from tkinter import *
from playsound import *
from shutil import copyfile
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
from tkinter import filedialog
from scipy.fftpack import fft
from scipy.io import wavfile



class Viewer:

    def __init__(self, master):
        frame = Frame(master)
        frame.grid()

        self.speakButton = Button(frame, text='Press to speak!', command=self.recognizeSpeechAndLanguage)
        self.speakButton.grid(row=0, column=0, padx=10, pady=10)
        self.playSound = Button(frame, text="Play recorded sound", command= self.playRecordedSound)
        self.playSound.grid(row=0, column=1, padx=10, pady=10)
        self.saveSound = Button(frame, text= "save Sound", command= self.saveSoundToFile)
        self.saveSound.grid(row=0, column=2, padx=10, pady=10)
        self.chartButton = Button(frame, text="Create chart", command=self.createSoundChart)
        self.chartButton.grid(row=0, column=3, padx=10, pady=10)
        self.fftButton=Button(frame, text= "Create fft", command=self.createFft)
        self.fftButton.grid(row=0, column= 4, padx= 10, pady=10)
        self.loadButton = Button(frame, text= "Load sound from disk", command= self.loadSoundFromDisk)
        self.loadButton.grid(row=0, column= 5, padx= 10, pady=10)
        self.pathLabel = Entry(frame)
        self.pathLabel.grid(row=0, column=6, padx=10, pady=10)
        self.text= Label(frame, text="You said nothing yet")
        self.text.grid(row=1, column=1, padx=10, pady=10)
        self.language= Label(frame, text="Your language: ")
        self.language.grid(row=2, column=1, padx=10, pady=10)

    def recognizeSpeechAndLanguage(self):

        r = sr.Recognizer()
        print("Speak now!")

        with sr.Microphone() as source:
            audio = r.listen(source)

        self.changeLabels(yourText=audio,r=r)

    def changeLabels(self, yourText, r):

        try:
            text = r.recognize_google(yourText)
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
            wav_data = yourText.get_wav_data()
            file.write(wav_data)

    def playRecordedSound(self):

        playsound("/home/adam/Desktop/Voice/Voice/venv/Lib/recorded")

        r=sr.Recognizer()
        with sr.WavFile("/home/adam/Desktop/Voice/Voice/venv/Lib/recorded") as source:
            audio = r.listen(source)

        self.changeLabels(yourText=audio, r=r)

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
        plt.close('all')
        plt.figure(1)
        plt.plot(signal)
        plt.savefig("/home/adam/Desktop/Voice/Voice/plot.png")
        image = PhotoImage(file="/home/adam/Desktop/Voice/Voice/plot.png")
        imageGUI = Toplevel()
        imageLabel = Label(imageGUI, image=image)
        imageLabel.pack()
        imageGUI.mainloop()

    def loadSoundFromDisk(self):

        fl = filedialog.askopenfilename(initialdir= "/home/adam/Desktop/Voice/Voice", title="Load sound")
        playsound(fl)
        r = sr.Recognizer()
        with sr.WavFile(fl) as source:
            audio = r.listen(source)

        self.changeLabels(yourText=audio, r=r)

    def createFft(self):
        plt.close('all')
        rate, data = wavfile.read("/home/adam/Desktop/Voice/Voice/venv/Lib/recorded")
        fft_out = fft(data)
        plt.figure(2)
        plt.plot(data, np.abs(fft_out))
        plt.savefig("/home/adam/Desktop/Voice/Voice/plot1.png")
        image = PhotoImage(file="/home/adam/Desktop/Voice/Voice/plot1.png")
        imageGUI2 = Toplevel()
        imageLabel2 = Label(imageGUI2, image=image)
        imageLabel2.pack()
        imageGUI2.mainloop()