import requests, time

def GetData(url, jsonData):
    r = requests.post(url, jsonData)
    return r.json()

def delay(milliseconds=500):
    count = int(milliseconds / 25)
    for i in range(count):
        time.sleep(0.025); i += 1