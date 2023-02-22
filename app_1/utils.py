import random 

def check(x):
    print("enter in utils")
    print(x)
    print()
    print(x[1].q_id)

    ques_list = list(x[i].q_id for i in range(0,10))
    print(ques_list)
    n=random.randint(1,30)
    while (n in ques_list):
        print("yes it is  present",n)
        n=random.randint(1,30)
    print("it is not present",n)