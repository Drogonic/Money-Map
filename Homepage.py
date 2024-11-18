import streamlit as st
import helpperFunctions
import DatabaseConnection as db_conn
#from streamlit_extras.app_logo import add_logo

# ADD DATABASE CALL HERE
helpperFunctions.hide_sidebar()
st.title("Money Map")

with st.form("Login"):
    st.write("Log in")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.form_submit_button("Login"):
        # Verify the user's credentials
        if db_conn.verify_user(username, password):
            st.success("Login successful!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.switch_page("pages/loggedinUserPage.py")
        else:
            st.error("Invalid username or password. Please try again.")

if st.button("Continue as Guest"):
    st.switch_page("pages/guestPage.py")
elif st.button("Signup"):
    st.switch_page("pages/signup.py")
st.info("If you choose to continue as a Guest your information will not be saved")