import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Replace with your API endpoint


def get_api_data(username):
    host = "http://54.210.90.102:8000" 
    endpoint = f"/get-admin-data/{username}"
    url = host + endpoint
    response = requests.get(url)
    if response.status_code == 400:
        endpoint = f"/get-user-data/{username}"
        url = host + endpoint
        response = requests.get(url)
  
    if response.status_code == 200:
        admin_data = response.json()
        df = pd.read_json(admin_data,lines=True)
        return df
    


def get_prev_day_data(df):
    prev_day = pd.Timestamp.now().normalize() - pd.Timedelta(days=1)
    return df[df['timestamp'].dt.normalize() == prev_day]


def get_last_week_data(df):
    last_week = pd.Timestamp.now().normalize() - pd.Timedelta(days=7)
    return df[df['timestamp'].dt.normalize() >= last_week]


def get_user_count_data(df):
    return df.groupby(['username', pd.Grouper(key='timestamp', freq='1D')])['endpoint'].count().reset_index()


def get_endpoint_count_data(df):
    return df.groupby('endpoint')['username'].count().reset_index()


def get_success_failed_data(df):
    success = df[df['call_status'].between(200,299,inclusive="both")].shape[0]
    failed = df[df['call_status'] >= 300].shape[0]
    return success, failed


def main(username):
    # Load data from API
    df = get_api_data(username)
    if df != None:
        # Calculate metrics
        prev_day_data = get_prev_day_data(df)
        prev_day_total_calls = prev_day_data.shape[0]
        last_week_data = get_last_week_data(df)
        last_week_avg_calls = last_week_data.shape[0] / 7
        user_count_data = get_user_count_data(df)
        endpoint_count_data = get_endpoint_count_data(df)
        success, failed = get_success_failed_data(df)



        st.title('User Activity Dashboard')
        st.subheader(f"Username: {username}")
        st.write(
            "Welcome to the User Activity Dashboard. This dashboard provides insights into user activity on your platform.")
        
        # Display total API calls the previous day
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Total API calls (previous day)')
            st.metric('API Calls', prev_day_total_calls)

        # Display total average calls during the last week
        with col2:
            st.subheader('Total average calls (last week)')
            st.metric('Average Calls', last_week_avg_calls)

        # Display success and failed request calls
        col3, col4 = st.columns(2)
        with col3:
            st.subheader('Success vs. Failed Requests')
            st.metric('Success', success)
            st.metric('Failed', failed)
        with col4:
            pass
        

        # Display each endpoint total number of calls
        st.subheader('Endpoint Calls')
        fig1 = px.bar(endpoint_count_data, x='endpoint', y='username', labels={'username': 'Call Count'})
        st.plotly_chart(fig1)

        # Display count of request by each user against time
        st.subheader('User Activity Over Time')
        fig2 = px.line(user_count_data, x='timestamp', y='endpoint', color='username', title='User Activity Over Time')
        fig2.update_layout(xaxis_title='Date', yaxis_title='Call Count', legend_title='User ID')
        st.plotly_chart(fig2)
    st.title('User has no activity yet!')
