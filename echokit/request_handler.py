import logging

handler_funcs = {}

from echokit import requests
from echokit.responses import Response
from echokit.speech import PlainTextOutputSpeech
from echokit._utils import convert_keys, revert_keys

logger = logging.getLogger(__name__)


def handler(event, context):
    """Lambda service calls this method when sending us a request

    :param event: Contains data on the Alexa request, used to 
        create ``echokit.request.RequestWrapper``
    :param context: RequestWrapper context, used primarily for logging. 
        **Note**: *Not* the same as ``echokit.request.Context``
    :return: Dict of ``echokit.response.ResponseWrapper`` object
    """
    logger.info(f"Received event: {event}")
    logger.info(f"Log stream name: {context.log_stream_name}")
    logger.info(f"Log group name: {context.log_group_name}")
    logger.info(f"RequestWrapper ID: {context.aws_request_id}")
    logger.info(f"Mem. limits(MB): {context.memory_limit_in_mb}")

    convert_keys(event)
    request_wrapper = requests.RequestWrapper(event.get('request'),
                                              event.get('session'),
                                              event.get('context'),
                                              event.get('version'))
    handler_func = _get_handler(event['request'])
    response = handler_func(request_wrapper)
    # Won't always receive responses (ex: SessionEndedRequest)
    if response is not None:
        response_dict = response._dict()
        revert_keys(response_dict)
        return response_dict


def fallback_default(request_wrapper):
    """Default handler for valid intent names without handlers"""
    speech = PlainTextOutputSpeech("Sorry, I didn't understand your request")
    return Response(output_speech=speech)


def _get_handler(request):
    if request['type'] == requests.INTENT:
        func = handler_funcs.get(request['intent']['name'], fallback_default)
    else:
        func = handler_funcs[request['type']]
    return func
