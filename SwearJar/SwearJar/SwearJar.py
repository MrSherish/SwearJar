"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    #if intent_name == "AMAZON.HelpIntent":
     #   return get_welcome_response()
    if intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "AddPerson":
        return add_person_to_jar(intent, session)
    elif intent_name == "WhatsRanking":
        return tell_the_ranking(intent, session)
    elif intent_name == "HowMuchInJar":        
        return tell_how_much_in(intent, session)
    elif intent_name == "SetPrice":
        return update_price(intent, session)
    elif intent_name == "RemovePerson":
        return remove_person(intent, session)
    elif intent_name == "ResetJar":
        return reset_jar(intent, session)
    elif intent_name == "HasSworn":
        return add_money_to_person(intent, session)
    elif intent_name == "AskedForAdd":
        return add_person_and_money(intent, session)
    else:
        raise ValueError("Invalid intent")

def add_money_to_person(intent, session):
    session_attributes = session.get('attributes', {})
    person = intent['slots']['Person']['value']
    persons = session_attributes['Persons']
    personsList = persons.keys()
    isPresent = False
    for p in personsList:
        if p == person:
            isPresent = True
    if isPresent:
        session_attributes['Persons'][person] = session_attributes['Persons'][person] + session_attributes['Price'] 
        speech_output = person + " has " + str(session_attributes['Persons'][person]) + " dollars on account"        
    else:
        speech_output = "There is no such person in the jar. Shall I add " + person + " to the jar?"
        session_attributes['Waiting'] = True
        session_attributes['NewPerson'] = person

    reprompt_text = ""
    should_end_session = False
    card_title = intent['name']
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))  

def add_person_and_money(intent, session):
    session_attributes = session.get('attributes', {})
    if session_attributes['Waiting']:
        if intent['slots']['response']['value'] == "yes":
            person = session_attributes['NewPerson']
            session_attributes['Persons'][person] = session_attributes['Price']
            speech_output = person + " has " + str(session_attributes['Persons'][person]) + " dollars on account" 
        else:
            speech_output = "No person was added"
    else:
        speech_output = ""
    reprompt_text = ""
    card_title = intent['name']
    should_end_session = False
    session_attributes['Waiting'] = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session)) 

def remove_person(intent, session):
    session_attributes = session.get('attributes', {})
    person = intent['slots']['Person']['value']
    found = False
    for p in session_attributes['Persons']:
        if p == person:
            found = True
    if found:
        session_attributes['Persons'].pop(person, None)
        speech_output = "Successfuly removed " + person + " from the jar"
    else:
        speech_output = "There's no such person in the jar"
    reprompt_text = ""
    should_end_session = False
    card_title = intent['name']

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))        

def reset_jar(intent, session):
    session_attributes = session.get('attributes', {})
    persons = session_attributes['Persons']
    persons.clear()


    card_title = intent['name']
    speech_output = "Jar has been reseted"
    reprompt_text = ""

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def update_price(intent,session):
    session_attributes = session.get('attributes', {})
    price = session_attributes['Price']
    newPrice = intent['slots']['Money']['value']
    session_attributes['Price'] = int(newPrice)

    card_title = intent['name']
    speech_output = "New price is " + newPrice
    reprompt_text = ""

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def tell_how_much_in(intent, session):
    session_attributes = session.get('attributes', {})
    persons = session_attributes['Persons']
    personsValues = persons.values()
    jarSum = 0
    for value in personsValues:
        jarSum = jarSum + value
    speech_output = "There is " + str(jarSum) + " in the jar"
    reprompt_text = ""
    should_end_session = False
    card_title = intent['name']

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def tell_the_ranking(intent, session):
    session_attributes = session.get('attributes', {})
    persons = session_attributes['Persons']
    personsList = persons.keys()
    card_title = intent['name']
    speech_output = "The ranking is: "
    if not personsList:
        speech_output = "There are no persons in the jar"
    else:
        for person in personsList:
            speech_output = speech_output + person + "with " + str(persons[person]) + "dollars,"
    reprompt_text = ""

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def add_person_to_jar(intent, session):
    session_attributes = session.get('attributes', {})
    persons = session_attributes['Persons']
    newPersonName = intent['slots']['Person']['value']

    personsList = session_attributes['Persons']
    exists = False
    for p in personsList:
        if p == newPersonName:
            exists = True
    if exists:
        speech_output = "That person already exists!"
    else:
        session_attributes['Persons'][newPersonName] = 0
        speech_output = "Added " + newPersonName + " to the jar"
    card_title = intent['name']
    reprompt_text = ""

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = { 'Persons' : {}, 'Price' : 1 } #initialize the local session

    personsAmount = len(session_attributes['Persons'])
    card_title = "Welcome"
    speech_output = "Welcome to the Swear Jar skill. " \
                    "The current price is set to" + str(session_attributes['Price']) + " dollars. " \
                    + "There are " + str(personsAmount) + " persons in the jar."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Swear Jar is ready"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }