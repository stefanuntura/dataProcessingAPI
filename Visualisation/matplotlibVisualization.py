from matplotlib import pyplot as plt
import matplotlib.style as style
import numpy as np
import requests
import json

plt.xkcd()


uri = "http://127.0.0.1:5000/accounts"

user = []
user_array = []
quotes = []
notes = []
events = []
sessions = []

response1 = requests.get(uri)
response = response1.json() 


for i in response:
    user.append(i['id'])
    user_array.append("User" + str(i['id']))



def get_answers(user_id, table, object_array):
    uri = "http://127.0.0.1:5000/" + table + "?id=" + str(user_id)
    response1 = requests.get(uri)
    response = response1.json()
    response1.close()
    if len(response) != 0:
        number = 0
        for y in response:
            number += 1
        object_array.append(number)
    else:
        object_array.append(0)

for x in user:
    get_answers(x, "quotes", quotes)


width = 0.5

x_indexes = np.arange(len(user_array))

plt.bar(x_indexes, quotes, width=width, color="#444444", label="Quotes")

plt.legend() 
plt.xticks(ticks=x_indexes, labels=user_array)
plt.title("Data Visualization")
plt.xlabel("User id")
plt.ylabel("User data")

plt.tight_layout()

plt.show()

