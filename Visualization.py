from matplotlib import pyplot as plt
import matplotlib.style as style
import numpy as np
import appRestApi as mainApi
import requests
import json
# Line plot/ graphs
# plt.style.use('fivethirtyeight')
plt.xkcd()


uri = "http://127.0.0.1:5000/accounts"

user = []
user_array = []
quotes = []
notes = []
events = []
sessions = []

response = requests.get(uri).json() # list type

for i in response:
    user.append(i['id'])
    user_array.append("User" + str(i['id']))

def get_answers(user_id, table, object_array):
    uri = "http://127.0.0.1:5000/" + table + "?id=" + str(user_id)
    response = requests.get(uri).json()
    if len(response) != 0:
        number = 0
        for y in response:
            number += 1
        object_array.append(number)
    else:
        object_array.append(0)


for x in user:
    get_answers(x, "quotes", quotes)
    get_answers(x, "notes", notes)
    get_answers(x, "events", events)
    get_answers(x, "sessions", sessions)

width = 0.2

x_indexes = np.arange(len(user_array))

plt.bar(x_indexes - width, quotes, width=width, color="#444444", label="Quotes")
plt.bar(x_indexes, notes, width=width, color="#008fd5", label="Notes")
plt.bar(x_indexes + width, events, width=width, color="#e5ae38", label="Events")
plt.bar(x_indexes + width + width, sessions, width=width, color="red", label="Sessions")

plt.legend() 
plt.xticks(ticks=x_indexes, labels=user_array)
plt.title("Data Visualization")
plt.xlabel("User id")
plt.ylabel("User data")

plt.tight_layout()

plt.show()

# plt.xticks((1,2,3,4,5), ('h','e','l','l','o'))


# plt.plot(x, y)
# plt.legend()
# plt.grid(True, color='b')
# plt.tight_layout()
# plt.plot(x, y, 'k-.')
# plt.plot(x, y, color="red", linestyle='--', marker='o', linewidth='2', label='sons of bitches')
# plt.savefig('plot.png')
# plt.show()

# Scatter plot
# plt.scatter(s=25)

# Bar chart
# plt.bar()

# Histogram
# x = [25, 26, 15]
# y = [0, 10, 20, 30]
# plt.hist(x, y, histtype='bar', rwidth=0.8)
# plt.hist(x)
# plt.show()

# Stack plot
# days = [1,2,3,4,5]
# sleeping = [7,8,6,11,7]
# eating = [2,3,4,3,2]
# working = [7,8,7,2,2]
# playing = [8,5,7,8,13]
# plt.plot([],[], color='m', label='Sleeping', linewidth=5)
# plt.plot([],[], color='c', label='Eating', linewidth=5)
# plt.plot([],[], color='r', label='Working', linewidth=5)
# plt.plot([],[], color='k', label='Playing', linewidth=5)
# plt.stackplot(days, eating, sleeping, working, playing, colors=['m','c','r','k'])

# Pie chart
# slices = [7,2,2,13]
# activities = ['Sleeping', 'eating', 'working', 'playing']
# cols = ['c','m','r','b']
# plt.pie(slices,
#         labels=activities,
#         wedgeprops={'edgecolor': 'black'},
#         colors=cols,
#         startangle=90,
#         shadow = True,
#         explode=(0,0,1,0,0)
#         autopct='%1.1f%%')