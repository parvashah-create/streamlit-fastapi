import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3
import os
from Functions.endpoints import request_geos_by_path, request_geos_download_by_name,request_nexrad_by_path,request_nexrad_download_by_name

def get_db(db):
    # eastablish connection with db
    db_path = os.getcwd() + "/database/{}".format(db)
    print(db_path)
    conn = sqlite3.connect(db_path,check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor


def geos_search_by_path(username):
    con, cursor = get_db("meta_data.db")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        station_val = cursor.execute("SELECT DISTINCT station FROM geos")
        station = st.selectbox(
            'Which Station ?',
            [i[0] for i in station_val]            
            )
        
    with col2:
        year_val = cursor.execute("SELECT DISTINCT year FROM geos WHERE station = '{}' ".format(station))
        year = st.selectbox(
            'What Year ?',
            [i[0] for i in year_val],
        )
    with col3:
        day_val = cursor.execute("SELECT DISTINCT day FROM geos WHERE station = '{}' AND year = '{}'".format(station,year))
        day = st.selectbox(
            'What Day ?',
            [i[0] for i in day_val],
        )
    with col4:
        hour_val = cursor.execute("SELECT DISTINCT hour FROM geos WHERE station = '{}' AND year = '{}' AND day = '{}'".format(station,year,day))
        hour = st.selectbox(
            'What Hour ?',
            [i[0] for i in hour_val],
        )

    
    response = request_geos_by_path(username,station,year,day,hour)
    if response != None:
        df_list = [i["noaa-goes18"] for i in response]
    else:
        df_list=["Rate Limit Exceeded"]
    file = st.selectbox(
            'Select file to download',
            df_list,
            key = "filename"
        )

    st.write("You selected:", file)
    download_btn = st.button("Download File")
    if 'log_df' not in st.session_state:
        st.session_state['log_df'] = pd.DataFrame(columns=['filename','time'])

    if download_btn:
        try:
            response = request_geos_download_by_name(username,file) #<------ Endpoint
            link = response['link']
            st.write(f"link: {link}")
            st.session_state['log_df'] = st.session_state['log_df'].append({'filename':file,'time':datetime.now()},ignore_index=True)
        except:
            pass
    st.dataframe(st.session_state['log_df'])
    con.close()

# this function displays input_boxes for search by filename method
def geos_search_by_filename(username):
    filename_input = st.text_input(
        "Enter filename 👇",
        placeholder="File Name",
    )
    download_btn = st.button("Download File")
    if 'log_df' not in st.session_state:
        st.session_state['log_df'] = pd.DataFrame(columns=['filename','time'])

    if download_btn:
        try:
            response = request_geos_download_by_name(username,filename_input) #<------ Endpoint
            print(response)
            link = response['link']
            st.write(f"link: {link}")
            st.session_state['log_df'] = st.session_state['log_df'].append({'filename':filename_input,'time':datetime.now()},ignore_index=True)
            
        except:
            pass
    st.dataframe(st.session_state['log_df'])


def nexrad_search_by_path(username):

    con, cursor = get_db("meta_data.db")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        year_val = cursor.execute("SELECT DISTINCT year FROM nexrad")
        year = st.selectbox(
            'Which Year ?',
            [i[0] for i in year_val]
            )

    with col2:
        month_val = cursor.execute("SELECT DISTINCT month FROM nexrad WHERE year = '{}' ".format(year))
        month = st.selectbox(
            'What Month ?',
            [i[0] for i in month_val]
        )
    with col3:
        day_val = cursor.execute("SELECT DISTINCT day FROM nexrad WHERE year = '{}' AND month = '{}'".format(year,month))
        day = st.selectbox(
            'What Day ?',
            [i[0] for i in day_val]
        )
    with col4:
        station_val = cursor.execute("SELECT DISTINCT station FROM nexrad WHERE year = '{}' AND month = '{}' AND day = '{}'".format(year,month,day))
        station = st.selectbox(
            'Which Station ?',
            [i[0] for i in station_val]
        )
    response = request_nexrad_by_path(username,year,month,day,station)
    if response != None:
        df_list = [i["noaa-nexrad-level2"] for i in response]
    else:
        df_list=["Rate Limit Exceeded"]
    
    file = st.selectbox(
            'Select file to download',
            df_list,
            key = "filename"
        )

    st.write("You selected:", file)
    download_btn = st.button("Download File")
    if 'log_df' not in st.session_state:
        st.session_state['log_df'] = pd.DataFrame(columns=['filename','time'])

    if download_btn:
        try:
            response = request_nexrad_download_by_name(username,file) #<------ Endpoint
            link = response['link']
            st.write(f"link: {link}")
            st.session_state['log_df'] = st.session_state['log_df'].append({'filename':file,'time':datetime.now()},ignore_index=True)
        except:
            pass
    st.dataframe(st.session_state['log_df'])
    con.close()


# this function displays input_boxes for search by file path method      
def nexrad_search_by_filename(username):

    filename_input = st.text_input(
        "Enter filename 👇",
        placeholder="File Name",
    )
    download_btn = st.button("Download File")
    if 'log_df' not in st.session_state:
        st.session_state['log_df'] = pd.DataFrame(columns=['filename','time'])

    if download_btn:
        try:
            response = request_nexrad_download_by_name(username,filename_input) #<------ Endpoint
            link = response['link']
            st.write(f"link: {link}")
            st.session_state['log_df'] = st.session_state['log_df'].append({'filename':filename_input,'time':datetime.now()},ignore_index=True)
        except:
            pass
    st.dataframe(st.session_state['log_df'])
