import random
from django.core.cache import cache


# print(random.randint(1,11))

que_list= random.sample(range(1,11),10)
que_list.remove(9)
print(que_list)
