import random
# from django.core.cache import cache
import openai

# print(random.randint(1,11))

# que_list= random.sample(range(1,53),53)
# que_list = [x for x in range(1,54)]
# # que_list.remove(9)
# # random.shuffle(que_list)
# print(que_list)

from decouple import config
openai.api_key = config("OPENAI_KEY")

def chatbot_response(user_input):
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


# print(chatbot_responsplain BST in 10 line?"))

for i in range(10):
    print(i,"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print(chatbot_response("Explain BST in 10 line?"))
    print("*************************************************************")

dict ={}
dict["key1"]="1"
dict["key2"]="2"
dict["key3"]="3"
dict["key4"]="4"

# print(dict)
# print(type(dict))




