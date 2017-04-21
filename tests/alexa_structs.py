from collections import namedtuple
import echopy
from echopy.response import Response, OutputSpeech

Context = namedtuple('Context', 'log_stream_name log_group_name '
                                'aws_request_id memory_limit_in_mb')

mock_context = Context('log name', 'group name', 'req ID', '10mb')

start_session = {
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

end_session = {
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

base_intent = {
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


def create_intent(intent_name, new=True, slots=None, attributes=None,
                  application_id=None):
    intent = dict(base_intent)
    intent['request']['intent']['name'] = intent_name
    intent['session']['new'] = new

    if attributes:
        intent['session']['attributes'] = attributes

    if slots:
        intent['request']['intent']['slots'] = slots

    if application_id:
        intent['session']['application']['applicationId'] = application_id
    return intent


@echopy.on_session_launch
def session_started(event):
    output_speech = OutputSpeech(text="You started a new session!")
    return Response(output_speech=output_speech)


@echopy.on_session_end
def session_ended(event):
    output_speech = OutputSpeech("You ended our session :[")
    return Response(output_speech=output_speech)


@echopy.on_intent('SomeIntent')
def on_intent(event):
    output_speech = OutputSpeech(text="I did something with SomeIntent!")
    return Response(output_speech=output_speech)


@echopy.on_intent('OrderIntent')
def specific_intent(event):
    order = event.request.intent.slots['Order'].value
    session_attrs = {'last_order': order}
    response_text = f'You asked me to {order}'
    img_url = "http://i.imgur.com/PytSZCG.png"
    card = echopy.StandardCard(title="Order",
                               text=f"You wanted me to {order}",
                               small_image_url=img_url,
                               large_image_url=img_url)
    return Response(output_speech=OutputSpeech(text=response_text),
                    session_attributes=session_attrs, card=card)

@echopy.fallback
def unimplemented(event):
    intent_name = event.request.intent.name
    output_speech = OutputSpeech(f"Sorry, {intent_name} isn't implemented!")
    return Response(output_speech)