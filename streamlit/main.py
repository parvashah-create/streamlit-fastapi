import streamlit as st

import pandas as pd
from streamlit_option_menu import option_menu
from Functions.streamlitFunctions import geos_search_by_path,geos_search_by_filename, nexrad_search_by_path,nexrad_search_by_filename
from Functions.endpoints import register_request,login_request,change_password_request
from Functions.dashboard import main
import plotly.graph_objects as go

      

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)




# Sidebar forms
with st.sidebar:
    # options menu  
    selected = option_menu("Menu", ["Log In", 'Sign Up', 'Change Password'], 
        icons=['box-arrow-in-right', 'plus-circle','lock'], menu_icon="menu-up", default_index=0)
    
    # log in form
    if 'login' not in st.session_state:
        st.session_state['login'] = False

   


    if selected == "Log In":
        
        st.write('## Log In')
        login_username = st.text_input('Username')
        login_password = st.text_input('Password', type='password')
        # authentication status update
        if st.button('Log In!'):
            # send login request 
            st.session_state['login'] = login_request(login_username,login_password)

        if st.session_state['login'] == True:
            if st.button("Logout"):
                st.session_state['login'] = False

    # Sign-up form 
    if selected == "Sign Up":
        st.write('## Sign up')
        name = st.text_input('Name')
        username = st.text_input('Username',key='signup_username')
        plan = st.selectbox(
                    "Select Plan",
                ["free", "gold","platinum"]
                )

        password = st.text_input('Password', type='password',key='signup_pass')
        confirm_password = st.text_input('Confirm Password', type='password')

        
        if st.button('Sign up'):
            if password != confirm_password:
                st.write("Passwords don't Match!")
            else:
                # send register request 
                register_request(name,username,password,plan)

    if selected == "Change Password":
        st.write('## Change Password')
        fp_username = st.text_input('Username',key='Fp_username')
        fp_old_password = st.text_input('Current Password')
        fp_new_password = st.text_input('New Password')
        if st.button('Change Password'):
            # send change password request
            change_password_request(fp_username,fp_old_password,fp_new_password)  


if  st.session_state['login']!= True:
    st.write("# Welcome! 👋")
    st.markdown(
            """
            # Assignment 1
            ## Team 14
            - Parva Shah 
            - Dev Shah
            - Harsh Shah

            This streamlit app has 3 pages:
            - 1_🛰_Geos_Data_Downloader:

                There are ywo methods to download a file:
                - Download by Path:
                User select the path and all files located on that path is displayed. The user can then select a file to download
                - Download by Filename:
                User writes the filename in the input box and a download link for the same is displayed.

            - 2_📡_Nexrad_Data_Downloader
            
                There are ywo methods to download a file:
                - Download by Path:
                User select the path and all files located on that path is displayed. The user can then select a file to download
                - Download by Filename:
                User writes the filename in the input box and a download link for the same is displayed.

            - 3_📍_NexRad_Locations
                This plots the Nexrad locations on the US map

        """
        )



if st.session_state['login']==True:
    
    # --- OPTION MENU ----
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "GEOS", "NexRad", "Locations"],
        icons=["house-door", "rocket", "airplane", "geo-fill"],
        default_index=0,
        orientation="horizontal"
    )
    if selected == "Dashboard":
        
        main(login_username)

    if selected == "GEOS":
        st.write("# GEOS Satellite Data Downloader 🛰")
        search_method = st.selectbox(
            "Select Search Method",
            ["Search by Filename", "Search by Path"]
        )

        if search_method == "Search by Path":
            geos_search_by_path(login_username)
        if search_method == "Search by Filename":
            geos_search_by_filename(login_username)

    if selected == "NexRad":
        st.write("# NexRad Data Downloader 📡")
        search_method = st.selectbox(
            "Select Search Method",
            ["Search by Filename", "Search by Path"]
        )

        if search_method == "Search by Path":
            nexrad_search_by_path(login_username)
        if search_method == "Search by Filename":
            nexrad_search_by_filename(login_username)

    if selected == "Locations":
        st.write("# Nexrad Locations in USA 📍")
        # filename issue
        df = pd.read_csv('./database/nexrad_loc.csv')
        df['text'] = 'City: ' + df['City'] + ', ' + 'State: ' + df["State"] + ', ' + 'Identifier: ' + df[
            'ICAO Location Identifier'].astype(str)

        fig = go.Figure(data=go.Scattergeo(
            lon=df['Long'],
            lat=df['Lat'],
            text=df['text'],
            mode='markers',
        ))

        fig.update_layout(
            title='NexRad Locations',
            geo_scope='usa',
            geo=dict(bgcolor='rgba(0,0,0,0)',
                     lakecolor='#4E5D6C',
                     landcolor='rgba(51,17,0,0.2)',
                     subunitcolor='grey'),

        )
        st.plotly_chart(fig, use_container_width=True)

