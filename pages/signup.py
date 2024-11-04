import streamlit as st
import helpperFunctions

helpperFunctions.hide_sidebar()
# we have to implement a check in the future for those that enter a matching user or email to an already created account
with st.form("Signup"):
    st.write("Create Account")
    username = st.text_input("Username")
    password = st.text_input("Username", type="password")
    email = st.text_input("Email")
    if st.form_submit_button("Create Account"):
        if username is None or password is None or email is None:
            st.error("Must provide Information")
        else:
            st.write("Account created successfully!")
            st.session_state['create_account'] = True
if st.button("Return to Log-in Page"):
    st.switch_page("Homepage.py")
