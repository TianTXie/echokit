from echopy.request import Request
from echopy.response import Response, OutputSpeech, SimpleCard, \
    StandardCard, LinkAccountCard, Reprompt

application_id = None

request_handlers = {}


def fallback_default(event):
    output_speech = OutputSpeech("Sorry, I didn't understand your request")
    return Response(output_speech=output_speech)


def handler(event, context):
    """Lambda service calls this method when sending us a request
    
    :param event: Contains data on the Alexa request, used to 
        create ``echopy.request.Request``
    :param context: Request context, used primarily for logging. **Note**: 
        *Not* the same as ``echopy.request.Context``
    :return: Dict of ``echopy.response.Response`` object
    """
    print(f"Log stream name: {context.log_stream_name}")
    print(f"Log group name: {context.log_group_name}")
    print(f"Request ID: {context.aws_request_id}")
    print(f"Mem. limits(MB): {context.memory_limit_in_mb}")
    event = Request.from_json(event)
    if event.request.request_type == 'IntentRequest':
        # Recognized intent name and handler function
        intent_name = event.request.intent.name
        if intent_name in request_handlers:
            resp = request_handlers.get(intent_name)
        else:
            # Handle intents without registered handlers
            print(f"Unexpected intent {intent_name}, falling back")
            resp = request_handlers.get('fallback')
            if not resp:
                resp = fallback_default
    else:
        # Other requests are LaunchRequest and SessionEndedRequest
        resp = request_handlers.get(event.request.request_type)
    return resp(event).to_json()


def on_session_launch(func):
    request_handlers['LaunchRequest'] = func


def on_session_end(func):
    request_handlers['SessionEndedRequest'] = func


def on_intent(intent_name):
    def func_wrapper(func):
        request_handlers[intent_name] = func
    return func_wrapper


def fallback(func):
    request_handlers['fallback'] = func


__all__ = ['request', 'response']