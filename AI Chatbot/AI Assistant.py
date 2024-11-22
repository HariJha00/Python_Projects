import re
import long_responses as long


def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    # Greetings
    response('Hello!', ['hello', 'hi', 'hey', 'heyo'], single_response=True)
    response('Hi there! How can I help you today?', ['hello', 'hi', 'greetings'], single_response=True)
    response('Hey! What’s up?', ['sup', 'what\'s up'], single_response=True)

    # Farewells
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('Take care!', ['bye', 'farewell', 'see you'], single_response=True)
    response('Talk to you later!', ['catch you later'], single_response=True)

    # Emotions and well-being
    response('I\'m doing great! How about you?', ['how', 'are', 'you', 'doing'], required_words=['how', 'you'])
    response('I\'m feeling awesome, thanks for asking!', ['how', 'do', 'you', 'feel'], required_words=['feel'])
    response('I hope you’re doing well!', ['hope', 'you', 'doing', 'well'], required_words=['hope', 'well'])

    # Gratitude
    response('You’re welcome!', ['thank', 'thanks', 'appreciate'], single_response=True)
    response('No problem at all!', ['thank you', 'thanks'], single_response=True)

    # Jokes
    response('Why don’t scientists trust atoms? Because they make up everything!', ['joke', 'funny', 'laugh'],
             single_response=True)
    response('I would tell you a construction joke, but I’m still working on it!', ['tell', 'me', 'a', 'joke'],
             required_words=['joke'])

    # Help or Assistance
    response('Sure, what do you need help with?', ['help', 'assist', 'support'], single_response=True)
    response('I can help with that! What exactly do you need?', ['need', 'help', 'with'], required_words=['help'])

    # Personal Information
    response('I’m your friendly chatbot, here to help you out!', ['who', 'are', 'you'], required_words=['who', 'you'])
    response('I’m just a bunch of code, but I love chatting with you!', ['what', 'are', 'you'],
             required_words=['what', 'you'])

    # Compliments
    response('Thank you! You’re too kind!', ['you', 'are', 'great', 'amazing'], required_words=['you', 'great'])
    response('I appreciate that! You’re awesome too!', ['i', 'like', 'you'], required_words=['like', 'you'])

    # Weather
    response('I’m not sure, but I hope it’s sunny wherever you are!', ['weather', 'outside'],
             required_words=['weather'])
    response('It’s always warm and cozy here in the digital world.', ['is', 'it', 'cold'], required_words=['cold'])

    # Random Facts
    response(
        'Did you know honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old and still edible!',
        ['fact', 'random'], required_words=['fact'])
    response('A day on Venus is longer than a year on Venus!', ['fact', 'interesting'], required_words=['fact'])

    # Encouragement
    response('You’ve got this! Keep going!', ['motivate', 'motivation'], required_words=['motivate'])
    response('Believe in yourself—you’re capable of amazing things!', ['inspire', 'encourage'],
             required_words=['inspire'])

    # Default catch-all
    response('I’m not sure I understand. Could you try rephrasing?', ['default'], single_response=True)
    response('Hmm, I don’t know about that. Can you ask me something else?', ['confused'], single_response=True)

    response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])

    # Longer responses
    response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


# Testing the response system
while True:
    print('Bot: ' + get_response(input('You: ')))