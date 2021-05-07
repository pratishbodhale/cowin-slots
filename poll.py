import http.client
import time
import json
import smtplib 
import base64
from datetime import datetime
from datetime import date
import pytz

IST = pytz.timezone('Asia/Kolkata')

## Define the user specific variables here 
pincode = ''
sender_email = ''
to_email = ''
sender_password_base64_encoded = ''
poll_duration_in_secs = 300.0

def emailText(from_email, to, subject, body):
    return """From: %s
To: %s
Subject: %s

%s
    """ % (from_email, ", ".join(to), subject, body)

def sendEmail(center):
    try: 
        print("Establishing email server connection ...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo() 
        server.starttls()
        server.ehlo()

        server.login(sender_email, base64.b64decode(sender_password_base64_encoded.encode()).decode()) 

        subject = 'Slot available for vaccination'
        body = json.dumps(center)
        email_text = emailText(sender_email, [to_email], subject, body)

        server.sendmail(sender_email, to_email, email_text) 
        server.close()

        print("Email sent!")
    except Exception as e:
        print("Exception has occured")
        print(e)

def checkForSlots(response):
    found = False
    for center in response["centers"]:
        for sessions in center["sessions"]:
            if sessions["available_capacity"] > 0:
                print("Available at: ", center)
                found = True
                sendEmail(center)

    if found == False:
        print("No Available centers found at: " + datetime.now(IST).strftime("%m/%d/%Y, %H:%M:%S"))


def main():
    starttime = time.time()
    while True:
        try:
            connection = http.client.HTTPSConnection("cdn-api.co-vin.in")
            dateString = datetime.now(IST).strftime("%d-%m-%y")

            connection.request("GET", "/api/v2/appointment/sessions/public/calendarByPin?pincode=441302&date=" + dateString)
            response = connection.getresponse()
            stringResponse = response.read().decode()
            jsonResponse = json.loads(stringResponse)
            
            checkForSlots(jsonResponse)
        except Exception as e:
            print("Exception has occured in main")
            print(e)

        time.sleep(poll_duration_in_secs - ((time.time() - starttime) % poll_duration_in_secs))

if __name__ == "__main__":
    main()