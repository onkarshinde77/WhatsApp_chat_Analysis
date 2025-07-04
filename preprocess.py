import numpy as np
import pandas as pd
import re

def preprocess(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s*[ap]m\s*-\s"
    message = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    data = pd.DataFrame({'messages':message,'dates':dates})
    data['dates'] = pd.to_datetime(data['dates'], format='%d/%m/%Y, %I:%M %p - ')
    data[['sender', 'messages']] = data['messages'].str.split(":", n=1, expand=True)
    data['sender'] = data['sender'].str.strip()
    data['messages'] = data['messages'].str.strip()
    # reorder the columns
    data = data[['sender', 'messages', 'dates']]
    data.dropna(inplace=True)
    
    data['dates'] = data['dates'].astype(str)
    data['year'] = data['dates'].str.split('-').str[0]
    data['month'] = data['dates'].str.split('-').str[1]
    
    data['day'] = data['dates'].str.split('-').str[2].str.split().str[0]
    data['time'] = data['dates'].str.split('-').str[2].str.split().str[1]
    data = data.drop('dates', axis=1)
    
    data['hour'] = data['time'].str.split(':').str[0]
    data['minute'] = data['time'].str.split(':').str[1]
    data['hour'] = data['hour'].astype(int)
    data['minute'] = data['minute'].astype(int)
    data = data.drop('time',axis=1)
    
    return data
