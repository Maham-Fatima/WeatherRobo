import requests
import json
import pyttsx3
import speech_recognition as r

if __name__ == '__main__':

    API_KEY = "your API key"
    speaker = pyttsx3.init()  # initialize
    speaker.say("What is your city name")  # text to speak
    speaker.runAndWait()  # speak
    model_path = r"C:\Users\lenovo\PycharmProjects\pythonProject1\venv\Lib\site-packages\vosk\vosk-model-small-en-us-0.15"
    recognizer_speech = r.Recognizer()

    with r.Microphone() as capture:  # Capture audio
        print("Listening for audio...")
        audio = recognizer_speech.listen(capture, 3)  # Listen audio from microphone and store in audio
        print("Audio captured successfully")

    try:
        text = recognizer_speech.recognize_google(audio)
        print(text)
    except:
        message = "Sorry, I couldn't understand your speech, I will use default values."
        print(message)
        speaker.say(message)
        speaker.runAndWait()
        text = 'Karachi'

    CITY_NAME = text
    # Example city name
    print(f"City name is {CITY_NAME=}")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        weather_description = data['weather'][0]['description']
        Celsius = round(float(temperature) - 273.15, 2)
        speaker.say(
            f"Temperature in {CITY_NAME} is {Celsius}Celsius, and Humidity is: {humidity}%. Weather summary is {weather_description}")
        speaker.runAndWait()
        if data['weather'][0]['main'] == "rain":
            speaker.say("It is raining Bring umbrella with you, outside")
        elif humidity <= 30:
            speaker.say("Heat wave. Do not go unnecessarily, outside")
        else:
            speaker.say("It is beautiful weather today. Enjoy your day")
        speaker.runAndWait()
        print(f"Temperature: {temperature}K {Celsius}C")
        print(f"Humidity: {humidity}%")
        print(f"Weather: {weather_description}")
        print(data)# complete data
    else:
        print("Error fetching weather data")
