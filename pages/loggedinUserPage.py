import datetime
import streamlit as st
import helpperFunctions
import DatabaseConnection as db_conn
helpperFunctions.hide_sidebar()
# REMEMBER TO ADD LOGIC FOR IF THE INPUTS ARE EMPTY
st.title("Money Map")

checking, saving, expenses, income, loans, credit, search, overview,quick_payoff,settings = st.tabs(
    ["Checking", "Savings", "Expenses", "Income"
        , "Loans", "Credit Cards", "Search", "Overview","Quick Payoff Calculator", "Settings"])
with checking:
    st.subheader("Manage Checking Accounts")

    # Fetch existing accounts for the logged-in user
    if "username" in st.session_state:
        username = st.session_state["username"]
        checking_accounts = db_conn.get_checking_accounts(username)
    else:
        st.error("You must be logged in to manage accounts.")
        checking_accounts = []

    # Select option: Add or Update
    add_or_update = st.selectbox("Would you like to?", ["", "Add new account", "Update existing account",
                                                        "Delete Account", ""])

    # Add New Checking Account
    if add_or_update == "Add new account":
        st.write("### Add New Checking Account")
        checking_name = st.text_input("Name of Checking Account")
        checking_amount = st.number_input("Amount", min_value=0.0)
        has_fee = st.checkbox("Checking Account Fee")
        if has_fee:
            fee_period = st.selectbox("Fee Period", ["Monthly", "Yearly"])
            checking_fee = st.number_input("Fee Amount", min_value=0.0)
        else:
            fee_period = None
            checking_fee = 0.0

        has_interest = st.checkbox("Calculate Interest Return")
        if has_interest:
            interest_rate_apy = st.number_input("Interest Rate (APY%)", min_value=0.0)
            compounding_type = st.selectbox("Compounding Type", ["Daily", "Monthly", "Quarterly", "Annual"])
        else:
            interest_rate_apy = 0.0
            compounding_type = None

        # Save the new account
        if st.button("Save Checking Account"):
            # Check if the account name already exists
            existing_names = [account["account_name"] for account in checking_accounts]
            if checking_name.strip() in existing_names:
                st.error(f"The account name '{checking_name}' already exists. Please use a different name.")
            elif checking_name.strip() == "":
                st.error("Checking account name cannot be empty.")
            else:
                account_data = {
                    "account_name": checking_name,
                    "amount": checking_amount,
                    "has_fee": has_fee,
                    "fee_period": fee_period,
                    "fee_amount": checking_fee,
                    "has_interest": has_interest,
                    "interest_rate_apy": interest_rate_apy,
                    "compounding_type": compounding_type,
                }
                db_conn.save_checking_account(username, account_data)
                st.success(f"New checking account '{checking_name}' added successfully!")
                st.experimental_rerun()

    # Update Existing Checking Account
    elif add_or_update == "Update existing account":
        st.write("### Update Existing Checking Account")
        account_names = [account["account_name"] for account in checking_accounts]
        selected_account = st.selectbox("Select Checking Account to Update", [""] + account_names)

        if selected_account:
            account_data = next(acc for acc in checking_accounts if acc["account_name"] == selected_account)
            checking_name = st.text_input("Name of Checking Account", value=account_data["account_name"])
            checking_amount = st.number_input("Amount", min_value=0.0, value=account_data["amount"])
            has_fee = st.checkbox("Checking Account Fee", value=account_data["has_fee"])
            if has_fee:
                fee_period = st.selectbox("Fee Period", ["Monthly", "Yearly"],
                                          index=["Monthly", "Yearly"].index(account_data["fee_period"]))
                checking_fee = st.number_input("Fee Amount", min_value=0.0, value=account_data["fee_amount"])
            else:
                fee_period = None
                checking_fee = 0.0

            has_interest = st.checkbox("Calculate Interest Return", value=account_data["has_interest"])
            if has_interest:
                interest_rate_apy = st.number_input("Interest Rate (APY%)", min_value=0.0,
                                                    value=account_data["interest_rate_apy"])
                compounding_type = st.selectbox(
                    "Compounding Type", ["Daily", "Monthly", "Quarterly", "Annual"],
                    index=["Daily", "Monthly", "Quarterly", "Annual"].index(account_data["compounding_type"])
                )
            else:
                interest_rate_apy = 0.0
                compounding_type = None

            # Save Updates
            if st.button("Update Checking Account"):
                updated_data = {
                    "account_name": checking_name,
                    "amount": checking_amount,
                    "has_fee": has_fee,
                    "fee_period": fee_period,
                    "fee_amount": checking_fee,
                    "has_interest": has_interest,
                    "interest_rate_apy": interest_rate_apy,
                    "compounding_type": compounding_type,
                }
                db_conn.update_checking_account(username, selected_account, updated_data)
                st.success(f"Checking account '{selected_account}' updated successfully!")
                st.experimental_rerun()
    elif add_or_update == "Delete Account":
        account_names = [account["account_name"] for account in checking_accounts]
        selected_account = st.selectbox("Select Account to Update", [""] + account_names)
        if selected_account:
            # Delete Account
                if st.button("Confirm Delete"):
                    db_conn.delete_checking_account(username, selected_account)
                    st.success(f"Checking account '{selected_account}' deleted successfully!")
                    st.experimental_rerun()


with saving:
    st.subheader("Manage Savings Accounts")

    # Fetch existing savings accounts for the logged-in user
    if "username" in st.session_state:
        username = st.session_state["username"]
        savings_accounts = db_conn.get_savings_accounts(username)  # New function to fetch savings accounts
    else:
        st.error("You must be logged in to manage accounts.")
        savings_accounts = []

    # Select option: Add or Update
    add_or_update = st.selectbox("Would you like to?", ["", "Add new account", "Update existing account", "Delete Account"])

    # Add New Savings Account
    if add_or_update == "Add new account":
        st.write("### Add New Savings Account")
        savings_name = st.text_input("Name of Savings Account")
        savings_amount = st.number_input("Amount", min_value=0.0)
        has_fee = st.checkbox("Savings Account Fee")
        if has_fee:
            fee_period = st.selectbox("Fee Period", ["Monthly", "Yearly"])
            savings_fee = st.number_input("Fee Amount", min_value=0.0)
        else:
            fee_period = None
            savings_fee = 0.0

        has_interest = st.checkbox("Calculate Interest Return")
        if has_interest:
            interest_rate_apy = st.number_input("Interest Rate (APY%)", min_value=0.0)
            compounding_type = st.selectbox("Compounding Type", ["Daily", "Monthly", "Quarterly", "Annual"])
        else:
            interest_rate_apy = 0.0
            compounding_type = None

        # Save the new account
        if st.button("Save Savings Account"):
            # Check if the account name already exists
            existing_names = [account["account_name"] for account in savings_accounts]
            if savings_name.strip() in existing_names:
                st.error(f"The account name '{savings_name}' already exists. Please use a different name.")
            elif savings_name.strip() == "":
                st.error("Savings account name cannot be empty.")
            else:
                account_data = {
                    "account_name": savings_name,
                    "amount": savings_amount,
                    "has_fee": has_fee,
                    "fee_period": fee_period,
                    "fee_amount": savings_fee,
                    "has_interest": has_interest,
                    "interest_rate_apy": interest_rate_apy,
                    "compounding_type": compounding_type,
                }
                db_conn.save_savings_account(username, account_data)  # New function to save savings accounts
                st.success(f"New savings account '{savings_name}' added successfully!")
                st.experimental_rerun()

    # Update Existing Savings Account
    elif add_or_update == "Update existing account":
        st.write("### Update Existing Savings Account")
        account_names = [account["account_name"] for account in savings_accounts]
        selected_account = st.selectbox("Select Savings Account to Update", [""] + account_names)

        if selected_account:
            account_data = next(acc for acc in savings_accounts if acc["account_name"] == selected_account)
            savings_name = st.text_input("Name of Savings Account", value=account_data["account_name"])
            savings_amount = st.number_input("Amount", min_value=0.0, value=account_data["amount"])
            has_fee = st.checkbox("Savings Account Fee", value=account_data["has_fee"])
            if has_fee:
                fee_period = st.selectbox("Fee Period", ["Monthly", "Yearly"],
                                          index=["Monthly", "Yearly"].index(account_data["fee_period"]))
                savings_fee = st.number_input("Fee Amount", min_value=0.0, value=account_data["fee_amount"])
            else:
                fee_period = None
                savings_fee = 0.0

            has_interest = st.checkbox("Calculate Interest Return", value=account_data["has_interest"])
            if has_interest:
                interest_rate_apy = st.number_input("Interest Rate (APY%)", min_value=0.0,
                                                    value=account_data["interest_rate_apy"])
                compounding_type = st.selectbox(
                    "Compounding Type", ["Daily", "Monthly", "Quarterly", "Annual"],
                    index=["Daily", "Monthly", "Quarterly", "Annual"].index(account_data["compounding_type"])
                )
            else:
                interest_rate_apy = 0.0
                compounding_type = None

            # Save Updates
            if st.button("Update Savings Account"):
                updated_data = {
                    "account_name": savings_name,
                    "amount": savings_amount,
                    "has_fee": has_fee,
                    "fee_period": fee_period,
                    "fee_amount": savings_fee,
                    "has_interest": has_interest,
                    "interest_rate_apy": interest_rate_apy,
                    "compounding_type": compounding_type,
                }
                db_conn.update_savings_account(username, selected_account, updated_data)  # New function to update savings accounts
                st.success(f"Savings account '{selected_account}' updated successfully!")
                st.experimental_rerun()

    # Delete Savings Account
    elif add_or_update == "Delete Account":
        account_names = [account["account_name"] for account in savings_accounts]
        selected_account = st.selectbox("Select Account to Delete", [""] + account_names)

        if selected_account:
            if st.button("Confirm Delete"):
                db_conn.delete_savings_account(username, selected_account)  # New function to delete savings accounts
                st.success(f"Savings account '{selected_account}' deleted successfully!")
                st.experimental_rerun()

with expenses:
    st.subheader("Manage Expenses")

    # Fetch existing expenses for the logged-in user
    if "username" in st.session_state:
        username = st.session_state["username"]
        expense_accounts = db_conn.get_expense_accounts(username)  # New function to fetch expenses
    else:
        st.error("You must be logged in to manage expenses.")
        expense_accounts = []

    # Select option: Add, Update, or Delete
    add_or_update = st.selectbox("Would you like to?", ["", "Add new expense", "Update existing expense", "Delete expense"])

    # Add New Expense
    if add_or_update == "Add new expense":
        st.write("### Add New Expense")
        expense_name = st.text_input("Expense Name")
        expense_amount = st.number_input("Expense Amount", min_value=0.0)
        expense_date = st.date_input("Expense Date", max_value=datetime.date.today())
        is_recurring = st.checkbox("Expense Recurring")
        if is_recurring:
            expense_period = st.selectbox("Recurring Period", ["Daily", "Weekly", "Biweekly", "Monthly", "Yearly"])
        else:
            expense_period = None

        # Save the new expense
        if st.button("Save Expense"):
            # Check if the expense name already exists
            existing_names = [expense["expense_name"] for expense in expense_accounts]
            if expense_name.strip() in existing_names:
                st.error(f"The expense name '{expense_name}' already exists. Please use a different name.")
            elif expense_name.strip() == "":
                st.error("Expense name cannot be empty.")
            else:
                expense_data = {
                    "expense_name": expense_name,
                    "amount": expense_amount,
                    "date": str(expense_date),
                    "is_recurring": is_recurring,
                    "period": expense_period,
                }
                db_conn.save_expense_account(username, expense_data)  # New function to save expenses
                st.success(f"New expense '{expense_name}' added successfully!")
                st.experimental_rerun()

    # Update Existing Expense
    elif add_or_update == "Update existing expense":
        st.write("### Update Existing Expense")
        expense_names = [expense["expense_name"] for expense in expense_accounts]
        selected_expense = st.selectbox("Select Expense to Update", [""] + expense_names)

        if selected_expense:
            expense_data = next(exp for exp in expense_accounts if exp["expense_name"] == selected_expense)
            expense_name = st.text_input("Expense Name", value=expense_data["expense_name"])
            expense_amount = st.number_input("Expense Amount", min_value=0.0, value=expense_data["amount"])
            expense_date = st.date_input("Expense Date", value=datetime.date.fromisoformat(expense_data["date"]))
            is_recurring = st.checkbox("Expense Recurring", value=expense_data["is_recurring"])
            if is_recurring:
                expense_period = st.selectbox(
                    "Recurring Period", ["Daily", "Weekly", "Biweekly", "Monthly", "Yearly"],
                    index=["Daily", "Weekly", "Biweekly", "Monthly", "Yearly"].index(expense_data["period"])
                )
            else:
                expense_period = None

            # Save updates
            if st.button("Update Expense"):
                updated_data = {
                    "expense_name": expense_name,
                    "amount": expense_amount,
                    "date": str(expense_date),
                    "is_recurring": is_recurring,
                    "period": expense_period,
                }
                db_conn.update_expense_account(username, selected_expense, updated_data)  # New function to update expenses
                st.success(f"Expense '{selected_expense}' updated successfully!")
                st.experimental_rerun()

    # Delete Expense
    elif add_or_update == "Delete expense":
        expense_names = [expense["expense_name"] for expense in expense_accounts]
        selected_expense = st.selectbox("Select Expense to Delete", [""] + expense_names)

        if selected_expense:
            if st.button("Confirm Delete"):
                db_conn.delete_expense_account(username, selected_expense)  # New function to delete expenses
                st.success(f"Expense '{selected_expense}' deleted successfully!")
                st.experimental_rerun()

with income:
    income_Name = st.text_input("Income Name")
    income_amount = st.number_input("Income Amount")
    income_date = st.date_input("Income Occurred", max_value=datetime.date.today())
    income_repeat = st.checkbox(" Income Reoccurring")
    if income_repeat:
        income_period = st.selectbox("Time period", ("Daily", "Weekly", "Biweekly", "Monthly", "Biweekly", "Yearly"))
    if st.button("Submit Income"):
        another_income = st.button("Add another income")
with loans:
    loan_Name = st.text_input("Name of Loan")
    initial_loan_amount = st.number_input("Initial loan amount", min_value=0)
    loan_Amount_left = st.number_input("Amount left on loan", min_value=0)
    loan_Amount_monthly_payment = st.number_input("Monthly payment", min_value=0)
    loan_interest = st.number_input("Interest Rate (APR%)",min_value=0)
    loan_start_date = st.date_input("Enter Loan Start Date")
    loan_end_date = st.date_input("Enter Loan End Date")
    if st.button("Submit"):
        another_loan = st.button("Add another Loan")
with credit:
    credit_Name = st.text_input("Name of Card")
    credit_Amount = st.number_input("Statement Amount")
    credit_interest = st.number_input(" Credit Card Interest Rate")
    if st.checkbox("Has Annual Fee"):
        credit_fee = st.number_input("Enter Annual Fee", min_value=0.00)
    if st.button("Submit Credit Card"):
        another_card = st.button("Add another Credit Card")
with quick_payoff:
    loan_Amount = st.number_input("Amount of loan")
    interest = st.number_input("Interest rate (APR%)")
    pay_by = st.number_input("Payoff in how many months", min_value= 0)
    if st.button("Calculate Payment"):
        helpperFunctions.quick_payoff(pay_by,interest,loan_Amount)

with search:
    st.write("WIP")
    # need to understand database
with overview:
    st.write("WIP")
    # need to understand database
with settings:
    if st.button("Log Out"):
        st.switch_page("Homepage.py")
