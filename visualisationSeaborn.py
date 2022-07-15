import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import requests
import datetime
import xml.etree.ElementTree as ET
import pandas as pd

# Graph showing the total sessions initiated for the individual weekdays and times of day 
# including two bar charts with marginal totals
# data imported in JSON format
def plotTotalSessions():
    yValues = []
    xValues = []
    accounts = requests.get("http://127.0.0.1:5000/accounts")
    accounts = accounts.json()

    for account in accounts:
        sessions = requests.get("http://127.0.0.1:5000/sessions?id=" + str(account["id"]))
        sessions = sessions.json()
        for session in sessions:
            if(session["date"].find("-") != -1):
                splitDate = session["date"].split("-")
                year = int(splitDate[0])
                month = int(splitDate[1])
                day = int(splitDate[2])
                x = datetime.datetime(year, month, day, 0, 0, 0, 0).weekday()
                y = int(session["time"].split(":")[0])
                xValues.append(x)
                yValues.append(y)
            elif(session["date"].find("/") != -1):
                splitDate = session["date"].split("/")
                year = int(splitDate[2])
                month = int(splitDate[1])
                day = int(splitDate[0])
                x = datetime.datetime(year, month, day, 0, 0, 0, 0).weekday()
                y = int(session["time"].split(":")[0])
                xValues.append(x)
                yValues.append(y)
    xValues.append(7)
    yValues.append(15)

    sns.set_theme(style="darkgrid")

    # rs = np.random.RandomState(9) 
    data = [xValues,yValues]

    graph = sns.jointplot( x=yValues, y=xValues, kind="hist", color="#4CB391", binwidth = 1, space = 0.2, height = 6, marginal_kws=dict(bins=(24), fill=True), marginal_ticks = True)

    # axis limits
    graph.ax_marg_x.set_xlim(0,24)
    graph.ax_marg_y.set_ylim(7,1)

    # axis labels
    graph.ax_joint.set_xlabel('Time', fontweight='bold')
    graph.ax_joint.set_ylabel('Weekdays', fontweight='bold')

    # window/graph size
    graph.fig.set_figwidth(14)
    graph.fig.set_figheight(6)

    # graph.ax_joint.set_aspect('equal')  # equal aspect ratio

    # Graph title
    graph.fig.suptitle("Total Sessions by Weekday and Time", fontsize = 13, fontweight = "bold")
    graph.fig.subplots_adjust(top=0.9)

    # set ticks per axis
    graph.ax_joint.set_yticks([0,1,2,3,4,5,6,7])
    graph.ax_joint.set_xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])

    # set tick labels
    graph.ax_joint.set_yticklabels(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday', ''])
    graph.ax_joint.set_xticklabels(['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'], fontsize  = 10)

    plt.show()

def getMin(collection):
        if(len(collection) <= 0):
            return -1
        min = collection[0]
        for i in range(0, len(collection)):
            if collection[i] < min:
                min = collection[i]
        return min

def getMax(collection):
    if(len(collection) <= 0):
        return -1
    max = collection[0]
    for i in range(0, len(collection)):
        if collection[i] > max:
            max = collection[i]
    return max

def monthToMonthName(month, data):
    if(month < 1 or month > 12):
        return "Unknown"
    monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return monthNames[month - 1]

def addData(elem, data):
    dateComponents = elem.text.split("-")
    year = dateComponents[0]
    month = dateComponents[1]
    if year not in data:
        data[year] = {}
        for i in range(1, 13):
            data[year][i] = 0
    data[year][int(month)] += 1

def xmlGraph():
  
    months = []
    years = []
    values = []
    data = {}

    # read session data
    sessionTree = ET.parse("SessionsXML.xml")
    sessions = sessionTree.getroot()
    for elem in sessionTree.iter():
        if(elem.tag == "date"):
            addData(elem, data)

    # read event data
    eventTree = ET.parse("EventsXML.xml")
    events = eventTree.getroot()
    for elem in eventTree.iter():
        if(elem.tag == "date"):
            addData(elem, data)

    # evaluate the collected data
    for year, currentMonths in data.items():
        for i in range(0, 12):
            years.append(int(year))
        for month, value in currentMonths.items():
            months.append(monthToMonthName(month, data))
            values.append(value)
        
    # convert the data into the required structure
    df = pd.DataFrame({
        'years': years,
        'months': months,
        'values': values
    })

    # print(years)
    # print(months)
    # print(values)

    minYear = getMin(years)
    maxYear = getMax(years)
        
    graph = sns.relplot(data=df, x="years", y="values", hue="months", kind="line")

    # Set ticks to match displayed years
    graph.set(xticks=np.arange(minYear, maxYear+1))
    # Set descriptions
    graph.set_xlabels("Years", fontsize = 10, fontweight = "bold")
    graph.set_ylabels("Activity (Sessions + Events)", fontsize = 10, fontweight = "bold")
    graph.fig.suptitle("User Activity per month and year", fontsize = 14, fontweight = "bold")
    graph.fig.subplots_adjust(top=0.9)

    plt.show()

plotTotalSessions()
xmlGraph()