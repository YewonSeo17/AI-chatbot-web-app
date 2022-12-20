from flask import Flask, render_template, request
import sys
import time
import pyttsx3
import AI_secretary

#create flask instance
app = Flask(__name__)

#show web
@app.route('/')
def render_page():
    return render_template('index.html')

from AI_secretary import res
@app.route('/output', methods=['GET', 'POST'])
def return_page():
    InputTxt = request.form['inputText']
    return render_template('result.html', output_Text = res)

app.run()