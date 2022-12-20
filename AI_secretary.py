import os
import sys
import time
import openai
openai.api_key = "REDACTED"

#브라우저
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

Chrome_options = Options()
Chrome_options.add_experimental_option("detach", True)



#내레이터
import pyttsx3
voice_id_Hazel = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0"
voice_id_David = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
voice_id_Zira = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
converter = pyttsx3.init()
converter.setProperty('voice', voice_id_David)
converter.setProperty('rate', 180)
converter.setProperty('volume', 1.0)

#시간정보
import datetime

#날씨정보
import requests, json
api_key = "3d6e2a14c4979bec99839f4ee58fe542"
base_url = "https://api.openweathermap.org/data/2.5/weather?"
city_name = 'Yongin, KR'
complete_url = base_url + "appid=" + api_key + "&q=" + city_name

#시간
def action_time():
        return datetime.datetime.now().time().strftime('%H:%M')

#날씨
def action_weather():
        response = requests.get(complete_url)
        x=response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            return "\n In " + city_name + ", there will be " + str(weather_description) + ", \n Temperature is " + str(round(float(current_temperature) - 273.15, 3)) + " degrees Celsius,\n atmospheric pressure is " + str(current_pressure) + " hecto pascal, \n and humidity is " + str(current_humidity) + " percent." 
        else:
            return " City is Not Found, please contact manager."


os.system('cls')
print("------------starting up Personal AI Secretary Service--------------")

#인터넷 검색
def search_web(input):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=Chrome_options)
    driver.implicitly_wait(1)
    driver.maximize_window()

    if any(i in input.lower() for i in ['youtube', 'music', 'song', 'play', 'listen']):
        query = identify_song(input)

        if 'no singer' in query:
            query.replace('no singer speciified', '')

        driver.get("http://www.youtube.com/results?search_query="+query)
        l=driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div[2]/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a")
        l.click()
        return query

    elif any(i in input.lower() for i in ['search', 'wiki', 'wikipedia', 'google', 'internet']):
        query = identify_searchword(input)
        driver.get("http://en.wikipedia.org/wiki/"+ query)
        return query


def identify_song(input):
    response = openai.Completion.create(
        model = 'text-davinci-003',
        prompt = """
            Identify the Title and the Singer of the song in a given sentence.

            Sentence: play some carol on youtube
            Title and Singer: carol
            Sentence: play stronger by Kanye west
            Title and Singer: Stronger, Kanye West
            Sentence: Can you play Godzilla by Eminem?
            Title and Singer: Godzilla, Eminem
            Sentence: I want to listen to viva la vida by coldplay
            Title and Singer: Viva La Vida, Coldplay
            Sentence: """ + input + """
            Title and Singer: """,
            temperature = 0.9,
            max_tokens=500
    )
    response = response.choices[0].text.replace("\n", "").lstrip()
    return response

def identify_searchword(input):
    response = openai.Completion.create(
        model = 'text-davinci-003',
        prompt = """
            Identify the keyword in given query.

            Query: Search kanye west?
            Keyword: Kanye West
            Query: Google richard feynman?
            Keyword: Richard feynman
            Query: Wikipedia were atomic bombs exploded during world war 2?
            Keyword: World War 2, atomic bombs
            Query: Search Christopher Colombus
            Keyword: Cristopher Columbus
            Query: """ + input + """
            Keyword: """,
            temperature = 0.9,
            max_tokens=500
    )
    response = response.choices[0].text.replace("\n", "").lstrip()
    return response

#입력값 확인
from flask_test import InputTxt  #html form에서 받은 string 가져옴
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

while True:
    res = chat()
    if len(res) > 30:
        print("AI --> " + res)
        converter.say(str(res))
        converter.runAndWait()
    else:
        print("AI --> speaking...")
        converter.say(str(res))
        converter.runAndWait()
        sys.stdout.write("\033[F")
        time.sleep(1)
        sys.stdout.write("\033[K")
        print("AI --> " + res)