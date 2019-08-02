import requests
import json
import datetime
import time

try:
    def wait():
        r = requests.get('http://api-kraken.tisseo.fr/v1/stops_schedules.json?stopAreaId=stop_area:SA_731&number=15&timetableByArea=1&key=t0b6442937d70d40d1a81d28cd3c94791&lang=fr')
        for index, i in enumerate(json.loads(r.text)["departures"]["stopAreas"][0]["schedules"][3]["journeys"]):
            if index == 0:
                thms = i["waiting_time"].split(":")
                ts = (int(thms[0]) * 3600 + int(thms[1]) * 60 + int(thms[2])) - 60
        if ts > 0:
            time.sleep(ts)

    def late(dr, svnb):
        r = requests.get('http://api-kraken.tisseo.fr/v1/stops_schedules.json?stopAreaId=stop_area:SA_731&number=15&timetableByArea=1&key=t0b6442937d70d40d1a81d28cd3c94791&lang=fr')
        da = []
        for index, i in enumerate(json.loads(r.text)["departures"]["stopAreas"][0]["schedules"][3]["journeys"]):
            da.append(i["dateTime"])
            if (db[-1] == da[index]):
                rmnb = 15 - index - 1
        if (rmnb > 0):
            da = da[:-rmnb]
        if rmnb != svnb:
            f = open("retards_zen.txt", "a")
            f.write(str(datetime.datetime.strptime(db[0], "%Y-%m-%d %H:%M:%S")) + " - Retard de : " + str(datetime.datetime.strptime(dr, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(db[0], "%Y-%m-%d %H:%M:%S")) + '\n')
            f.close()
            db.pop(0)
            svnb = rmnb
            wait()
        else:
            dr = da[0]
        if rmnb == 10:
            return
        time.sleep(3)
        late(dr, svnb)

    while True:
        if datetime.datetime.now().time() > datetime.time(8,0,0) and datetime.datetime.now().time() < datetime.time(9,0,0):
            db = []
            svnb = 0
            dr = None
            r = requests.get('http://api-kraken.tisseo.fr/v1/stops_schedules.json?stopAreaId=stop_area:SA_731&number=15&timetableByArea=1&key=t0b6442937d70d40d1a81d28cd3c94791&lang=fr')
            for index, i in enumerate(json.loads(r.text)["departures"]["stopAreas"][0]["schedules"][3]["journeys"]):
                db.append(i["dateTime"])
                if index == 0:
                    thms = i["waiting_time"].split(":")
                    ts = (int(thms[0]) * 3600 + int(thms[1]) * 60 + int(thms[2])) / 2
            time.sleep(ts)
            wait()
            late(dr, svnb)
            f = open("retards_zen.txt", "a")
            f.write('\n')
            f.close()
        else:
            time.sleep(120)

except Exception as e:
    print(e)
