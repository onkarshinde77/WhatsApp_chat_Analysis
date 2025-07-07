from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import numpy as np

def fetch_stats(selected_user,data):
    new_df = data
    if selected_user != 'All Users':
        new_df = data[data['sender'] == selected_user ]
    words=[]
    num = new_df.shape[0]
    for mess in new_df['messages']:
        words.extend(mess.split())
    # count media
    media = new_df[new_df['messages']=='<Media omitted>'].shape[0]
    # count links
    link_count = new_df[new_df['messages'].str.startswith("https://") | new_df['messages'].str.startswith("www.")].shape[0]

    return num,words,media, link_count


def active_user(data):
    active_users = data['sender'].value_counts()
    per = round((data['sender'].value_counts()/data.shape[0])*100,2).reset_index()
    per = per.rename(columns={'index':"name",'sender':'percentage'})
    per['percentage'] = per['percentage'].astype(str) + '%'
    return active_users,per

def create_wordcloud(selected_user,data):
    df = data[data['messages'] != '<Media omitted>' ]
    if selected_user != 'All Users':
        df = df[df['sender'] == selected_user]
    wc = WordCloud(width=300,height=300,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['messages'].str.cat(sep=" ")) 
    return df_wc

# ------------------------------------- Fuctions ------------------------------------------------------------

def count_word(word,data):
    count=0
    for i in data:
        if word== i:
            count+=1
    return count

def sort_(words):
    words=list(words)
    n = len(words)
    for i in range(n):
        for j in range(0, n - i - 1):
            if words[j][1] < words[j + 1][1]:
                words[j], words[j + 1] = words[j + 1], words[j]
    return words

def clean_word(str):
    char = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',':', ';', 
            '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
    str = str.lower().strip()
    st=""
    for i in str:
        if i in char:
            continue
        st+=i
    return st
        
# ------------------------------------------------------------------------------------------------------------

def count_max_word(selected_user,data):
    new_df = data[data['messages'] != '<Media omitted>' ]
    if selected_user != 'All Users':
        new_df = new_df[new_df['sender'] == selected_user ]
    
    stop_word = ["i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but",
                 "if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than",
                 "too","very","s","t","can","will","just","don","should","now","main", "mujhe", "mera", "meri", "hum", "hamara", "hamare", "tum", "tumhara", "tumhare","vah", "wo", "yah", "ye", "jo", "kaun", "kya", "kaise", "kahan", "kab", "kyon","hai", "hain", "tha", "the", "tha", "tha", "tha", "tha", "tha", "tha","aur", "lekin", "ya", "kyonki", "to", "yadi", "jab", "tak", "se", "par", "mein", "ka", "ki", "ke",
                "bhi", "na", "nahi", "is","media","omitted", "us", "un", "in", "unke", "apne", "apne", "apne","karna", "kiya", "kiye", "karte", "karta", "karti", "kar", "raha", "rahi", "rahe","hona", "hua", "hui", "hue", "hain", "hai", "tha", "the", "tha", "the","yahan", "wahan", "kahan", "kis", "kisi", "kuch", "sab", "sabhi", "kuch", "koi","1","2","3","4","5","6","7","8","9","0",'!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']

    words = []
    for mess in new_df['messages']:
        words.extend(mess.split())
    
    # # Filter out stop words
    filtered_words = [word for word in words if word.lower().strip() not in stop_word]
    
    # clean word(exclude * ' " ect )
    words = [clean_word(word) for word in filtered_words]
    
    # remove emoji
    words = [word for word in words if not any(emoji.is_emoji(char) for char in word)]
    # count words
    word_counts = Counter(words)
    
    # # Convert to list of (word, count) tuples
    max_repeat_word = [list(item) for item in word_counts.items()]

    # # Sort using your manual sort
    temp = sort_(max_repeat_word)
    temp = pd.DataFrame(temp, columns=['word', 'count'])
    temp = temp[temp['word'] != ""]
    return temp

def emoji_list(selected_user,data):
    new_df = data
    new_df = new_df[new_df['messages'] != '<Media omitted>' ]
    if selected_user != 'All Users':
        new_df = data[data['sender'] == selected_user ]
        
    emojis = []
    for message in new_df['messages']:
        emojis.extend([emj for emj in message.strip() if emoji.is_emoji(emj)])
    emojis = Counter(emojis)
    emojis = [list(item) for item in emojis.items()]
    emoji_ = pd.DataFrame(sort_(emojis))
    # emoji_['nor_num'] = 1/(1+ np.exp(-emoji_[1]))
    # bins = [0,10, 20, 30, 40, np.inf]
    # labels = ['10 <', '20 <', '30 <', '40 <', '40+']
    # emoji_['label'] = pd.cut(emoji_[1], bins=bins, labels=labels, right=True)

    return emoji_

def month_year(selected_user,data):
    new_df = data
    new_df = new_df[new_df['messages'] != '<Media omitted>' ]
    if selected_user != 'All Users':
        new_df = data[data['sender'] == selected_user ]
    timeline = new_df.groupby(['year','month_name']).count()['messages'].reset_index()
    timeline['month_year'] = timeline['month_name'] + "-" + timeline['year'].astype(str)
    # timeline=timeline.sort_values('month_year',ascending=False)
    return timeline
    
