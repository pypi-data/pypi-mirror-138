# -*- coding: utf-8 -*-

import pyttsx3



def speak(text):
    '''Example: for single recipient: 
            speak(""I am a robot who can speak the text you write.")
    '''
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()



    

