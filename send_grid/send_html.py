#!/usr/bin/env python3
import os
from sendgrid.helpers.mail import Mail, To
from sendgrid import SendGridAPIClient

# from address we pass to our Mail object, edit with your name
FROM_EMAIL = "Your_Name@SendGridTest.com"

# create our To list to pass to our mail object
# the substitutions in this list are the dynamic HTML values
TO_EMAILS = [
    To(
        email="your_email@domain.com",  # update with your email
        name="Sir or Madam",
        substitutions={
            "-name-": "James",
            "-link-": "https://twilio.com",
            "-event-": "Twilio Signal",
        },
    ),
    To(
        email="your_email+1@domain.com",  # update with your email alias
        name="Sir or Madam",
        substitutions={
            "-name-": "Joe",
            "-link-": "https://github.com/",
            "-event-": "Developers Anonymous",
        },
        # override the subject for this particular recipient
        subject="Developers need to stick together!",
    ),
]


def send_html():
    """Send an HTML email to the global list of email addresses
    :returns API response code
    :raises Exception e: raises an exception"""
    # create our Mail object and populate dynamically with our to_emails
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAILS,
        subject="Hello from SendGrid!",
        html_content="<strong>Hello there from SendGrid</strong> "
        + "It was good meeting you -name- at -event-."
        + "Enjoy this -link-! ",
        is_multiple=True,
    )

    # create our sendgrid client object, pass it our key, then send and return our response objects
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print(f"Response code: {code}")
        print(f"Response headers: {headers}")
        print(f"Response body: {body}")
        print("HTML Messages Sent!")
    except Exception as e:
        print("Error: {0}".format(e))
    return str(response.status_code)


if __name__ == "__main__":
    send_html()