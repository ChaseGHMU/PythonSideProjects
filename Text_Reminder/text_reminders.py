from twilio.rest import Client
from apscheduler.schedulers.blocking import BlockingScheduler

twilio_account_sid = "ACCOUNT_ID_HERE"
twilio_token = "PRIVATE_TOKEN_HERE"

client = Client(twilio_account_sid, twilio_token)
sched = BlockingScheduler()


def text_jake():
    client.messages.create(
        to="RECIPIENT NUMBER",
        from_="NUMBER GENERATED BY TWILIO",
        body="Daily reminder that I love you"
    )


def text_pete():
    client.messages.create(
        to="RECIPIENT NUMBER",
        from_="NUMBER GENERATED BY TWILIO",
        body="C'est Vendredi, mes mecs"
    )


def main():
    sched.add_job(text_jake, 'cron', day_of_week="mon-sun", hour=21)
    sched.add_job(text_pete, 'cron', day_of_week="fri", hour=9)
    sched.start()


main()
