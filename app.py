import streamlit as st
import numpy as np
from functions.preprocess import preprocess
from functions.helper import fetch_stats , active_user , create_wordcloud,count_max_word , emoji_list,month_year
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
# uploaded_file = open('chats/chat.txt','r',encoding='utf-8').read()

if uploaded_file is not None:
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode('utf-8')
    # data = uploaded_file
    data = preprocess(data)
    st.dataframe(data)
    
    user_list = data['sender'].unique()
    user_list.sort()
    user_list = np.insert(user_list,0,"All Users")
    selected_user = st.sidebar.selectbox("users",user_list)
    
    if st.sidebar.button("Show Analysis"):
        
        num_message,words,media_count,link_count = fetch_stats(selected_user,data)
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_message)
        with col2:
            st.header("Total Words")
            st.title(len(words))
        with col3:
            st.header("Total Media")
            st.header(media_count)
        with col4:
            st.header("Total Links")
            st.title(link_count)
            
        if selected_user == "All Users":
            st.title("Most Active Users")
            X,active_percentage = active_user(data)
            fig , ax = plt.subplots()
            col1,col2 = st.columns(2)
            with col1:
                ax.bar(X.index,X.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(active_percentage)
        # wordcloud
        df_wc = create_wordcloud(selected_user,data)
        fig ,ax = plt.subplots()
        st.title("Most use words")
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        # max word
        st.title("Most used word")
        col1,col2 = st.columns(2)
        max_word = count_max_word(selected_user,data)
        with col1: 
            st.write(max_word.head(10))
            # st.write(max_word.shape)
        with col2:
            fig ,ax = plt.subplots()
            ax.barh(max_word['word'].head(10),max_word['count'].head(10))
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        st.title("Most used emojis")
        col1,col2 = st.columns(2)
        emoji_ = emoji_list(selected_user,data)
        with col1:
            st.dataframe(emoji_)
        with col2:
            fig ,ax = plt.subplots()
            try:
                ax.barh(emoji_[0], emoji_[1], color='skyblue')
                st.pyplot(fig)
            except Exception as e:
                st.write("Does not contain emoji")

            
        st.title('Message Frequency by month')
        timeline = month_year(selected_user,data)
        if timeline.shape[0]<2:
            st.dataframe(timeline[["month_year",'messages']])
        else:
            fig ,ax = plt.subplots()
            ax.plot(timeline['month_year'],timeline['messages'], color='red')
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

