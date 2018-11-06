# -*- coding: utf-8 -*-
from __future__ import print_function

from ask_sdk_core.skill_builder import SkillBuilder
#from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.dispatch_components import (AbstractRequestHandler, AbstractExceptionHandler,
                                              AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from ask_sdk_model.interfaces.audioplayer import (PlayDirective, PlayBehavior, AudioItem, Stream)

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

import boto3
s3 = boto3.client('s3')

## data
SKILL_NAME = "The Kids Times"
WELCOME_MSG = "Welcome Kids Times, what do you want to listen"
WELCOME_NEXT = "what do you want to listen"
HELP_MESSAGE = "You can say tell me a category, or, you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."
DEVICE_NOT_SUPPORTED = "Sorry, this skill is not supported on this device"

BUCKET_NAME = "kidstimes"
SAMPLE_FILE = "World/469.wav"

## System handlers
# Standard requests
# LaunchRequest, IntentRequest, SessionEndedRequest, CanFulfillIntentRequest
class KidsTimesHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_request_type("LaunchRequest")(handler_input) or is_intent_name("KidsTimes")(handler_input))

    def handle(self, handler_input):
        logger.info("Welcome Kids Times")
        handler_input.response_builder.speak(WELCOME_MSG).ask(WELCOME_NEXT)
        return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("Session ended reason: {}".format(handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response

class CheckAudioInterfaceHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        if handler_input.request_envelope.context.system.device:
            return handler_input.request_envelope.context.system.device.supported_interfaces.audio_player is None
        else:
            return False

    def handle(self, handler_input):
        logger.info("In CheckAudioInterfaceHandler")
        handler_input.response_builder.speak(DEVICE_NOT_SUPPORTED).set_should_end_session(True)
        return handler_input.response_builder.response

## Exception handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(HELP_REPROMPT)
        return handler_input.response_builder.response

## Logger interceptors
class RequestLogger(AbstractRequestInterceptor):
    def process(self, handler_input):
        logger.debug("Alexa Request: {}".format(handler_input.request_envelope.request))

class ResponseLogger(AbstractResponseInterceptor):
    def process(self, handler_input, response):
        logger.debug("Alexa Response: {}".format(response))

## Built-In Intents
class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(HELP_REPROMPT).set_card(SimpleCard(SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response

class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In FallbackIntentHandler")

class CancelIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.CancelIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In CancelIntentHandler")

        return stop(handler_input.response_builder)

class StopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In StopIntentHandler")

        return stop(handler_input.response_builder)
        
class NavigateHomeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.NavigateHomeIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In NavigateHomeIntentHandler")

## AudioPlayer Intent
class PauseIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.PauseIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In PauseIntentHandler")

        return stop(handler_input.response_builder)

class ResumeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.ResumeIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In ResumeIntentHandler")
        # load playback info
        return handler_input.response_builder.speak("I can't support not yet this function").response

class LoopOffIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.LoopOffIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In LoopOffIntentHandler")
        
class LoopOnIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.LoopOnIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In LoopOnIntentHandler")
        
class NextIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.NextIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In NextIntentHandler")
        
class PreviousIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.PreviousIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In PreviousIntentHandler")
        
class RepeatIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In RepeatIntentHandler")

class ShuffleOnIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.ShuffleOnIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In ShuffleOnIntentHandler")

class StartOverIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.StartOverIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In StartOverIntentHandler")

## AudioPlayer Requests
class PlaybackStartedHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("AudioPlayer.PlaybackStarted")(handler_input)
    
    def handle(self, handler_input):
        logger.info("In PlaybackStartedHandler")
        return handler_input.response_builder.response
        
class PlaybackFinishedHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("AudioPlayer.PlaybackFinished")(handler_input)
    
    def handle(self, handler_input):
        logger.info("In PlaybackFinishedHandler") 
        return handler_input.response_builder.response
       
class PlaybackStoppedHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("AudioPlayer.PlaybackStopped")(handler_input)
    
    def handle(self, handler_input):
        logger.info("In PlaybackStoppedHandler")
        # will save playback info in db
        # handler_input.request_envelope.request.offset_in_milliseconds
        return handler_input.response_builder.response
        
class PlaybackNearlyFinishedHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("AudioPlayer.PlaybackNearlyFinished")(handler_input)
    
    def handle(self, handler_input):
        logger.info("In PlaybackNearlyFinished")
        return handler_input.response_builder.response
        
class PlaybackFailedHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("AudioPlayer.PlaybackFailed")(handler_input)
    
    def handle(self, handler_input):
        logger.info("In PlaybackFailedHandler")
        return handler_input.response_builder.response

## PlaybackController Intent
class NextCommandIssuedHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("PlaybackController.NextCommandIssued")(handler_input)
    
    def handle(self, handler_input):
        logger.info("In NextCommandIssued")
        
class PreviousCommandIssuedHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("PlaybackController.PreviousCommandIssued")(handler_input)
    
    def handle(self, handler_input):
        logger.info("In PreviousCommandIssued")
        
class PlayCommandIssuedHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("PlaybackController.PlayCommandIssued")(handler_input)
    
    def handle(self, handler_input):
        logger.info("In PlayCommandIssued")

## Custom Intents
class PlayKidsTimesHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("PlayKidsTimes")(handler_input)

    def handle(self, handler_input):
        logger.info("Play Kids Times")
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': SAMPLE_FILE
            }
        )
        return play(handler_input.response_builder, url)

from ask_sdk_model.interfaces.audioplayer import (PlayDirective, PlayBehavior, AudioItem, Stream, StopDirective)
def play(response_builder, url):
    response_builder.add_directive(PlayDirective(
        play_behavior = PlayBehavior.REPLACE_ALL,
        audio_item = AudioItem(
            stream = Stream(url=url, token="0"),
            metadata = None
        ))
    ).set_should_end_session(True)
    return response_builder.response

def stop(response_builder):
    response_builder.add_directive(StopDirective())
    return response_builder.response

sb = SkillBuilder()
#sb = StandardSkillBuilder(table_name=data.DYNAMODB_TABLE_NAME, auto_create_table=True)

# ############# REGISTER HANDLERS #####################
# Handlers
sb.add_request_handler(KidsTimesHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(CheckAudioInterfaceHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(CancelIntentHandler())
sb.add_request_handler(StopIntentHandler())
sb.add_request_handler(NavigateHomeIntentHandler())

sb.add_request_handler(PauseIntentHandler())
sb.add_request_handler(ResumeIntentHandler())
sb.add_request_handler(LoopOffIntentHandler())
sb.add_request_handler(LoopOnIntentHandler())
sb.add_request_handler(NextIntentHandler())
sb.add_request_handler(PreviousIntentHandler())
sb.add_request_handler(RepeatIntentHandler())
sb.add_request_handler(ShuffleOnIntentHandler())
sb.add_request_handler(StartOverIntentHandler())

sb.add_request_handler(PlaybackStartedHandler())
sb.add_request_handler(PlaybackFinishedHandler())
sb.add_request_handler(PlaybackStoppedHandler())
sb.add_request_handler(PlaybackNearlyFinishedHandler())
sb.add_request_handler(PlaybackFailedHandler())

sb.add_request_handler(NextCommandIssuedHandler())
sb.add_request_handler(PreviousCommandIssuedHandler())
sb.add_request_handler(PlayCommandIssuedHandler())

sb.add_request_handler(PlayKidsTimesHandler())

# Exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Interceptors
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# AWS Lambda handler
handler = sb.lambda_handler()