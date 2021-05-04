# Script that checks Cowin portal for vaccine availability

### This python script polls on https://www.cowin.gov.in/home website to check if the vaccine is available at any center in your pincode. It sends a mail to the specified email ids as a mechanism of notification of availability. 

## Setup
- Download this script wherever you plan to run
- Edit the following variables at the beginning of poll.py
> pincode, sender_email, to_email, sender_password_base64_encoded
- Run the script with `python poll.py`