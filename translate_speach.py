import streamlit as st 
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
import tempfile
import os
import speech_recognition as sr


def text_to_speech(text, lang='en',c=0):
    tts = gTTS(text=text, lang=lang)

    tts.save(f"output{c}.mp3")
    return f"output{c}.mp3"


def transcribe(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                file_path = tmpfile.name
                tmpfile.write(uploaded_file.read())

    c1.audio(uploaded_file, format="audio/wav")

    # Convert to WAV (Google API requires WAV)
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(file_path, format="wav")

    # Recognize speech
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        st.write("🔄 Transcribing... Please wait!")
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

    # Clean up temp file
    os.remove(file_path)
    return "error"

# """------------------------------------------------------------------------------------------------------------"""

Languages = {'afrikaans':'af','albanian':'sq','amharic':'am','arabic':'ar','armenian':'hy','azerbaijani':'az','basque':'eu','belarusian':'be','bengali':'bn','bosnian':'bs','bulgarian':'bg','catalan':'ca','cebuano':'ceb','chichewa':'ny','chinese (simplified)':'zh-cn','chinese (traditional)':'zh-tw','corsican':'co','croatian':'hr','czech':'cs','danish':'da','dutch':'nl','english':'en','esperanto':'eo','estonian':'et','filipino':'tl','finnish':'fi','french':'fr','frisian':'fy','galician':'gl','georgian':'ka','german':'de','greek':'el','gujarati':'gu','haitian creole':'ht','hausa':'ha','hawaiian':'haw','hebrew':'iw','hebrew':'he','hindi':'hi','hmong':'hmn','hungarian':'hu','icelandic':'is','igbo':'ig','indonesian':'id','irish':'ga','italian':'it','japanese':'ja','javanese':'jw','kannada':'kn','kazakh':'kk','khmer':'km','korean':'ko','kurdish (kurmanji)':'ku','kyrgyz':'ky','lao':'lo','latin':'la','latvian':'lv','lithuanian':'lt','luxembourgish':'lb','macedonian':'mk','malagasy':'mg','malay':'ms','malayalam':'ml','maltese':'mt','maori':'mi','marathi':'mr','mongolian':'mn','myanmar (burmese)':'my','nepali':'ne','norwegian':'no','odia':'or','pashto':'ps','persian':'fa','polish':'pl','portuguese':'pt','punjabi':'pa','romanian':'ro','russian':'ru','samoan':'sm','scots gaelic':'gd','serbian':'sr','sesotho':'st','shona':'sn','sindhi':'sd','sinhala':'si','slovak':'sk','slovenian':'sl','somali':'so','spanish':'es','sundanese':'su','swahili':'sw','swedish':'sv','tajik':'tg','tamil':'ta','telugu':'te','thai':'th','turkish':'tr','turkmen':'tk','ukrainian':'uk','urdu':'ur','uyghur':'ug','uzbek':'uz','vietnamese':'vi','welsh':'cy','xhosa':'xh','yiddish':'yi','yoruba':'yo','zulu':'zu'}

text=""
st.set_page_config(page_title='Simply! Translate', 
                   page_icon='translator-icon.png', 
                   layout='wide', 
                   initial_sidebar_state='expanded')
c1,c2=st.columns(2)

inp=c1.selectbox('Input format',("text","audio"))
if(inp=="text"):
    text = c1.text_area("Enter text:",help="Enter your text here")
else:
    uploaded_file = c1.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])
    if uploaded_file is not None:
        # Save uploaded file temporarily
        if c1.button('transcibe'):
            text=transcribe(uploaded_file)
    

option2 = c1.selectbox('Output language',
                       ('afrikaans', 'albanian', 'amharic', 'arabic', 'armenian', 'azerbaijani', 'basque', 'belarusian', 'bengali', 'bosnian', 'bulgarian', 'catalan', 'cebuano', 'chichewa', 'chinese (simplified)', 'chinese (traditional)', 'corsican', 'croatian', 'czech', 'danish', 'dutch', 'english', 'esperanto', 'estonian', 'filipino', 'finnish', 'french', 'frisian', 'galician', 'georgian', 'german', 'greek', 'gujarati', 'haitian creole', 'hausa', 'hawaiian', 'hebrew', 'hindi', 'hmong', 'hungarian', 'icelandic', 'igbo', 'indonesian', 'irish', 'italian', 'japanese', 'javanese', 'kannada', 'kazakh', 'khmer', 'korean', 'kurdish (kurmanji)', 'kyrgyz', 'lao', 'latin', 'latvian', 'lithuanian', 'luxembourgish', 'macedonian', 'malagasy', 'malay', 'maltese', 'maori', 'marathi', 'mongolian', 'myanmar (burmese)', 'nepali', 'norwegian', 'odia', 'pashto', 'persian', 'polish', 'portuguese', 'punjabi', 'romanian', 'russian', 'samoan', 'scots gaelic', 'serbian', 'sesotho', 'shona', 'sindhi', 'sinhala', 'slovak', 'slovenian', 'somali', 'spanish', 'sundanese', 'swahili', 'swedish', 'tajik', 'tamil', 'telugu', 'thai', 'turkish', 'turkmen', 'ukrainian', 'urdu', 'uyghur', 'uzbek', 'vietnamese', 'welsh', 'xhosa', 'yiddish', 'yoruba', 'zulu'))


value2 = Languages[option2]



if c2.button('Translate Sentence'):
    text=transcribe(uploaded_file)
    translated_text =GoogleTranslator(target=value2).translate(text)
    c2.title("translated text:")
    c2.write(translated_text)
    c2.success("Translation is **successfully** completed!")
    


c=0
    
if c2.button("Convert to Speech"):
    c2.title("🔊 Text-to-Speech Converter")
    text=transcribe(uploaded_file)
    translated_text =GoogleTranslator(target=value2).translate(text)
    if translated_text.strip():
        
        audio_file = text_to_speech(translated_text, value2,c)
        c+=1
        c2.audio(audio_file, format='audio/mp3',autoplay=True)
        
    else:
        c2.warning("Please enter some text before converting.")



        
