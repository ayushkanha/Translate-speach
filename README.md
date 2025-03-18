# Speech-to-Speech Translation App

## Overview
The Speech-to-Speech Translation App is a Python-based application that translates spoken language into another language using advanced speech recognition and translation models. The application is built using Streamlit and can be hosted locally for easy accessibility.

## Features
- Converts speech from one language to another in real-time.
- Supports multiple languages for input and output.
- Uses **Google Speech Recognition API** for speech-to-text conversion.
- Translates text using **Google Translate API**.
- Converts translated text back into speech using **gTTS (Google Text-to-Speech)**.
- Provides a simple and interactive user interface built with **Streamlit**.
- Can be hosted locally to allow access over a network.

## Tech Stack
- **Python**
- **Streamlit** (for UI)
- **Google Speech Recognition API** (for audio input processing)
- **Google Translate API** (for translation)
- **gTTS** (for text-to-speech conversion)

## Installation
### Prerequisites
Ensure you have Python installed on your system. Install the required dependencies using:
```sh
pip install streamlit googletrans==4.0.0-rc1 SpeechRecognition gtts pydub
```

### Running the Application
To start the application, run:
```sh
streamlit run app.py
```
This will open the application in your default web browser.

## Usage
1. Select the input and output languages.
2. Press the **Record** button to speak into the microphone.
3. The app will recognize your speech and display the text.
4. The text will be translated into the selected target language.
5. The translated text will be converted back into speech and played aloud.

## Limitations
- Accuracy depends on the Google Speech Recognition API.
- Some languages may not have accurate text-to-speech conversion.
- Requires an internet connection for translation and speech recognition.

## Future Improvements
- Adding offline speech recognition using Vosk or DeepSpeech.
- Implementing a better text-to-speech engine with more natural voice output.
- Improving real-time performance.

## Contributing
Contributions are welcome! Feel free to fork the repository, make improvements, and submit a pull request.

## License
This project is licensed under the MIT License.

## Author
**Ayush Kumar Sahu**

---
For any queries or suggestions, feel free to reach out!

