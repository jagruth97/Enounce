#       importing modules
import speech_recognition as sr                             
r = sr.Recognizer()             
from pydub import AudioSegment
from pydub.silence import split_on_silence
from PyPDF2 import PdfReader


import os
import shutil  #file manager

from gtts import gTTS

import tkinter as tk
from tkinter.filedialog import askopenfilename

#       sample audios

audio1 = "sample.mp3"   
audio2 = "audio1.wav"

#       converating non wav files to wavs

def make_wave(audio_file):
    
    req_audio = AudioSegment.from_mp3(audio_file)
    destiny = "sample.wav"

    if os.path.isfile(destiny):                         #willl auto replace file , this checking is for few extra lines of code
        os.remove(destiny)                              #destiny=filename
        req_audio.export(destiny, format = "wav")       #automatically save the file in the current folder
    else:
        req_audio.export(destiny, format = "wav")

#       audio to text 

def audio_to_text(file):
    audio = AudioSegment.from_wav(file)
    chunks = split_on_silence(audio_segment = audio, min_silence_len = 500, silence_thresh = audio.dBFS-14, keep_silence = 500)

    if os.path.isdir("temp"):                           #creating temp folder to store chunks and read them
        shutil.rmtree("temp")                           #checks if temp folder is present, if s then delete & create new for temp storage
        os.mkdir("temp")

    else:
        os.mkdir("temp")                                #if no file temp exists ,create new for storing chunks

    counter = 0
    req_text = ""
    for chunk in chunks:                                #reading data from chunks
        chunk_filename = os.path.join("temp", f"chunk{counter}.wav")            #path loc with file name
        counter+=1
        chunk.export(chunk_filename, format = "wav")

        with sr.AudioFile(chunk_filename) as source:
            audio_data = r.record(source)   
            try:
                text = r.recognize_google(audio_data)
            except:
                text = ""   #having errors like bg noise

            if not text == "":
                req_text += text + "\n"

    return req_text
        
#pdf to text 
def pdf_to_text(pdf_file):
    reader = PdfReader(pdf_file)
    length = len(reader.pages)
    text = ""

    for i in range(length):
        page = reader.pages[i]
        text += page.extract_text() + " " #extracting the words from pdf

    return text

#           text to audio
def text_to_audio(text):
    audio_file = gTTS(text = text, lang = "en", slow = False, tld = "co.in")
    destiny = "text_to_audio.mp3" #destiny=current directory

    if os.path.isfile(destiny):                         #willl auto replace file  this checking is for few extra lines of code
        os.remove(destiny)
        audio_file.save(destiny)
    else:
        audio_file.save(destiny)
 
#       main code

"""
text = audio_to_text(audio2)
os.system("cls")
print("\n" + text)
"""

#           gui functions
def back_to_home():
    lst = root.winfo_children() #children= all elemnts of gui like buttons,labels
    for widgets in lst:
        widgets.pack_forget() 
        
    audio_to_text_button.pack() #stacking all required functions when clicked
    text_to_audio_button.pack()

def browser_file():
    filename = askopenfilename(filetypes=(("All files","*.*"), ("tiff files","*.tiff")))
    return filename

def tk_audio_to_text():
    audio_to_text_button.pack_forget()
    text_to_audio_button.pack_forget()
    loading_label.pack()

    file = browser_file()
    extension = file.split(".")[-1]

    if extension == "mp3":
        make_wave(file)
    elif extension == "wav":
        shutil.copyfile(file, "sample.wav")
    else: 
        invalid_label.pack()
        home_button.pack()
        
    text = audio_to_text("sample.wav")

    with open("audio_to_text.txt", "w") as text_file:   #w=write
        text_file.write(text)
    
    location_label = tk.Label(root, text= f"Text file is stored at {os.getcwd()}\\audio_to_text.txt")
    loading_label.pack_forget()
    location_label.pack()
    home_button.pack()


def tk_text_to_audio():
    audio_to_text_button.pack_forget()
    text_to_audio_button.pack_forget()
    loading_label.pack()

    file = browser_file()
    extension = file.split(".")[-1]

    if extension == "txt":
        with open(file, "r") as data:
            text = data.read()

        text_to_audio(text)
        location_label = tk.Label(root, text= f"Text file is stored at {os.getcwd()}\\text_to_audio.mp3")  #cwd=current working directore
        loading_label.pack_forget()
        location_label.pack()
        home_button.pack()

    elif extension == "pdf":
        text = pdf_to_text(file)
        text_to_audio(text)
        location_label = tk.Label(root, text= f"Text file is stored at {os.getcwd()}\\text_to_audio.mp3")
        loading_label.pack_forget()
        location_label.pack()
        home_button.pack()
       


    else:
        loading_label.pack_forget()
        invalid_label.pack()
        home_button.pack()

    
#           python gui for the code

root = tk.Tk(className= "Enounce")  #root= main window-interface

root_width = 20
root_height = 10

audio_to_text_button = tk.Button(root, text = "Audio to Text",command= tk_audio_to_text, width = root_width, height = int(root_height/2), activebackground = "grey") #buttons size
text_to_audio_button = tk.Button(root, text = "Text to Audio", command = tk_text_to_audio, width = root_width, height = int(root_height/2), activebackground = "grey")
audio_to_text_button.pack()
text_to_audio_button.pack()
home_button = tk.Button(root, text="Go back",command = back_to_home, width = root_width, height = int(root_height/2), activebackground = "grey")

location_label = tk.Label(root, text= f"Text file is stored at {os.getcwd()}\\audio_to_text.txt") #writing here to make it global
invalid_label = tk.Label(root, text = "file format is invalid")
loading_label = tk.Label(root, text = "Loading please wait...") 

root.mainloop() #keep file running,until user terminates

