import streamlit as st
import helpperFunctions
import DatabaseConnection as db_conn
#from streamlit_extras.app_logo import add_logo

# ADD DATABASE CALL HERE
helpperFunctions.hide_sidebar()
logo = "MoneyMapLogo.png"

col1, col2 = st.columns([1, 7])

with col1:
    st.image(logo, width=70)

with col2:
    st.markdown("<h1 style='font-size: 30px;'>Money <span style='color: red;'>Map</span></h1>", unsafe_allow_html=True)

def show_homepage():
    st.title("Homepage")
    st.write("Welcome to the homepage of the app!")

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