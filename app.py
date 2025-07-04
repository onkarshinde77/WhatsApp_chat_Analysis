import streamlit as st
import numpy as np
from preprocess import preprocess
from helper import fetch_stats

st.sidebar.title("Whatsapp chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode('utf-8')
    data = preprocess(data)
    st.dataframe(data)
    
    user_list = data['sender'].unique()
    user_list.sort()
    np.insert(user_list,0,"All Users")
    
    selected_user = st.sidebar.selectbox("users",user_list) 
    
    if st.sidebar.button("Show Analysis"):
        
        num_message = fetch_stats(selected_user,data)
        col1,col2,col3,col4 = st.beta_columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_message)