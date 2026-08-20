# DSC 510
# Term Project
# Programming Term Project
# Author Seth Dice
# 8/12/2023

import requests  # Library to request data from webservice


def status_code_handler(response):
    """"Function used to handle status codes from URL and being used inside other functions"""
    # Print openweather error message for status code 400
    if response.status_code == 400:
        print("Mandatory fields missing, please check URL to ensure all fields are entered.")
    # Print openweather error message for status code 401
    elif response.status_code == 401:
        print("Unauthorized access, please check API key.")
    # Print openweather error message for status code 404
    elif response.status_code == 404:
        print("Latitude and longitude do not exist in database, please check location.")
    # Print openweather error message for status code 429
    elif response.status_code == 429:
        print("Too many requests received, please wait and try again or increase key quota.")
    # Print openweather error message for status code 5xx
    elif response.status_code == '5xx':
        print('Error with openweather, please contact site admins.')
    # No error message found, print generic error
    else:
        print('Unsuccessful, please review entered values.')


def units_conversion(user_units):
    """Function to convert weather units from user to be used by API"""
    while user_units.lower() not in ('imperial', 'metric', ''):
        user_units = input('Please provide units of measurement either Fahrenheit, Celsius, or Kelvin.\n')
        # Check user input and convert to value used by API
        if user_units.lower() == 'fahrenheit':
            # Change user_units to Fahrenheit used by API
            user_units = 'imperial'
        elif user_units.lower() == 'celsius':
            # Change user_units to Celsius used by API
            user_units = 'metric'
        elif user_units.lower() == 'kelvin':
            # Change user_units to Kelvin used by API
            user_units = ''
        else:
            # Keep asking until valid selection is made
            print('Please check spelling and try again.')
    return user_units


def zip_code_weather(user_zip, user_units, api_key):
    """Function that is run if user selects zip code"""
    # Store url address
    url_geo = (f"http://api.openweathermap.org/geo/1.0/zip?zip={user_zip},US&appid={api_key}")

    # Check to see if the zip code values is found in openweather geo coordinates; otherwise, print exception
    try:
        response = requests.get(url_geo)
        response.raise_for_status()
        print('Lat/Lon Connection Successful')
    except Exception:
        status_code_handler(response)

    # If zip code values found then get lat/lon for weather lookup
    data = response.json()
    lat = data.get('lat')
    lon = data.get('lon')

    # Weather url
    url_weather = (f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&"
                   f"units={user_units}")

    # Check to confirm lat/lon can retrieve weather and print if successful or not
    try:
        response_weather = requests.get(url_weather)
        response.raise_for_status()
        print('Weather Connection successful')
    except Exception:
        status_code_handler(response_weather)

    # If connection is made, then retrieve data and gather weather to print
    if response_weather.status_code == 200:
        data_weather = response_weather.json()

        # Location
        print('City is: ' + str(data_weather.get('name')))

        # Weather
        weather_list = data_weather['weather']
        for i in weather_list:
            print('Sky: ' + i['main'])
            print('Sky Description: ' + i['description'].title())

        # Get current temperature from the main key
        print('Temp is: ' + str(data_weather['main'].get('temp')))
        print('Feels like: ' + str(data_weather['main'].get('feels_like')))
        print('Temp Min: ' + str(data_weather['main'].get('temp_min')))
        print('Temp Max: ' + str(data_weather['main'].get('temp_max')))
        print('Pressure is: ' + str(data_weather['main'].get('pressure')))
        print('Humidity is: ' + str(data_weather['main'].get('humidity')))

    else:
        # Tell user that zip code search was unsuccessful before restarting program to allow reentry
        print('Zip code weather lookup unsuccessful, restarting...')


def city_state_weather(user_city, user_state, user_units, api_key):
    """Function that is run if user requests city"""
    # Store url address for city/state lookup
    url_geo = (f"http://api.openweathermap.org/geo/1.0/direct?q={user_city},{user_state},US&limit=5&appid={api_key}")

    # Get data from URL
    response = requests.get(url_geo)

    # If status code is 200, meaning connection made, then continue with weather program
    if response.status_code == 200:
        data = response.json()
        # Retrieve lat and lon values to get weather from location, or print exception to check spelling
        try:
            for key, value in data[0].items():
                if key == 'lat':
                    lat = value
                elif key == 'lon':
                    lon = value
            # Lat/Lon data was found for location
            print('Lat/Lon Connection Successful')
        except IndexError:
            status_code_handler(response)
            print('City/State not found, please check spelling')

    # Weather url and pass error due to error would be from spelling to continue program
    try:
        url_weather = (f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&"
                       f"units={user_units}")
    except NameError:
        pass

    # Try block to allow code to continue even if city/state was not found
    try:
        response_weather = requests.get(url_weather)
        print('Weather Connection successful')
    except NameError:
        pass

    # If status_code is 200 means connection successful and weather data retrieved
    try:
        if response_weather.status_code == 200:
            data_weather = response_weather.json()

            # Location
            print('City is: ' + str(data_weather.get('name')))

            # Weather
            weather_list = data_weather['weather']
            for i in weather_list:
                print('Sky: ' + i['main'])
                print('Sky Description: ' + i['description'].title())

            # Get current temperature from the main key
            print('Temp is: ' + str(data_weather['main'].get('temp')))
            print('Feels like: ' + str(data_weather['main'].get('feels_like')))
            print('Temp Min: ' + str(data_weather['main'].get('temp_min')))
            print('Temp Max: ' + str(data_weather['main'].get('temp_max')))
            print('Pressure is: ' + str(data_weather['main'].get('pressure')))
            print('Humidity is: ' + str(data_weather['main'].get('humidity')))

        else:
            # Tell user that city/state search was unsuccessful before restarting program to allow reentry
            print("City/State weather lookup unsuccessful, restarting...")

    except NameError:
        # Tell user that city/state search was unsuccessful before restarting program to allow reentry
        print('City/State weather lookup unsuccessful, restarting...')


def main():
    # Api key for weather lookup
    api_key = "a274ac2c5fb48cd271c51efad21a23eb"

    # Initial greeting
    print('Welcome to the weather lookup program using OpenWeather where you will be asked to lookup by '
          'zip code or city.')

    # Empty variable to initiate while loop asking for zip code or city
    user_req = ''
    while user_req.lower() != 'q()':
        # Prompt user to input either zip code or city, state
        user_req = input("For the weather lookup would you like to search by 'zip code', 'city' or type 'q()'"
                         "to exit?\n")

        # If user requests zip code check here
        if user_req.lower() == 'zip code':
            print('Zip code has been selected.')

            # While loop ensuring value is digit, or repeating
            while True:
                user_zip = input('Please provide 5-digit zip code.\n')
                try:
                    user_zip = int(user_zip)
                    break
                except ValueError:
                    print('This is not a number. Please enter a valid number.')

            # Empty user_units to convert the requested units from user
            user_units = ' '
            user_units = units_conversion(user_units)

            # Retrieve weather by zip code
            zip_code_weather(user_zip, user_units, api_key)

        # If user requests city check here
        elif user_req.lower() == 'city':
            print('City has been selected.')

            # City for weather lookup
            user_city = input('Please provide city.\n')

            # State for weather lookup
            user_state = input('Please provide state.\n')

            # Empty user_units to convert the requested units from user
            user_units = ' '
            user_units = units_conversion(user_units)

            # Retrieve weather by city and state
            city_state_weather(user_city, user_state, user_units, api_key)

        # Quit program if user requests
        elif user_req.lower() == 'q()':
            print('Thank you and have a nice day!')
            break

        # User doesn't input a valid option then say to try again
        else:
            print('Not a valid option, please try again.')


if __name__ == '__main__':
    main()
