from learning_german import send_message
import pytest
from twilio.base.exceptions import TwilioRestException
from unittest import mock


@mock.patch("learning_german.client.messages.create")
def test_send_a_common_word(create_message_mock):
    words_set = [
        {
            "rank": 105,
            "german_word": "wirklich",
            "english_translation": "real, true, natural",
            "part_of_speech": "adjective",
            "url": "http://languagedaily.com/learn-german/vocabulary/common-german-words-3",
        }
    ]
    message = (
        f"The word of the day is... {words_set[0]['german_word']}"
        f" ({words_set[0]['part_of_speech']})"
        f"\n\nMeaning: {words_set[0]['english_translation']}"
        f"\nMore at: {words_set[0]['url']}"
    )

    expected_sid = "SM87105da94bff44b999e4e6eb90d8eb6a"
    create_message_mock.return_value.sid = expected_sid

    to = "+491112223"
    from_ = "+493332221"
    sid = send_message(to, from_, message)

    assert create_message_mock.called is True
    assert sid == expected_sid


@pytest.mark.skip
@mock.patch("learning_german.client.messages.create")
def test_raise_exception_when_cannot_send_a_message(create_message_mock):
    error_message = (
        f"Unable to create record: The 'To' number "
        "+491799999999 is not a valid phone number."
    )
    status = 500
    uri = "/Accounts/ACXXXXXXXXXXXXXXXXX/Messages.json"
    msg = error_message
    create_message_mock.side_effect = TwilioRestException(
        status, uri, msg=error_message
    )
    with pytest.raises(TwilioRestException):
        to = "+491112223"
        from_ = "+493332221"
        send_message(to, from_, "Wrong message")


@mock.patch("learning_german.client.messages.create")
def test_log_error_when_cannot_send_a_message(create_message_mock, caplog):
    error_message = (
        f"Unable to create record: The 'To' number "
        "+491799999999 is not a valid phone number."
    )
    status = 500
    uri = "/Accounts/ACXXXXXXXXXXXXXXXXX/Messages.json"
    msg = error_message
    create_message_mock.side_effect = TwilioRestException(
        status, uri, msg=error_message
    )

    to = "+491112223"
    from_ = "+493332221"
    sid = send_message(to, from_, "Wrong message")

    assert sid is None
    assert "Oh no:" in caplog.text
    assert error_message in caplog.text


def test_send_a_common_word_with_stubs():
    words_set = [
        {
            "rank": 105,
            "german_word": "wirklich",
            "english_translation": "real, true, natural",
            "part_of_speech": "adjective",
            "url": "http://languagedaily.com/learn-german/vocabulary/common-german-words-3",
        }
    ]
    message = (
        f"The word of the day is... {words_set[0]['german_word']}"
        f" ({words_set[0]['part_of_speech']})"
        f"\n\nMeaning: {words_set[0]['english_translation']}"
        f"\nMore at: {words_set[0]['url']}"
    )

    expected_sid = "SM87105da94bff44b999e4e6eb90d8eb6a"

    to = "+491112223"
    from_ = "+493332221"
    sid = send_message(to, from_, message)

    assert sid == expected_sid
