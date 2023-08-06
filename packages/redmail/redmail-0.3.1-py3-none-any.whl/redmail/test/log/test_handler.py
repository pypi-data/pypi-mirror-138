
import pytest
from redmail import EmailSender
from redmail import EmailHandler
import logging

def _create_dummy_send(messages:list):
    def _dummy_send(msg):
        messages.append(msg)
    return _dummy_send

def test_default_body():
    hdlr = EmailHandler(host="localhost", port=0, receivers=["me@example.com"], subject="Some logging")
    # By default, this should be body if text/html/html_template/text_template not specified
    assert hdlr.email.text == "{{ msg }}"


@pytest.mark.parametrize("kwargs,exp_headers,exp_payload",
    [
        pytest.param(
            {
                "email": EmailSender(host="localhost", port=0),
                "subject": "A log record",
                "sender": "me@example.com",
                "receivers": ["he@example.com", "she@example.com"],
            }, 
            {
                "from": "me@example.com",
                "to": "he@example.com, she@example.com",
                "subject": "A log record",
                'Content-Transfer-Encoding': '7bit',
                'Content-Type': 'text/plain; charset="utf-8"',
                'MIME-Version': '1.0',
            },
            'a message\n',
            id="Minimal",
        ),
        pytest.param(
            {
                "email": EmailSender(host="localhost", port=0),
                "subject": "A log record",
                "sender": "me@example.com",
                "receivers": ["he@example.com", "she@example.com"],
                "text": "Log Record: \n{{ msg }}",
                "fmt": '%(name)s: %(levelname)s: %(message)s'
            }, 
            {
                "from": "me@example.com",
                "to": "he@example.com, she@example.com",
                "subject": "A log record",
                'Content-Transfer-Encoding': '7bit',
                'Content-Type': 'text/plain; charset="utf-8"',
                'MIME-Version': '1.0',
            },
            'Log Record: \n_test: INFO: a message\n',
            id="Custom message (msg)",
        ),
        pytest.param(
            {
                "email": EmailSender(host="localhost", port=0),
                "subject": "A log record",
                "sender": "me@example.com",
                "receivers": ["he@example.com", "she@example.com"],
                "text": "Log Record: \n{{ record.message }}",
                "fmt": '%(name)s: %(levelname)s: %(message)s'
            }, 
            {
                "from": "me@example.com",
                "to": "he@example.com, she@example.com",
                "subject": "A log record",
                'Content-Transfer-Encoding': '7bit',
                'Content-Type': 'text/plain; charset="utf-8"',
                'MIME-Version': '1.0',
            },
            'Log Record: \na message\n',
            id="Custom message (record)",
        ),
        pytest.param(
            {
                "email": EmailSender(host="localhost", port=0),
                "subject": "Log: {record.name} - {record.levelname}",
                "sender": "me@example.com",
                "receivers": ["he@example.com", "she@example.com"],
            }, 
            {
                "from": "me@example.com",
                "to": "he@example.com, she@example.com",
                "subject": "Log: _test - INFO",
                'Content-Transfer-Encoding': '7bit',
                'Content-Type': 'text/plain; charset="utf-8"',
                'MIME-Version': '1.0',
            },
            'a message\n',
            id="Sender with fomatted subject",
        ),
        pytest.param(
            {
                "email": EmailSender(host="localhost", port=0),
                "subject": "A log record",
                "sender": "me@example.com",
                "receivers": ["he@example.com", "she@example.com"],
                "fmt": '%(name)s: %(levelname)s: %(message)s',
                "html": "<h1>{{ record.levelname }}</h1><p>{{ msg }}</p>"
            }, 
            {
                "from": "me@example.com",
                "to": "he@example.com, she@example.com",
                "subject": "A log record",
                'Content-Type': 'multipart/alternative',
            },
            ["<h1>INFO</h1><p>_test: INFO: a message</p>\n"],
            id="Custom message (HTML, msg)",
        ),
        pytest.param(
            {
                "email": EmailSender(host="localhost", port=0),
                "subject": "A log record",
                "sender": "me@example.com",
                "receivers": ["he@example.com", "she@example.com"],
                "fmt": '%(name)s: %(levelname)s: %(message)s',
                "html": "<h1>{{ record.levelname }}</h1><p>{{ record.message }}</p>"
            }, 
            {
                "from": "me@example.com",
                "to": "he@example.com, she@example.com",
                "subject": "A log record",
                'Content-Type': 'multipart/alternative',
            },
            ["<h1>INFO</h1><p>a message</p>\n"],
            id="Custom message (HTML, record)",
        ),
    ]
)
def test_emit(logger, kwargs, exp_headers, exp_payload):
    msgs = []
    fmt = kwargs.pop("fmt", None)
    hdlr = EmailHandler(**kwargs)
    hdlr.formatter = logging.Formatter(fmt)
    hdlr.email.send_message = _create_dummy_send(msgs)
    
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    logger.info("a message")
    
    assert len(msgs) == 1
    msg = msgs[0]
    headers = dict(msg.items())
    payload = msg.get_payload()

    assert headers == exp_headers

    if isinstance(payload, str):
        assert payload == exp_payload
    else:
        # HTML (and text) of payloads
        payloads = [pl.get_payload() for pl in payload]
        assert payloads == exp_payload
