import datetime
import streamlit as st
import helpperFunctions

# REMEMBER TO ADD LOGIC FOR IF THE INPUTS ARE EMPTY
st.title("Money Map")

checking, saving, expenses, income, loans, credit, search, overview,settings = st.tabs(
    ["Checking", "Savings", "Expenses", "Income"
        , "Loans", "Credit Cards", "Search", "Overview","Settings"])
with checking:
    checking_Name = st.text_input("Name of Checking Account")
    checking_Amount = st.number_input("Amount")
    fee = st.checkbox(" Checking Account Fee")
    calculate_interest = st.checkbox("Calculate Interest Return for Checking")
    if fee:
        fee_period = st.selectbox("Fee Period", ("Monthly", "Yearly"))
    if calculate_interest:
        interest_rate = st.number_input("Enter Interest Rate")
with saving:
    saving_Name = st.text_input("Name of Saving Account")
    saving_Amount = st.number_input("Saving Amount")
    saving_fee = st.checkbox("Account Fee")
    saving_calculate_interest = st.checkbox("Calculate Interest Return")
    if saving_fee:
        saving_fee_period = st.selectbox("Fee Period", ("Monthly", "Yearly"))
    if calculate_interest:
        saving_interest_rate = st.number_input("Enter Interest Rate")
with expenses:
    expense_Name = st.text_input("Expense Name")
    expense_amount = st.number_input("Expense Amount")
    expense_date = st.date_input("Expense Occurred", max_value=datetime.date.today())
    expense_repeat = st.checkbox(" Expense Reoccurring")
    if expense_repeat:
        expense_period = st.selectbox("Time period", ("Daily", "Weekly", "Biweekly", "Monthly", "Biweekly", "Yearly"))
    if st.button("Submit Expense"):
        another_expense = st.button("Add another expense", type="Primary")
with income:
    income_Name = st.text_input("income Name")
    income_amount = st.number_input("Income Amount")
    income_date = st.date_input("Income Occurred", max_value=datetime.date.today())
    income_repeat = st.checkbox(" Income Reoccurring")
    if income_repeat:
        income_period = st.selectbox("Time period", ("Daily", "Weekly", "Biweekly", "Monthly", "Biweekly", "Yearly"))
    if st.button("Submit Income"):
        another_income = st.button("Add another income")
with loans:
    loan_Name = st.text_input("Name of Loan")
    loan_Amount = st.number_input("Loan Amount")
    loan_interest = st.number_input("Interest Rate")
    loan_length_time = st.selectbox("Days", "Months")
    loan_length_amount = st.number_input(f"Amount of {loan_length_time} ")
    if st.button("Quick Payoff"):
        loan_afford = st.number_input("Payment")
        loan_speed = st.number_input("In how many months")
    if st.button("Submit"):
        another_loan = st.button("Add another Loan")
with credit:
    credit_Name = st.text_input("Name of Card")
    credit_Amount = st.number_input("Statement Amount")
    credit_interest = st.number_input(" Credit Card Interest Rate")
    if st.checkbox("Has Fee"):
        credit_fee = st.selectbox("Annual", "Monthly")
    if st.button("Quick Payoff Credit"):
        credit_afford = st.number_input("Payment")
        credit_speed = st.number_input("In how many months")
    if st.button("Submit Credit Card"):
        another_card = st.button("Add another Credit Card")
with search:
    st.write("WIP")
    # need to understand database
with overview:
    st.write("WIP")
    # need to understand database
with settings:
    if st.button("Log Out"):
        st.switch_page("Homepage.py")
