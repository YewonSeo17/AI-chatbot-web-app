from flask import Flask, render_template, request
import AI_secretary
from AI_secretary import *

#create flask instance
app = Flask(__name__)

#show web
@app.route('/')
def render_page():
    return render_template('index.html')

toPassElement = []

@app.route('/output', methods=['GET', 'POST'])
def return_page():
    InputTxt = request.form['inputText']

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

    res = chat()
    myLine = "me --> " + InputTxt
    aiLine = "AI --> " + res
    toPassElement.append(myLine)
    toPassElement.append(aiLine)

    if(InputTxt == "cls"):
        toPassElement.clear()

    return render_template('result.html', toPass = toPassElement)

app.run(debug=True)