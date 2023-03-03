import requests
import streamlit as st
import pandas as pd

host_link = "http://127.0.0.1:8000"


def register_request(name,username,password,plan):
    endpoint = "/register"
    url = host_link + endpoint
    payload = {
        "name": name,
        "username": username,
        "password": password,
        "plan": plan
    }

    response = requests.post(url, json=payload)
    if response.status_code == 400:
        st.sidebar.error("username taken, enter other username")
    else:
        st.sidebar.success("User Registration Successful! Please login to continue...")
       
def login_request(username,password):
    endpoint = "/login"
    url = host_link + endpoint
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=payload)
    if response.status_code == 400:
        st.sidebar.error('Invalid username and/or password')
        return None
    else:
        st.sidebar.success(f"{username} successfully loggedIn")
        return True
def change_password_request(username,current_password,new_password):
    endpoint = "/change-password"
    url = host_link + endpoint
    payload = {
        "username": username,
        "current_password": current_password,
        "new_password": new_password
    }
    response = requests.post(url, json=payload)
    if response.status_code == 400:
        st.sidebar.error('Invalid username and/or password')
    if response.status_code == 401:
        st.sidebar.error('Token has expired, log in again!')
    else:
        st.sidebar.success(f"{username}, successfully changed password")


def request_geos_by_path(username,station,year,day,hour):
    endpoint = f"/geos-get-by-path/{username}/{station}/{year}/{day}/{hour}"
    url = host_link + endpoint
    response = requests.get(url)
    if response.status_code == 400:
        st.error('path parameters not valid')
    if response.status_code == 401:
        st.error('Token has expired, log in again!')
    if response.status_code == 429:
        st.error('API rate limit exceeded! upgrade plan to continue')
    else:
        return response.json()

def request_nexrad_by_path(username,year,month,day,station):
    endpoint = f"/nexrad-get-by-path/{username}/{year}/{month}/{day}/{station}"
    url = host_link + endpoint
    response = requests.get(url)
    if response.status_code == 400:
        st.error('path parameters not valid')
    if response.status_code == 401:
        st.error('Token has expired, log in again!')
    if response.status_code == 429:
        st.error('API rate limit exceeded! upgrade plan to continue')
    else:
        return response.json()

def request_geos_download_by_name(username,filename):
    endpoint = f"/geos-download-by-name/{username}/{filename}"
    url = host_link + endpoint
    response = requests.get(url)
    if response.status_code == 400:
        st.error('Filename not valid')
    if response.status_code == 401:
        st.error('Token has expired, log in again!')
    if response.status_code == 429:
        st.error('API rate limit exceeded! upgrade plan to continue')
    else:
        return response.json()


def request_nexrad_download_by_name(username,filename):
    endpoint = f"/nexrad-download-by-name/{username}/{filename}"
    url = host_link + endpoint
    response = requests.get(url)
    if response.status_code == 400:
        st.error('Filename not valid')
    if response.status_code == 401:
        st.error('Token has expired, log in again!')
    if response.status_code == 429:
        st.error('API rate limit exceeded! upgrade plan to continue')
    else:
        return response.json()
