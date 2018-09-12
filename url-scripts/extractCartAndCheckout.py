import pandas
import os
from csv import writer as csvwriter
from csv import QUOTE_NONE
import re

directory = os.path.join("/Users/parveenarora/Documents/URL - Script/data")

for root,dirs,files in os.walk(directory):
    for file in files:
       if file.endswith(".csv"):
            reader = pandas.read_csv(file)
            action = reader['Action']
            avg = reader['Avg (ms)']
            with open('data.csv', 'a', newline='', encoding='utf-8', buffering=1) as csvoutfile:
                writer = csvwriter(csvoutfile, lineterminator='\n', delimiter=',', quotechar='"',
                                    escapechar='\\', doublequote=False, quoting=QUOTE_NONE, strict=True)
                writer.writerow([file, "**********************************"])
                index = 0
                for x in action:
                    try:
                        match = re.search(r"/cart|/checkout", x)
                        if match:
                            writer.writerow([x,avg[index]])
                    except:
                        print("failed")
                        #writer.writerow([x, "failed"])
                    index += 1
