from django.test import TestCase
import openai
# Create your tests here.
openai.api_key = ""
def chatbot_response(user_input):
    '''to give output from  CHATGPT'''
    response = openai.Completion.create(
        engine = "text-davinci-002",
        prompt = user_input,
        temperature = 0.5,
        max_tokens = 1024 ,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0
    )
    return response["choices"][0]["text"]


print(chatbot_response("What is 1 ?"))
