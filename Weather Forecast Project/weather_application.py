import os 
import tkinter as tk
import requests
import pytz
import datetime

class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title("Weather Application")

        # Set the background color for the root window
        master.config(bg="light blue")
        # Construct the relative path for the images directory
        images_dir = os.path.join(os.getcwd(), "images")
        
        try:
            # Load weather icon images
            self.cloud_img = tk.PhotoImage(file=os.path.join(images_dir, "cloud.png"))
            self.clear_img = tk.PhotoImage(file=os.path.join(images_dir, "clear.png"))
            self.rain_img = tk.PhotoImage(file=os.path.join(images_dir, "rain.png"))
            self.snow_img = tk.PhotoImage(file=os.path.join(images_dir, "snow.png"))
            self.thunderstorm_img = tk.PhotoImage(file=os.path.join(images_dir, "thunderstorm.png"))
            self.Haze_img = tk.PhotoImage(file=os.path.join(images_dir, "Haze.png"))
        except tk.TclError:
            print("Could not load one or more images.")
            self.master.destroy()
        
        # Create a frame to hold the result widgets
        self.result_frame = tk.Frame(master, bg="light blue")
        self.result_frame.grid(row=0, column=0, padx=50, pady=10)

        # Create a label to display the background image
        self.background_label = tk.Label(master, bg="light green", width=500, height=500)
        self.background_label.grid(row=1, column=0, sticky="nsew")
        self.master.rowconfigure(1, weight=1)
        self.master.columnconfigure(0, weight=1)

        # Create a label and an entry to enter the city name
        self.city_label = tk.Label(self.result_frame, text="Enter City Name:", font=("Times New Roman", 22), bg="light blue")
        self.city_label.grid(row=0, column=0, padx=10, pady=(30,0), sticky="w")
        self.city_entry = tk.Entry(self.result_frame, font=("Times New Roman", 18))
        self.city_entry.grid(row=1, column=0, padx=10, pady=(5,0), sticky="ew")
        self.result_frame.rowconfigure(1, weight=1)

        # Create a button to get weather data
        self.get_weather_button = tk.Button(self.result_frame, text="Get Weather", command=self.get_weather, font=("Times New Roman", 18))
        self.get_weather_button.grid(row=2, column=0, padx=10, pady=(5,0), sticky="ew")

        # Bind the <Enter> and <Leave> events to callback functions
        self.get_weather_button.bind("<Enter>", self.on_get_weather_enter)
        self.get_weather_button.bind("<Leave>", self.on_get_weather_leave)

        # Create a button to refresh the weather data
        self.refresh_button = tk.Button(self.result_frame, text="Refresh", command=self.get_weather, font=("Times New Roman", 18))
        self.refresh_button.grid(row=2, column=1, padx=10, pady=(5,0), sticky="ew")

        # Bind the <Enter> and <Leave> events to callback functions
        self.refresh_button.bind("<Enter>", self.on_refresh_enter)
        self.refresh_button.bind("<Leave>", self.on_refresh_leave)

        # Create a label to display the weather data
        self.result_label = tk.Label(self.result_frame, font=("Times New Roman", 16), bg="light blue")
        self.result_label.grid(row=3, column=0, padx=10, pady=(5,0), sticky="nsew")

        # Configure the layout of the result frame
        self.result_frame.columnconfigure(0, weight=1)
        self.result_frame.rowconfigure(3, weight=1)
        self.result_frame.bind("<Configure>", self.on_window_resize)
        
    def on_get_weather_enter(self, event):
        # Callback function for <Enter> event on Get Weather button
        self.get_weather_button.config(relief="sunken", bg="light green", font=("Times New Roman", 20))

    def on_get_weather_leave(self, event):
        # Callback function for <Leave> event on Get Weather button
        self.get_weather_button.config(relief="raised", bg="SystemButtonFace", font=("Times New Roman", 18))

    def on_refresh_enter(self, event):
        # Callback function for <Enter> event on Refresh button
        self.refresh_button.config(relief="sunken", bg="light green")

    def on_refresh_leave(self, event):
        # Callback function for <Leave> event on Refresh button
        self.refresh_button.config(relief="raised", bg="SystemButtonFace")

    def on_window_resize(self, event):
        # Update padding of result label based on the width of the result frame
        result_frame_width = self.result_frame.winfo_width()
        self.result_label.config(pady=result_frame_width/50)

    def change_background(self, weather_main):
        # Update the background label with an image corresponding to the current weather
        if weather_main == "Clouds":
            self.background_label.config(image=self.cloud_img)
        elif weather_main == "Clear":
            self.background_label.config(image=self.clear_img)
        elif weather_main == "Rain":
            self.background_label.config(image=self.rain_img)
        elif weather_main == "Snow":
            self.background_label.config(image=self.snow_img)
        elif weather_main == "Thunderstorm":
            self.background_label.config(image=self.thunderstorm_img)
        elif weather_main == "Haze":
            self.background_label.config(image=self.Haze_img)

    def get_weather(self):
        # Fetches and displays weather information for a given city
        city = self.city_entry.get()
        if not city:
            self.result_label.config(text="Please enter a city name.", font=("Times New Roman", 16))
            return
        
        # Validate city name format (e.g. no special characters)
        if not city.isalpha():
            self.result_label.config(text="City name should only contain alphabets.", font=("Times New Roman", 16))
            return

        api_key = '6a12a94be547ebc2fcb1f281d0f64d40'
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        # Clear the result label and create a refresh button
        self.result_label.config(text="")
        self.refresh_button = tk.Button(self.result_frame, text="Refresh", command=self.refresh_weather, font=("Times New Roman", 14))

        # Disable the get weather button and fetch weather data
        self.get_weather_button.config(state='disabled')
        
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.result_label.config(text=f"Could not get weather for {city}. Please check the city name and your internet connection.", font=("Times New Roman", 12))
        else:
            weather = response.json()

            if "message" in weather:
                self.result_label.config(text="City Not Found!", font=("Times New Roman", 12))
            elif "weather" not in weather or len(weather["weather"]) == 0:
                self.result_label.config(text="Weather data not available for this city.", font=("Times New Roman", 12))
            else:
                try:
                    # Parse weather data and update the UI  
                    weather_main = weather["weather"][0]["main"]
                    self.change_background(weather_main)
                    weather_description = weather["weather"][0]["description"]
                    temp = None
                    pressure = None
                    humidity = None
                    wind_speed = None
                    sunrise_time = None
                    sunset_time = None
                    time_offset = None
                    if "main" in weather and "temp" in weather["main"] and "humidity" in weather["main"]:
                        temp = weather["main"]["temp"] - 273.15
                        temp = round(temp, 2)
                        humidity = weather["main"]["humidity"]
                        pressure = weather["main"]["pressure"]
                    else:
                        raise KeyError("Temperature, Pressure or Humidity data not found in weather response.")
                    if "wind" in weather and "speed" in weather["wind"]:
                        wind_speed = weather["wind"]["speed"]
                    else:
                        raise KeyError("Wind speed data not found in weather response.")
                    if "sys" in weather and "sunrise" in weather["sys"] and "sunset" in weather["sys"] and "timezone" in weather:
                        sunrise_time = weather["sys"]["sunrise"]
                        sunset_time = weather["sys"]["sunset"]
                        time_offset = weather["timezone"]
                        tz = pytz.timezone("UTC")
                        sunrise_time = datetime.datetime.fromtimestamp(sunrise_time, tz)
                        sunrise_time = sunrise_time + datetime.timedelta(seconds=time_offset)
                        sunrise_time = sunrise_time.strftime("%H:%M:%S")
                        sunset_time = datetime.datetime.fromtimestamp(sunset_time, tz)
                        sunset_time = sunset_time + datetime.timedelta(seconds=time_offset)
                        sunset_time = sunset_time.strftime("%H:%M:%S")
                        current_time = datetime.datetime.now(tz)
                        current_time = current_time + datetime.timedelta(seconds=time_offset)
                        current_time = current_time.strftime("%H:%M:%S")
                    else:
                        raise KeyError("Sunrise, sunset, or timezone data not found in weather response.")

                    # Update result label with weather information
                    result_text = f"Weather: {weather_main}\nDescription: {weather_description}\nTemperature: {temp} °C\nPressure: {pressure} hPa\nHumidity: {humidity}%\nWind Speed: {wind_speed} m/s\nSunrise Time: {sunrise_time}\nSunset Time: {sunset_time}\nCurrent Time: {current_time}"
                    self.result_label.config(text=result_text, font=("Times New Roman", 18))
                except KeyError as e:
                    self.result_label.config(text=f"An error occurred while processing the weather data. Please try again later. Error: {str(e)}", font=("Times New Roman", 16))

            self.get_weather_button.config(state='normal')

    def refresh_weather(self):
        self.result_label.config(text="")
        self.get_weather()
        self.get_weather_button.config(state='normal')

root = tk.Tk()
weather_app = WeatherApp(root)
root.mainloop() # Run the GUI application
