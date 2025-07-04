

def fetch_stats(selected_user,data):
    if selected_user == 'All Users':
        return data.shape[0]