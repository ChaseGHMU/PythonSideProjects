import requests
import time
import datetime
import user
from apscheduler.schedulers.blocking import BlockingScheduler
from twilio.rest import Client

#relevant twilio tokens
twilio_account_sid = "TWILIO ACCOUNT ID HERE"
twilio_token = "PRIVATE TOKEN HERE"

client = Client(twilio_account_sid, twilio_token)

#Fortnite API information
token = "TOKEN FOR FORTNITE API"

#apscheduler setup
sched = BlockingScheduler()

#Persons name, PSN username, Cellphone number
#removed username and number for privacy
chase = user.User("Chase", "", "")
alec = user.User("Alec", "", "")
scott = user.User("Scott", "", "")
herwig = user.User("Herwig", "", "")
jake = user.User("Jake", "", "")
brady = user.User("Brady", "", "")

userlist = list()
userlist.append(jake)
userlist.append(chase)
userlist.append(alec)
userlist.append(scott)
userlist.append(herwig)
userlist.append(brady)

header = {"TRN-Api-Key": token}


def init():
    for x in userlist:
        response = requests.get(x.url, headers=header)
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                continue
            else:
		print(str(datetime.datetime.now()) + ": Added " + x.name + " to the userlist")
                stats = data['lifeTimeStats']
                x.total = int(stats[7]['value'])
                x.top25 = int(stats[5]['value'])
                x.top12 = int(stats[4]['value'])
                x.top6 = int(stats[3]['value'])
            time.sleep(5)


def check_scores():
    for x in userlist:
        response = requests.get(x.url, headers=header)
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                print(x.name + " Not in system")
                continue
            else:
                stats = data['lifeTimeStats']
                total = int(stats[7]['value'])
                top25 = int(stats[5]['value'])
                top12 = int(stats[4]['value'])
                top6 = int(stats[3]['value'])

                if total == x.total:
                    print(str(datetime.datetime.now()) + ": No update in score for " + x.name)
                else:
                    if x.top25 == top25 and x.top12 == top12 and x.top6 == top6:
                        x.total = total
                        print(str(datetime.datetime.now()) + ": Texting " + x.name)
                        bodyMessage = "Hey "+x.name+", you suck at Fortnite. \nLove, Chase"
                        client.messages.create(
                            to=x.number,
                            from_="TWILIO GENERATED NUMBER",
                            body=bodyMessage
                        )
                    else:
                        print(str(datetime.datetime.now())+": "+x.name+" Won a game. Updating scores.")
                        x.total = total
                        x.top25 = top25
                        x.top6 = top6
                        x.top12 = top12
        time.sleep(5)


def main():
    init()
    sched.add_job(check_scores, 'interval', seconds=180)
    sched.start()


main()

