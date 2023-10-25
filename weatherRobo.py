import requests
import pyttsx3
import speech_recognition as sr
import tkinter as tk


def text_to_speech(text):
    speaker = pyttsx3.init()
    speaker.say(text)
    speaker.runAndWait()


def get_city_name_from_text():
    return city_entry.get()


def get_city_name_from_speech():
    text_to_speech("What is your city name?")
    recognizer_speech = sr.Recognizer()

    with sr.Microphone() as capture:
        result_label.config(text="listening...")
        result_label.update()
        audio = recognizer_speech.listen(capture, timeout=4, phrase_time_limit=2)

    try:
        city_name = recognizer_speech.recognize_google(audio)
        if city_name:
            city_entry.delete(0, tk.END)
            city_entry.insert(0, city_name)
        else:
            message = "No speech input detected."
            result_label.config(text=message)
            text_to_speech(message)

    except sr.WaitTimeoutError:
        message = "Speech input timed out. Please try again."
        result_label.config(text=message)
        text_to_speech(message)
    except sr.UnknownValueError:
        message = "Sorry, I couldn't understand your speech. Please enter the city name."
        result_label.config(text=message)
        text_to_speech(message)
    except Exception as e:
        message = f"An error occurred: {str(e)}"
        result_label.config(text=message)
        text_to_speech(message)


def fetch_weather():
    CITY_NAME = get_city_name_from_text()
    if (CITY_NAME):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            weather_description = data['weather'][0]['description']
            Celsius = round(float(temperature) - 273.15, 2)
            weather_info = f"Temperature in {CITY_NAME} is {Celsius} Celsius, and Humidity is: {humidity}%. Weather summary is {weather_description}"
            result_label.config(text=weather_info)
            root.update()
            if data['weather'][0]['main'] == "Rain":
                text_to_speech("It is raining. Bring an umbrella with you if you're going outside.")
            elif humidity <= 30:
                text_to_speech("Heat wave. Do not go outside unnecessarily.")
            else:
                text_to_speech("It is beautiful weather today. Enjoy your day.")
        else:
            result_label.config(text="Error fetching weather data")
    else:
        result_label.config(text="Input field is null")


def clear_output():
    city_entry.delete(0, tk.END)
    result_label.config(text="")


# Initialize Tkinter
root = tk.Tk()
root.title("Weather Information")
root.geometry("500x300")
# API Key and Widgets
API_KEY = "61a174b702c75cbba6972151d0093919"
city_label = tk.Label(root, text="Enter City Name:")
city_entry = tk.Entry(root)
get_weather_button = tk.Button(root, text="Get Weather", command=fetch_weather, bg="green", foreground="white")
speech_input_button = tk.Button(root, text="Speech Input", command=get_city_name_from_speech, bg="blue", foreground="white")
clear_output_button = tk.Button(root, text="Clear Entry", command=clear_output, bg="red", foreground="white")
result_label = tk.Label(root, text="")

# Set the row and column for each widget
city_label.grid(row=0, column=0, columnspan=3)
city_entry.grid(row=1, column=0, columnspan=4)
get_weather_button.grid(row=2, column=0, columnspan=1)
speech_input_button.grid(row=2, column=1, columnspan=1)
clear_output_button.grid(row=2, column=2, columnspan=1)
result_label.grid(row=3, column=0, columnspan=3)

# Add vertical padding between rows
root.rowconfigure(0, pad=10)
root.rowconfigure(1, pad=10)
root.rowconfigure(2, pad=10)
root.rowconfigure(3, pad=10)

# Center widgets in the middle
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

root.mainloop()
