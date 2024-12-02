import time
import financial_tools
import streamlit as st
import helpperFunctions
import DatabaseConnection as db_conn
import checking_account
import savings_account
import expenses_account
import income_account
import loans_account
import creditcard_account
import overview_accounts
import smart_accounting


helpperFunctions.hide_sidebar()
logo = "MoneyMapLogo.png"

col1, col2 = st.columns([1, 7])

with col1:
    st.image(logo, width=70)

with col2:
    st.markdown("<h1 style='font-size: 30px;'>Money <span style='color: red;'>Map</span></h1>", unsafe_allow_html=True)

checking, saving, expenses, income, loans, credit, smart, overview, financialtools, settings = st.tabs(
    ["Checking", "Savings", "Expenses", "Income"
        , "Loans", "Credit Cards", "Smart Accounting", "Overview", "Financial Tools", "Settings"])
with checking:
    checking_account.checking_account()

with saving:
    savings_account.saving_account()

with expenses:
    expenses_account.expenses_account()
with income:
    income_account.income_account()

with loans:
    loans_account.loan_accounts()

with credit:
    creditcard_account.credit_accounts()

with financialtools:
    financial_tools.financial_tools()
with smart:
    smart_accounting.smart_selection()
with overview:
    overview_accounts.overview_selection()
with settings:
    # Pull accounts for the logged-in user
    if "username" in st.session_state:
        username = st.session_state["username"]
    else:
        st.error("You must be logged in to manage accounts.")
        st.stop()

    # Log Out Button
    if st.button("Log Out"):
        st.session_state.clear()
        st.success("You have been logged out.")
        time.sleep(1)
        st.switch_page("AboutUs.py")

    # Delete Account Section
    delete_confirmed = st.checkbox("I understand this will delete my account permanently.")

    if delete_confirmed:
        if st.button("Delete My Account"):
            delete_result = db_conn.delete_account(username)
            if delete_result:
                st.success("Your account has been deleted.")
                st.session_state.clear()
                time.sleep(1)
                st.switch_page("AboutUs.py")
            else:
                st.error("An error occurred while deleting your account. Please try again later.")
