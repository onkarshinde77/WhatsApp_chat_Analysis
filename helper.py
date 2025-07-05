
def fetch_stats(selected_user,data):
    new_df = data
    if selected_user != 'All Users':
        new_df = data[data['sender'] == selected_user ]
    words=[]
    num = new_df.shape[0]
    for mess in new_df['messages']:
        words.extend(mess.split())
    return num,words