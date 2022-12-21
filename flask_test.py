from flask import Flask, render_template, request
import AI_secretary
from AI_secretary import *
import pyttsx3

voice_id_Hazel = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0"
voice_id_David = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
voice_id_Zira = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
converter = pyttsx3.init()
converter.setProperty('voice', voice_id_David)
converter.setProperty('rate', 180)
converter.setProperty('volume', 1.0)

#create flask instance
app = Flask(__name__)

#show web
@app.route('/')
def render_page():
    return render_template('index.html')

toPassElement = []

def chat():
    text = InputTxt
    if "time" in text:
        response = "It is " + action_time() + "."
    elif any(i in text for i in ['weather', 'Weather', 'WEather']):
        response = action_weather()
    elif any(i in text.lower() for i in ['search', 'play', 'music', 'watch', 'youtube', 'song', 'internet', 'chrome', 'listen']):
        response = 'searching ' + search_web(text)
    else:
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt = """
            The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.
            The completion can’t go to a new line.
            The completion can’t change the speaker.
            The completion won’t allow the speaker to speak twice in a row

            Human: Hello, who are you?
            AI: I am your humble AI servant created by HAFS Artifical Intelligence Research Club.
            AI: How can I help you?
            Human: """ + text + """
            AI: """,
            temperature = 0.9,
            max_tokens=500
        )
        response = response.choices[0].text.replace("\n", "").lstrip()
    return response

@app.route('/output', methods=['GET', 'POST'])
def return_page():
    global InputTxt
    InputTxt = request.form['inputText']

    res = chat()
    myLine = "me --> " + InputTxt
    aiLine = "AI --> " + res
    toPassElement.append(myLine)
    toPassElement.append(aiLine)

    if(InputTxt == "cls"):
        toPassElement.clear()
        res = ""

    # converter.say(str(res))
    # converter.runAndWait()

    return render_template('result.html', toPass = toPassElement)

app.run(debug=True)