import streamlit as st 
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
import tempfile
import os
import speech_recognition as sr
from transformers import pipeline


st.set_page_config(page_title='Simply! Translate', 
                   page_icon='🌍', 
                   layout='wide', 
                   initial_sidebar_state='expanded')
st.markdown("<h1 style='text-align: center; color: grey;'>Speech to Speech translation</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: grey;'>by Ayush Sahu </h5>", unsafe_allow_html=True)

st.markdown("""
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px;
        border-radius: 10px;
    }
    .stTextArea textarea {
        font-size: 16px;
    }
    .stSelectbox div {
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)


def text_to_speech(text, lang='en', c=0):
    tts = gTTS(text=text, lang=lang)
    audio_file = f"output{c}.mp3"
    tts.save(audio_file)
    return audio_file


def transcribe(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        file_path = tmpfile.name
        tmpfile.write(uploaded_file.read())

    c1.audio(uploaded_file, format="audio/wav")
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(file_path, format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        st.info("🔄 Transcribing... Please wait!")
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            st.success("✅ Transcription Complete!")
            c1.text_area("Transcribed Text:", text, height=100)
            return text
        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio.")
        except sr.RequestError:
            st.error("❌ API error. Check internet connection.")
    os.remove(file_path)
    return ""

Languages = {'afrikaans':'af','albanian':'sq','amharic':'am','arabic':'ar','armenian':'hy','azerbaijani':'az','basque':'eu','belarusian':'be','bengali':'bn','bosnian':'bs','bulgarian':'bg','catalan':'ca','cebuano':'ceb','chichewa':'ny','chinese (simplified)':'zh-cn','chinese (traditional)':'zh-tw','corsican':'co','croatian':'hr','czech':'cs','danish':'da','dutch':'nl','english':'en','esperanto':'eo','estonian':'et','filipino':'tl','finnish':'fi','french':'fr','frisian':'fy','galician':'gl','georgian':'ka','german':'de','greek':'el','gujarati':'gu','haitian creole':'ht','hausa':'ha','hawaiian':'haw','hebrew':'iw','hebrew':'he','hindi':'hi','hmong':'hmn','hungarian':'hu','icelandic':'is','igbo':'ig','indonesian':'id','irish':'ga','italian':'it','japanese':'ja','javanese':'jw','kannada':'kn','kazakh':'kk','khmer':'km','korean':'ko','kurdish (kurmanji)':'ku','kyrgyz':'ky','lao':'lo','latin':'la','latvian':'lv','lithuanian':'lt','luxembourgish':'lb','macedonian':'mk','malagasy':'mg','malay':'ms','malayalam':'ml','maltese':'mt','maori':'mi','marathi':'mr','mongolian':'mn','myanmar (burmese)':'my','nepali':'ne','norwegian':'no','odia':'or','pashto':'ps','persian':'fa','polish':'pl','portuguese':'pt','punjabi':'pa','romanian':'ro','russian':'ru','samoan':'sm','scots gaelic':'gd','serbian':'sr','sesotho':'st','shona':'sn','sindhi':'sd','sinhala':'si','slovak':'sk','slovenian':'sl','somali':'so','spanish':'es','sundanese':'su','swahili':'sw','swedish':'sv','tajik':'tg','tamil':'ta','telugu':'te','thai':'th','turkish':'tr','turkmen':'tk','ukrainian':'uk','urdu':'ur','uyghur':'ug','uzbek':'uz','vietnamese':'vi','welsh':'cy','xhosa':'xh','yiddish':'yi','yoruba':'yo','zulu':'zu'}
c1, c3 ,c2 = st.columns(3)
c3.text(" ")
inp = c1.selectbox('Choose Input Format', ("Text", "Audio_file","MIC"))
text = ""

if inp == "Text":
    text = c1.text_area("Enter Text:", help="Type your text here...")
elif inp == "MIC":
    uploaded_file = c1.audio_input("Record a Voice Message")
    if uploaded_file and c2.button('🎤 Transcribe Audio'):
        text = transcribe(uploaded_file)
else:
    uploaded_file = c1.file_uploader("Upload an Audio File", type=["mp3", "wav", "m4a"])
    if uploaded_file and c2.button('🎤 Transcribe Audio'):
        text = transcribe(uploaded_file)

option2 = c1.selectbox('Select Output Language', list(Languages.keys()))
value2 = Languages[option2]

if c2.button('🌎 Translate Text'):
    if inp != "Text":
        text = transcribe(uploaded_file)
    if text:
        translated_text = GoogleTranslator(target=value2).translate(text)
        c2.success("✅ Translation Completed!")
        c2.text_area("Translated Text:", translated_text, height=100)
    else:
        c2.warning("Please provide text or an audio file.")

if c2.button("🔊 Convert to Speech"):
    if inp != "Text":
        text = transcribe(uploaded_file)
    translated_text = GoogleTranslator(target=value2).translate(text)
    if translated_text.strip():
        audio_file = text_to_speech(translated_text, value2)
        c2.audio(audio_file, format='audio/mp3', autoplay=True)
        st.download_button(label="Download Audio",
                     data=audio_file,
                     file_name="output.mp3",
                     mime="audio/mp3")
    else:
        c2.warning("Please enter text before converting.")

if c2.button("🤔 Sentiment analysis"):
    if inp != "Text":
        text = transcribe(uploaded_file)
    if text !="" and text != " ":
        pipe = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")
        sentence = text
        result = pipe(sentence)[0] 

        sentiment = result['label']  

        if sentiment == "Very Negative":
            st.error('This is Very Negative', icon="🚨")
        elif sentiment == "Negative":
            st.error('This is Negative', icon="😭")
        elif sentiment == "Neutral":
            st.warning('This is Neutral', icon="😐")
        elif sentiment == "Positive":
            st.success('This is Positive', icon="😊")
        else: 
            st.success('This is Very Positive', icon="😃")
    else:
        st.warning("write something first")
