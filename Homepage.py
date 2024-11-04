import streamlit as st
import helpperFunctions

helpperFunctions.hide_sidebar()
with st.form("Login"):
    st.write("Log in")
    username = st.text_input("Username")
    password = st.text_input("Username", type="password")

    submitted = st.form_submit_button("Login")
    if submitted:
        st.write("Login")

if st.button("Guest Login"):
    st.switch_page("pages/guestPage.py")
elif st.button("Signup"):
    st.switch_page("pages/signup.py")
