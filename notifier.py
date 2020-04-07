from twilio.rest import Client

import requests
import datetime
import pause
import time

import json

SID = "Your Twilio account SID"
TOK = "Your Twilio auth token"

CLI = Client(SID, TOK)

TWNUM = "Your Twilio phone number"

MYNUM = "Your personal phone number"

dd = {
    "1": 31,
    "2": 27,
    "3": 31,
    "4": 30,
    "5": 31,
    "6": 30,
    "7": 31,
    "8": 31,
    "9": 30,
    "10": 31,
    "11": 30,
    "12": 31
}

# API endpoint
URL = "https://corona.lmao.ninja/countries/your_country_goes_here"


def move_day(date, dx):
    date["day"] = date["day"] + dx

    if date["day"] > dd[str(date["month"])]:
        date["day"] = 1
        date["month"] = date["month"] + 1

        if date["month"] > 12:
            date["year"] = date["year"] + 1
            date["month"] = 1

    elif date["day"] == 0:
        date["month"] = date["month"] - 1

        if date["month"] == 0:
            date["year"] = date["year"] - 1
            date["month"] = 12

        date["day"] = dd[str(date["month"])]


def write_to_file(filename, data):
    datas = json.dumps(data)

    with open(filename, "w") as f:
        print(datas, file=f)


def read_from_file(filename):
    data = {}
    with open(filename, "r") as f:
        data = f.read()
        data = json.loads(data)

    return data


def send_msg(data, juce):
    msg = f"\nNewly infected {data['todayCases']}\n"
    msg += f"Total {data['active']}/{data['cases']} ({data['recovered']} izlecenih)\n"

    death_perc = data['deaths'] / data['cases'] * 100

    msg += f"Deaths {data['deaths']} ({death_perc:.2f}%)\n\n"

    vsjuc = (data['todayCases'] - juce['todayCases']) / juce['todayCases'] * 100

    if vsjuc > 0:
        msg += f"vs yesterday: +{vsjuc:.2f}%"
    else:
        msg += f"vs yesterday: {vsjuc:.2f}%"

    CLI.messages.create(body=msg, from_=TWNUM, to=MYNUM)


if __name__ == "__main__": 
    while True:
        vr = datetime.datetime.now()

        pause.until(datetime.datetime(vr.year, vr.month, vr.day, 15))

        juce = read_from_file("juce.txt")

        while True:
            novo = requests.get(url=URL)
            novi = novo.json()

            if novi["tests"] != juce["tests"]:
                break

            time.sleep(60 * 15)
        
        send_msg(novi, juce)

        write_to_file("juce.txt", novi)

        sl = {"year": vr.year, "month": vr.month, "day": vr.day}
        move_day(sl, 1)

        print("w8ing until", sl)

        pause.until(datetime.datetime(sl["year"], sl["month"], sl["day"], 15))

