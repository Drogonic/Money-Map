import streamlit as st
import helpperFunctions
from streamlit_extras.app_logo import add_logo

# ADD DATABASE CALL HERE
helpperFunctions.hide_sidebar()
st.title("Money Map")
with st.form("Login"):
    st.write("Log in")
    username = st.text_input("Username")
    password = st.text_input("Username", type="password")

    if st.form_submit_button("Login"):
        st.switch_page("pages/loggedinUserPage.py")

if st.button("Guest Login"):
    st.switch_page("pages/guestPage.py")
elif st.button("Signup"):
    st.switch_page("pages/signup.py")
