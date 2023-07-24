import requests
import json
import time

def ask_claude(question, conversation_id=''):
    '''

    Args:
        question: the question that you want to ask
        conversation_id: if not none, the conversation will continuously happen in a single chat box.
                        if none, we start a new chat box each time

    Returns:
    '''

    url = "" # the url that can be retrieved from laf after deploy the claude

    # Define the parameters of request
    params = {
        "question": question,
        "conversationId": conversation_id
    }

    # request to claude
    response = requests.get(url, params=params)
    # time.sleep(15)

    # If the request was successful, print the result
    if response.status_code == 200:
        result = response.json()
        # these two parameters should be identical to those in laf settings
        answer = result["Answer"]
        conv_id = result["ID"]
        return answer, conv_id
    else:
        print("Request failed with status code", response.status_code)
        return None


# start the conversation
answer, conv_id = ask_claude("hi")
print(answer)

# start training
question = "I have a fuzzy-matching results, and need to further check whether the fuzzy matching pairs are correct (i.e., true match). And I need to do this work manually, since programming cannot figure out a pattern." \
           "I will provide you some examples (that I've already checked manually), and please learn from the example, and help me identify several samples that has not been checked." \
           "1st example: fasani matteo	fasani matteo	&  mta  	mta s p a --> this is a true match (the first two are individual names, the last two are company names. A pair is true match if and only if the individual name and company names are matched)" \
           "2nd example: sola a	a s	&   fiat	  fiat group (also true match, this is because some might only give their first initial instead of full name)" \
           "3rd example: marconi stefano	micco stefano	& ferrari	ferrari spa (this is not true)" \
           "Please identify, whether the following matching pair is true: giuseppe civardi	giuseppe civeli	 & fiat auto	 fiat"

answer, conv_id = ask_claude(question, conv_id)
print(answer)

question_2 = "based on your previous learning, please identify whether the following matching pair is true: ryan mei    ryan mei & apple    amazon. " \
             "This time, please just return 1 if this is a true match, 0 if this is the wrong match, and 2 if you can not determine whether this is true or not."

answer_2, conv_id = ask_claude(question_2, conv_id)
print(answer_2)
