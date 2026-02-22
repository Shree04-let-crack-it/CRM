import speech_recognition as sr
import streamlit as st

def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except:
        return "Speech not recognized"
