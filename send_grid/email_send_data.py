#!/usr/bin/env python3
import base64
import os
import json
import sendgrid
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
    ContentId,
)


# create our client instance and pass it our key
sg = sendgrid.SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))

# from address we pass to our Mail object, edit with your name
FROM_EMAIL = "Your_Name@SendGridTest.com"

# list of emails you would like the report sent to
TO_EMAILS = ["your_email@domain.com", "your_email+1@domain.com"]


def email_send_data():
    """Reads from a file (assumed to exist), encodes the binary, then
    sends it as an email attachment to specified address
    :returns API response code
    :raises Exception e: raises an exception"""
    # create our message object
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAILS,
        subject="Send Data attached",
        html_content="<strong>Your Send Data is attached!</strong>",
    )
    # read the binary version of our text file
    with open("SendData.txt", "rb") as f:
        data = f.read()
        f.close()
    # create our attachment object, first pass the binary data above to base64 for encoding
    encoded_file = base64.b64encode(data).decode()
    # attach the file and set its properties, info here: https://sendgrid.com/docs/API_Reference/Web_API_v3/Mail/index.html
    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName("Send_Data.txt"),
        FileType("text/plain"),
        Disposition("attachment"),
    )
    message.attachment = attachedFile
    # create our sendgrid client object, pass it our key, then send and return our response objects
    try:
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print(f"Response code: {code}")
        print(f"Response headers: {headers}")
        print(f"Response body: {body}")
        print("Email send data has been sent as an attachment")
    except Exception as e:
        print("Error: {0}".format(e))
    return str(response.status_code)


if __name__ == "__main__":
    email_send_data()