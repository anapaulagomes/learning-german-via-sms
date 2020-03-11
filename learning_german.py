import logging
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


client = Client()
# or
# account_sid = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# auth_token = "your_auth_token"
# client = Client(account_sid, auth_token)


def send_message(message):
    try:
        sent_message = client.messages.create(
            to="+491799324300", 
            from_="+13477673436",
            body=message
        )
    except TwilioRestException as e:
        logging.error(f'Oh no: {e}')
        return

    return sent_message.sid
