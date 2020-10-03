#!/usr/bin/env python3
import os
import json
import sendgrid

# create our client instance and pass it our key
sg = sendgrid.SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))

# define three parameters bodies for the API calls below
# general stats header parameters
STAT_PARAMS = {
    "aggregated_by": "day",
    "limit": 1,
    "start_date": "2020-05-12",
    "end_date": "2020-05-13",
    "offset": 1,
}

# mailbox recipient header parameters
MB_PARAMS = {
    "end_date": "2020-05-13",
    # 'mailbox_providers': 'Gmail',
    "aggregated_by": "day",
    "limit": 1,
    "offset": 1,
    "start_date": "2020-05-12",
}

# browser views header parameters
B_PARAMS = {
    "end_date": "2020-05-13",
    "aggregated_by": "day",
    # 'browsers': 'iPhone',
    "limit": "test_string",
    "offset": "test_string",
    "start_date": "2020-05-12",
}

endpoints = [
    sg.client.stats.get(query_params=STAT_PARAMS),
    sg.client.browsers.stats.get(query_params=MB_PARAMS),
    sg.client.browsers.stats.get(query_params=B_PARAMS),
]


def get_send_data():
    # empty list for our JSON results
    send_data = []

    # Retrieve general email stats, mailbox stats, and device stats
    # GET /mailbox_providers/stats
    try:
        print("Retrieving statistics...")
        for endpoint in endpoints:
            response = endpoint
            if response.status_code == 200:
                print("Call Successful.")
                json_response = json.loads(response.body)
                json_formatted_string = json.dumps(
                    json_response, indent=4, sort_keys=True
                )
                # print(json_formatted_string)
                send_data.append(json_formatted_string)
            else:
                print("Error on retrieval.")
        with open("SendData.txt", "w") as f:
            for send in send_data:
                f.write(send)
            f.close()
    except Exception as e:
        print("Error: {0}".format(e))


if __name__ == "__main__":
    get_send_data()