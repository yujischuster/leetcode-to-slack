import schedule
import time

def job_name(text):
    print("I am doing this job!" + text)

schedule.every().tuesday.at("18:26").do(job_name, "hey")

while True:
    schedule.run_pending()
    time.sleep(1)