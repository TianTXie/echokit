class MockContext:
    log_stream_name = '1999/09/09/[$LATEST]some_id'
    log_group_name = 'aws/lambda/mock_skill'
    aws_request_id = 'some-unique-id'
    memory_limit_in_mb = 'Mem. limits(MB): 128'


def build_slot(name, value, confirmation_status='NONE'):
    return {name: {'name': name, 'value': value,
                   'confirmationStatus': confirmation_status}}


def build_intent(intent_name, new=True, slots=None, attributes=None,
                 application_id='random_app_id'):
    """Sets intent parameters for tests"""
    intent = {
        "session": {
            "new": False,
            "sessionId": "amzn1.echo-api.session.[unique-value-here]",
            "attributes": {},
            "user": {
                "userId": "amzn1.ask.account.[unique-value-here]"
            },
            "application": {
                "applicationId": "amzn1.ask.skill.[unique-value-here]"
            }
        },
        "version": "1.0",
        "request": {
            "locale": "en-US",
            "timestamp": "2016-10-27T21:06:28Z",
            "type": "IntentRequest",
            "requestId": "amzn1.echo-api.request.[unique-value-here]",
            "intent": {
                "slots": {},
                "name": "BaseIntent"
            }
        },
        "context": {
            "AudioPlayer": {
                "playerActivity": "IDLE"
            },
            "System": {
                "device": {
                    "supportedInterfaces": {
                        "AudioPlayer": {}
                    }
                },
                "application": {
                    "applicationId": "amzn1.ask.skill.[unique-value-here]"
                },
                "user": {
                    "userId": "amzn1.ask.account.[unique-value-here]"
                }
            }
        }
    }
    intent['request']['intent']['name'] = intent_name
    intent['session']['new'] = new
    intent['session']['application']['applicationId'] = application_id
    if slots:
        intent['request']['intent']['slots'] = slots
    if attributes:
        intent['session']['attributes'] = attributes
    return intent


LAUNCH_REQUEST = {
    "session": {
        "new": True,
        "sessionId": "amzn1.echo-api.session.[unique-value-here]",
        "attributes": {},
        "user": {
            "userId": "amzn1.ask.account.[unique-value-here]"
        },
        "application": {
            "applicationId": "amzn1.ask.skill.[unique-value-here]"
        }
    },
    "version": "1.0",
    "request": {
        "locale": "en-US",
        "timestamp": "2016-10-27T18:21:44Z",
        "type": "LaunchRequest",
        "requestId": "amzn1.echo-api.request.[unique-value-here]"
    },
    "context": {
        "AudioPlayer": {
            "playerActivity": "IDLE"
        },
        "System": {
            "device": {
                "supportedInterfaces": {
                    "AudioPlayer": {}
                }
            },
            "application": {
                "applicationId": "amzn1.ask.skill.[unique-value-here]"
            },
            "user": {
                "userId": "amzn1.ask.account.[unique-value-here]"
            }
        }
    }
}

SESSION_ENDED_REQUEST = {
    "session": {
        "new": False,
        "sessionId": "amzn1.echo-api.session.[unique-value-here]",
        "attributes": {},
        "user": {
            "userId": "amzn1.ask.account.[unique-value-here]"
        },
        "application": {
            "applicationId": "amzn1.ask.skill.[unique-value-here]"
        }
    },
    "version": "1.0",
    "request": {
        "locale": "en-US",
        "timestamp": "2016-10-27T21:11:41Z",
        "reason": "USER_INITIATED",
        "type": "SessionEndedRequest",
        "requestId": "amzn1.echo-api.request.[unique-value-here]"
    },
    "context": {
        "System": {
            "device": {
                "supportedInterfaces": {
                    "AudioPlayer": {}
                }
            },
            "application": {
                "applicationId": "amzn1.ask.skill.[unique-value-here]"
            },
            "user": {
                "userId": "amzn1.ask.account.[unique-value-here]"
            }
        }
    }
}
