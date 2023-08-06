import requests, time

def GetData(url, jsonData):
    r = requests.post(url, jsonData)
    while True:
        if 200 <= r.status_code <= 226:
            return "OK", r.json(), r.status_code
        else:
            break
    return "Fail", None, r.status_code



def delay(milliseconds=500):
    count = int(milliseconds / 25)
    for i in range(count):
        time.sleep(0.025); i += 1