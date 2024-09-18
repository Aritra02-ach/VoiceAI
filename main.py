import speech_recognition as sr
import win32com.client
import webbrowser
import datetime
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyBnzQ2F7PWkWLqb4YDOYdz9XBHuob8OaYE"
genai.configure(api_key=GOOGLE_API_KEY)

speaker=win32com.client.Dispatch("SAPI.SpVoice")

def ai(prompt):
    generation_config = {
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 600,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel('gemini-1.0-pro-latest',
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    convo = model.start_chat()
    '''response=model.generate_content(input('Ask Gemini:'))
    response_text = response._result.candidates[0].content.parts[0].text'''

    while True:
        print('Ask Gemini:')
        user_input = takeCommand()
        print(user_input)
        if "stop" in user_input:
            break
        convo.send_message(user_input)
        print(convo.last.text)
        speaker.Speak(convo.last.text)


def say(text):
    speaker.speak(text)

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold=1
        audio=r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-IN")
            return query
        except Exception as e:
            return "Error!"

if __name__ =='__main__':
    while True:
        print("Listening...")
        text = takeCommand()
        sites=[["youtube","https://youtube.com"],["google","https://www.google.com"],
               ["wikipedia","https://www.wikipedia.com"],["firefox","https://firefox.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in text.lower():
                say(f"Opening {site[0]}")
                webbrowser.open(site[1])
                break;

        if "time" in text.lower():
            strftime=datetime.datetime.now().strftime(("%H:%M"))
            say(strftime)
            continue;

        if "Talk to AI".lower() in text.lower():
            ai(text)

        if "quit" in text.lower():
            break;



