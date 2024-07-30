# Some code was adjusted to test while the ISS was not overhead

import requests
from datetime import datetime
import smtplib
import time
import os

MY_LAT = 0 # Your latitude
MY_LNG = 0 # Your longitude
MY_POSITION = (MY_LAT, MY_LNG)

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

data = response.json()

longitude = float(data["iss_position"]["longitude"])
latitude = float(data["iss_position"]["latitude"])
iss_position = (float(longitude), float(latitude))


def check_if_iss_overheard(my_lat, iss_lat):
    if abs(my_lat - iss_lat) <= 5:
        return True


def check_if_night(time_hour, sunrise_hour, sunset_hour):
    if time_hour > sunset_hour or time_hour < sunrise_hour:
        return True

parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0
}

response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.utcnow().hour

for _ in range(10):
    if check_if_iss_overheard(MY_LAT, latitude) and check_if_night(time_now, sunrise, sunset):
        print("sending email")
    else:
        print("ISS not ready, try again later.")

        with smtplib.SMTP("smtp-mail.outlook.com", port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=EMAIL,
                msg="Subject:International Space Station\n\n"
                    "The ISS is currently above you, look up!"
            )
    time.sleep(30)
