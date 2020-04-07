import json
import logging
from collections import namedtuple
import os
import random
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


environment = os.getenv("ENVIRONMENT", "dev")


class FakeClient:
    def __init__(self, **kwargs):
        self.messages = self.MessageFactory()

    class MessageFactory:
        @staticmethod
        def create(**kwargs):
            Message = namedtuple("Message", ["sid"])
            message = Message(sid="SM87105da94bff44b999e4e6eb90d8eb6a")
            return message


if environment == "dev":
    client = FakeClient()
else:
    client = Client()
# or
# account_sid = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# auth_token = "your_auth_token"
# client = Client(account_sid, auth_token)


def send_message(to, from_, message):
    try:
        sent_message = client.messages.create(to=to, from_=from_, body=message)
    except TwilioRestException as e:
        logging.error(f"Oh no: {e}")
        return

    return sent_message.sid


def send_a_german_word():
    german_words = json.load(open("most-common-german-words.json"))
    chosen_word = random.choice(german_words)
    if chosen_word["part_of_speech"]:
        part_of_speech = f"({chosen_word['part_of_speech']})"
    else:
        part_of_speech = ""
    if chosen_word["english_translation"]:
        meaning = f"\n\nMeaning: {chosen_word['english_translation']}"
    else:
        meaning = ""
    message = (
        f"The word of the day is... "
        f"{chosen_word['german_word'].upper()} {part_of_speech} {meaning}"
        f"\nMore at: {chosen_word['url']}"
    )
    sid = send_message("+491799324300", "+13477673436", message)
    return sid


if __name__ == "__main__":
    send_a_german_word()
