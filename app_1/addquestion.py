questions = [
    {"question": "What is 10 + 5?", "options": ["13", "14", "15", "16"], "answer": "15"},
    {"question": "What is 20 - 8?", "options": ["10", "12", "14", "16"], "answer": "12"},
    {"question": "What is 15 + 12?", "options": ["25", "27", "29", "31"], "answer": "27"},
    {"question": "What is 40 - 7?", "options": ["28", "31", "33", "37"], "answer": "33"},
    {"question": "What is 18 + 14?", "options": ["30", "32", "36", "38"], "answer": "32"},
    {"question": "What is 30 - 12?", "options": ["16", "18", "20", "22"], "answer": "18"},
    {"question": "What is 25 + 7?", "options": ["29", "30", "31", "32"], "answer": "32"},
    {"question": "What is 17 - 6?", "options": ["9", "10", "11", "12"], "answer": "11"},
    {"question": "What is 42 + 8?", "options": ["49", "50", "51", "52"], "answer": "50"},
    {"question": "What is 23 - 14?", "options": ["7", "8", "9", "10"], "answer": "9"},
    {"question": "What is 56 + 7?", "options": ["61", "62", "63", "64"], "answer": "63"},
    {"question": "What is 40 - 15?", "options": ["20", "22", "24", "25"], "answer": "25"},
    {"question": "What is 35 + 12?", "options": ["44", "46", "47", "50"], "answer": "47"},
    {"question": "What is 65 - 14?", "options": ["43", "48", "51", "56"], "answer": "51"},
    {"question": "What is 80 + 9?", "options": ["86", "87", "88", "89"], "answer": "89"},
    {"question": "What is 24 - 9?", "options": ["12", "14", "15", "16"], "answer": "15"},
    {"question": "What is 52 + 18?", "options": ["68", "70", "72", "74"], "answer": "70"},
    {"question": "What is 39 - 12?", "options": ["23", "25", "27", "29"], "answer": "27"},
    {"question": "What is 73 + 6?", "options": ["78", "79", "80", "81"], "answer": "79"},
    {"question": "What is 28 - 7?", "options": ["19", "20", "21", "22"], "answer": "21"},
    {"question": "What is 45 + 13?", "options": ["56", "58", "60", "62"], "answer": "58"},
    {"question": "What is 5 + 7?", "options": ["10", "11", "12", "13"], "answer": "12"},
    {"question": "What is 8 - 3?", "options": ["3", "5", "8", "11"], "answer": "5"},
    {"question": "What is 4 + 2?", "options": ["3", "5", "6", "7"], "answer": "6"},
    {"question": "What is 9 - 4?", "options": ["3", "5", "6", "7"], "answer": "5"},
    {"question": "What is 6 + 9?", "options": ["12", "13", "14", "15"], "answer": "15"},
    {"question": "What is 11 - 8?", "options": ["1", "2", "3", "4"], "answer": "3"},
    {"question": "What is 7 + 5?", "options": ["10", "11", "12", "13"], "answer": "12"},
    {"question": "What is 10 - 2?", "options": ["6", "7", "8", "9"], "answer": "8"},
    {"question": "What is 8 + 4?", "options": ["10", "11", "12", "13"], "answer": "12"},
    {"question": "What is 12 - 5?", "options": ["5", "6", "7", "8"], "answer": "7"},
    {"question": "What is 6 + 7?", "options": ["11", "12", "13", "14"], "answer": "13"},
    {"question": "What is 15 - 6?", "options": ["6", "7", "8", "9"], "answer": "9"},
    {"question": "What is 3 + 9?", "options": ["10", "11", "12", "13"], "answer": "12"},
    {"question": "What is 11 - 7?", "options": ["2", "3", "4", "5"], "answer": "4"},
    {"question": "What is 9 + 5?", "options": ["12", "13", "14", "15"], "answer": "14"},
    {"question": "What is 13 - 8?", "options": ["4", "5", "6", "7"], "answer": "5"},
    {"question": "What is 8 + 6?", "options": ["12", "13", "14", "15"], "answer": "14"},
    {"question": "What is 14 - 3?", "options": ["10", "11", "12", "13"], "answer": "11"},
    {"question": "What is 6 + 8?", "options": ["12", "13", "14", "15"], "answer": "14"},
    {"question": "What is 10 - 3?", "options": ["5", "6", "7", "8"], "answer": "7"},
    {"question": "What is 9 + 7?", "options": ["14", "15", "16", "17"], "answer": "16"},
]

from .models import *
def add():
    # for i in questions:
    # i=[{"question": "What is 9 + 7?", "options": ["14", "15", "16", "17"], "answer": "16"}]
    # print(s)
    # print(s[0]["question"])
    # print(s[0]["options"][0])
    num = 11
    for s in questions:
        q=Question(questionID=num,questionText=s["question"],questionOption1=s["options"][0],questionOption2=s["options"][1],questionOption3=s["options"][2],questionOption4=s["options"][3],questionAnswer=int(s["answer"]))
        print(q)
        q.save()
        num+=1

def changeOPtion():
    num = 11
    # i=[{"question": "What is 9 + 7?", "options": ["14", "15", "16", "17"], "answer": "16"}]

    for s in questions:
        q=Question.objects.get(questionID=num)
        q.questionAnswer = int(s["options"].index(s["answer"])) + 1
        print(q)
        q.save()
        num+=1


# questionID = models.IntegerField(unique=True,primary_key=True)
#     questionText = models.TextField()
#     questionOption1 = models.TextField()
#     questionOption2 = models.TextField()
#     questionOption3 = models.TextField()
#     questionOption4 = models.TextField()
#     questionAnswer = models.IntegerField()