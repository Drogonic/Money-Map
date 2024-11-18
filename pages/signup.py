import streamlit as st
import helpperFunctions
import DatabaseConnection as db_conn
import bcrypt
helpperFunctions.hide_sidebar()
# we have to implement a check in the future for those that enter a matching user or email to an already created account
with st.form("Signup"):
    st.write("Create Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")
    if st.form_submit_button("Create Account"):
        # Check for existing username
        if db_conn.get_user(username):
            st.error("Username already exists. Please choose a different username.")
        elif not username or not password or not email:
            st.error("All fields are required!")
        else:
            # Save user to database and encrypt password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            db_conn.save_user({
                "username": username,
                "password": hashed_password.decode('utf-8'),
                "email": email,
            })
            st.success("Account created successfully!")
            st.session_state["create_account"] = True

if st.button("Return to Log-in Page"):
    st.switch_page("Homepage.py")
