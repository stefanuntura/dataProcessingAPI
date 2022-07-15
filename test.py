import xml.etree.ElementTree as ET
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

tree = ET.parse("SessionsXML.xml")
sessions = tree.getroot()

months = []
years = []
values = []

df = pd.DataFrame({
    'years': [2011, 2011, 2011, 2011, 2011, 2011, 2011, 2011, 2011, 2011, 2011, 2011, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012],
    'months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'values': [1,2,3,4,5,6,7,8,9,10,11,12,12,11,10,9,8,7,6,5,4,3,2,1]
})

test = []

for elem in tree.iter():
    if(elem.tag == "date"):
        dateComponents = elem.text.split("-")
        months.append(dateComponents[1])
        years.append(dateComponents[0])
        values.append(dateComponents[1])
        # test.append()

data = [years, months, values]

graph = sns.relplot(data=df, x="years", y="months", hue="values", kind="line")
graph.set(xticks=np.arange(2011,2013))

plt.show()