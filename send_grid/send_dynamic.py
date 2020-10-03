#!/usr/bin/env python3
import os
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

# from address we pass to our Mail object, edit with your name
FROM_EMAIL = "Your_Name@SendGridTest.com"

# update to your dynamic template id from the UI
TEMPLATE_ID = "d-d027f2806c894df38c59a9dec5460594"

# list of emails and preheader names, update with yours
TO_EMAILS = [
    ("your_email@domain.com", "James Holden"),
    # update email and name
    ("your_email+1@domain.com", "Joe Miller"),
]


def send_dynamic():
    """Send a dynamic email to a list of email addresses
    :returns API response code
    :raises Exception e: raises an exception"""
    # create Mail object and populate
    message = Mail(from_email=FROM_EMAIL, to_emails=TO_EMAILS)
    # pass custom values for our HTML placeholders
    message.dynamic_template_data = {
        "subject": "SendGrid Development",
        "place": "New York City",
        "event": "Twilio Signal",
    }
    message.template_id = TEMPLATE_ID
    # create our sendgrid client object, pass it our key, then send and return our response objects
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print(f"Response code: {code}")
        print(f"Response headers: {headers}")
        print(f"Response body: {body}")
        print("Dynamic Messages Sent!")
    except Exception as e:
        print("Error: {0}".format(e))
    return str(response.status_code)


if __name__ == "__main__":
    send_dynamic()