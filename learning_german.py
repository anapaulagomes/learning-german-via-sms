import json
import logging
import random
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


client = Client()
# or
# account_sid = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# auth_token = "your_auth_token"
# client = Client(account_sid, auth_token)


def send_message(to, from_, message):
    try:
        sent_message = client.messages.create(
            to=to,
            from_=from_,
            body=message
        )
    except TwilioRestException as e:
        logging.error(f'Oh no: {e}')
        return

    return sent_message.sid


def send_a_german_word():
    german_words = json.load(open('most-common-german-words.json'))
    chosen_word = random.choice(german_words)
    if chosen_word['part_of_speech']:
        part_of_speech = f"({chosen_word['part_of_speech']})"
    else:
        part_of_speech = ''
    if chosen_word['english_translation']:
        meaning = f"\n\nMeaning: {chosen_word['english_translation']}"
    else:
        meaning = ''
    message = (
        f"The word of the day is... "
        f"{chosen_word['german_word'].upper()} {part_of_speech} {meaning}"
        f"\nMore at: {chosen_word['url']}"
    )
    sid = send_message("+491799324300", "+13477673436", message)
    return sid


if __name__ == '__main__':
    send_a_german_word()
