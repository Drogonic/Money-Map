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


helpperFunctions.hide_sidebar()
st.title("Money Map")

checking, saving, expenses, income, loans, credit, search, overview, financialtools, settings = st.tabs(
    ["Checking", "Savings", "Expenses", "Income"
        , "Loans", "Credit Cards", "Search", "Overview", "Financial Tools", "Settings"])
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
with search:
    st.write("WIP")
    # need to understand database
with overview:
    # Example usage in Streamlit
    if "username" in st.session_state:
        username = st.session_state["username"]
        overview_accounts.load_format_display_checking_data(username)
        overview_accounts.load_format_display_saving_data(username)
        overview_accounts.load_expenses_for_month(username)
        overview_accounts.load_expenses_for_year(username)
        overview_accounts.load_income_for_month(username)
        overview_accounts.load_income_for_year(username)
    else:
        st.error("Please log in to view your checking accounts.")
with settings:
    if st.button("Log Out"):
        st.session_state.clear()
        st.success("You have been logged out.")
        time.sleep(1)
        st.switch_page("Homepage.py")
    if st.button("Delete Account"):
        if st.button("Proceed with deletion"):
            db_conn.delete_account(st.session_state.get("username"))
            st.success("Your account has been deleted.")
            st.session_state.clear()
            time.sleep(1)
            st.switch_page("Homepage.py")
        elif st.button("Cancel deletion"):
            st.info("Account deletion canceled.")
            st.rerun()

