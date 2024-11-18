import datetime
import streamlit as st
import helpperFunctions
import DatabaseConnection as db_conn

helpperFunctions.hide_sidebar()
st.title("Money Map")

checking, saving, expenses, income, loans, credit, search, overview, financial_tools, settings = st.tabs(
    ["Checking", "Savings", "Expenses", "Income"
        , "Loans", "Credit Cards", "Search", "Overview", "Financial Tools", "Settings"])
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
        checking_amount = st.number_input("Amount", min_value=0.00)
        has_fee = st.checkbox("Checking Account Fee")
        if has_fee:
            fee_period = st.selectbox("Fee Period", ["Monthly", "Yearly"])
            checking_fee = st.number_input("Fee Amount", min_value=0.00)
        else:
            fee_period = None
            checking_fee = 0.00

        has_interest = st.checkbox("Calculate Interest Return")
        if has_interest:
            interest_rate_apy = st.number_input("Interest Rate (APY%)", min_value=0.00)
            compounding_type = st.selectbox("Compounding Type", ["Daily", "Monthly", "Quarterly", "Annual"])
        else:
            interest_rate_apy = 0.00
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
                # st.experimental_rerun()
                st.rerun()

    # Update Existing Checking Account
    elif add_or_update == "Update existing account":
        st.write("### Update Existing Checking Account")
        account_names = [account["account_name"] for account in checking_accounts]
        selected_account = st.selectbox("Select Checking Account to Update", [""] + account_names)

        if selected_account:
            account_data = next(acc for acc in checking_accounts if acc["account_name"] == selected_account)
            checking_name = st.text_input("Name of Checking Account", value=account_data["account_name"])
            checking_amount = st.number_input("Amount", min_value=0.00, value=account_data["amount"])
            has_fee = st.checkbox("Checking Account Fee", value=account_data["has_fee"])
            if has_fee:
                fee_period = st.selectbox("Fee Period", ["Monthly", "Yearly"],
                                          index=["Monthly", "Yearly"].index(account_data["fee_period"]))
                checking_fee = st.number_input("Fee Amount", min_value=0.00, value=account_data["fee_amount"])
            else:
                fee_period = None
                checking_fee = 0.00

            has_interest = st.checkbox("Calculate Interest Return", value=account_data["has_interest"])
            if has_interest:
                interest_rate_apy = st.number_input("Interest Rate (APY%)", min_value=0.00,
                                                    value=account_data["interest_rate_apy"])
                compounding_type = st.selectbox(
                    "Compounding Type", ["Daily", "Monthly", "Quarterly", "Annual"],
                    index=["Daily", "Monthly", "Quarterly", "Annual"].index(account_data["compounding_type"])
                )
            else:
                interest_rate_apy = 0.00
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
                # st.experimental_rerun()
                st.rerun()
    elif add_or_update == "Delete Account":
        account_names = [account["account_name"] for account in checking_accounts]
        selected_account = st.selectbox("Select Account to Update", [""] + account_names)
        if selected_account:
            # Delete Account
            if st.button("Confirm Delete"):
                db_conn.delete_checking_account(username, selected_account)
                st.success(f"Checking account '{selected_account}' deleted successfully!")
                # st.experimental_rerun()
                st.rerun()

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
    add_or_update = st.selectbox("Would you like to?",
                                 ["", "Add new account", "Update existing account", "Delete Account"])

    # Add New Savings Account
    if add_or_update == "Add new account":
        st.write("### Add New Savings Account")
        savings_name = st.text_input("Name of Savings Account")
        savings_amount = st.number_input("Amount", min_value=0.00)
        has_fee = st.checkbox("Savings Account Fee")
        if has_fee:
            fee_period = st.selectbox("Fee Period", ["Monthly", "Yearly"])
            savings_fee = st.number_input("Fee Amount", min_value=0.00)
        else:
            fee_period = None
            savings_fee = 0.00

        has_interest = st.checkbox("Calculate Interest Return")
        if has_interest:
            interest_rate_apy = st.number_input("Interest Rate (APY%)", min_value=0.00)
            compounding_type = st.selectbox("Compounding Type", ["Daily", "Monthly", "Quarterly", "Annual"])
        else:
            interest_rate_apy = 0.00
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
                # st.experimental_rerun()
                st.rerun()
    # Update Existing Savings Account
    elif add_or_update == "Update existing account":
        st.write("### Update Existing Savings Account")
        account_names = [account["account_name"] for account in savings_accounts]
        selected_account = st.selectbox("Select Savings Account to Update", [""] + account_names)

        if selected_account:
            account_data = next(acc for acc in savings_accounts if acc["account_name"] == selected_account)
            savings_name = st.text_input("Name of Savings Account", value=account_data["account_name"])
            savings_amount = st.number_input("Amount", min_value=0.00, value=account_data["amount"])
            has_fee = st.checkbox("Savings Account Fee", value=account_data["has_fee"])
            if has_fee:
                fee_period = st.selectbox("Fee Period", ["Monthly", "Yearly"],
                                          index=["Monthly", "Yearly"].index(account_data["fee_period"]))
                savings_fee = st.number_input("Fee Amount", min_value=0.00, value=account_data["fee_amount"])
            else:
                fee_period = None
                savings_fee = 0.00

            has_interest = st.checkbox("Calculate Interest Return", value=account_data["has_interest"])
            if has_interest:
                interest_rate_apy = st.number_input("Interest Rate (APY%)", min_value=0.00,
                                                    value=account_data["interest_rate_apy"])
                compounding_type = st.selectbox(
                    "Compounding Type", ["Daily", "Monthly", "Quarterly", "Annual"],
                    index=["Daily", "Monthly", "Quarterly", "Annual"].index(account_data["compounding_type"])
                )
            else:
                interest_rate_apy = 0.00
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
                db_conn.update_savings_account(username, selected_account,
                                               updated_data)  # New function to update savings accounts
                st.success(f"Savings account '{selected_account}' updated successfully!")
                # st.experimental_rerun()
                st.rerun()

    # Delete Savings Account
    elif add_or_update == "Delete Account":
        account_names = [account["account_name"] for account in savings_accounts]
        selected_account = st.selectbox("Select Account to Delete", [""] + account_names)

        if selected_account:
            if st.button("Confirm Delete"):
                db_conn.delete_savings_account(username, selected_account)  # New function to delete savings accounts
                st.success(f"Savings account '{selected_account}' deleted successfully!")
                # st.experimental_rerun()
                st.rerun()

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
    add_or_update = st.selectbox("Would you like to?",
                                 ["", "Add new expense", "Update existing expense", "Delete expense"])

    # Add New Expense
    if add_or_update == "Add new expense":
        st.write("### Add New Expense")
        expense_name = st.text_input("Expense Name")
        expense_amount = st.number_input("Expense Amount", min_value=0.00)
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
                # st.experimental_rerun()
                st.rerun()

    # Update Existing Expense
    elif add_or_update == "Update existing expense":
        st.write("### Update Existing Expense")
        expense_names = [expense["expense_name"] for expense in expense_accounts]
        selected_expense = st.selectbox("Select Expense to Update", [""] + expense_names)

        if selected_expense:
            expense_data = next(exp for exp in expense_accounts if exp["expense_name"] == selected_expense)
            expense_name = st.text_input("Expense Name", value=expense_data["expense_name"])
            expense_amount = st.number_input("Expense Amount", min_value=0.00, value=expense_data["amount"])
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
                db_conn.update_expense_account(username, selected_expense,
                                               updated_data)  # New function to update expenses
                st.success(f"Expense '{selected_expense}' updated successfully!")
                # st.experimental_rerun()
                st.rerun()

    # Delete Expense
    elif add_or_update == "Delete expense":
        expense_names = [expense["expense_name"] for expense in expense_accounts]
        selected_expense = st.selectbox("Select Expense to Delete", [""] + expense_names)

        if selected_expense:
            if st.button("Confirm Delete"):
                db_conn.delete_expense_account(username, selected_expense)  # New function to delete expenses
                st.success(f"Expense '{selected_expense}' deleted successfully!")
                # st.experimental_rerun()
                st.rerun()

with income:
    st.subheader("Manage Income")
    # Fetch existing income for the logged-in user
    if "username" in st.session_state:
        username = st.session_state["username"]
        income_accounts = db_conn.get_income_accounts(username)  # New function to fetch income
    else:
        st.error("You must be logged in to manage Income.")
        income_accounts = []

    # Select option: Add, Update, or Delete
    add_or_update = st.selectbox("Would you like to?",
                                 ["", "Add new income", "Update existing income", "Delete income"])

    # Add New income
    if add_or_update == "Add new income":
        st.write("### Add New Income")
        income_name = st.text_input("Income Name")
        income_amount = st.number_input("Income Amount", min_value=0.00)
        income_date = st.date_input("Income Date", max_value=datetime.date.today())
        is_recurring = st.checkbox("Income Recurring")
        if is_recurring:
            income_period = st.selectbox("Recurring Period", ["Daily", "Weekly", "Biweekly", "Monthly", "Yearly"])
        else:
            income_period = None

        # Save the new income
        if st.button("Save Income"):
            # Check if the income name already exists
            existing_names = [income["income_name"] for income in income_accounts]
            if income_name.strip() in existing_names:
                st.error(f"The income name '{income_name}' already exists. Please use a different name.")
            elif income_name.strip() == "":
                st.error("Income name cannot be empty.")
            else:
                income_data = {
                    "income_name": income_name,
                    "amount": income_amount,
                    "date": str(income_date),
                    "is_recurring": is_recurring,
                    "period": income_period,
                }
                db_conn.save_income_account(username, income_data)  # New function to save income
                st.success(f"New income '{income_name}' added successfully!")
                # Comment the following lines if as needed
                # st.experimental_rerun()
                st.rerun()

    # Update Existing income
    elif add_or_update == "Update existing income":
        st.write("### Update Existing Income")
        income_names = [income["income_name"] for income in income_accounts]
        selected_income = st.selectbox("Select income to Update", [""] + income_names)

        if selected_income:
            income_data = next(inc for inc in income_accounts if inc["income_name"] == selected_income)
            income_name = st.text_input("Income Name", value=income_data["income_name"])
            income_amount = st.number_input("Income Amount", min_value=0.00, value=income_data["amount"])
            income_date = st.date_input("Income Date", value=datetime.date.fromisoformat(income_data["date"]))
            is_recurring = st.checkbox("Income Recurring", value=income_data["is_recurring"])
            if is_recurring:
                income_period = st.selectbox(
                    "Recurring Period", ["Daily", "Weekly", "Biweekly", "Monthly", "Yearly"],
                    index=["Daily", "Weekly", "Biweekly", "Monthly", "Yearly"].index(income_data["period"])
                )
            else:
                income_period = None

            # Save updates
            if st.button("Update income"):
                updated_data = {
                    "income_name": income_name,
                    "amount": income_amount,
                    "date": str(income_date),
                    "is_recurring": is_recurring,
                    "period": income_period,
                }
                db_conn.update_income_account(username, selected_income,
                                              updated_data)  # New function to update income
                st.success(f"Income '{selected_income}' updated successfully!")
                # st.experimental_rerun()
                st.rerun()

    # Delete income
    elif add_or_update == "Delete income":
        income_names = [income["income_name"] for income in income_accounts]
        selected_income = st.selectbox("Select Income to Delete", [""] + income_names)

        if selected_income:
            if st.button("Confirm Delete"):
                db_conn.delete_income_account(username, selected_income)  # New function to delete income
                st.success(f"Income '{selected_income}' deleted successfully!")
                # st.experimental_rerun()
                st.rerun()

with loans:
    st.subheader("Manage Loans")
    # Fetch existing loans for the logged-in user
    if "username" in st.session_state:
        username = st.session_state["username"]
        loan_accounts = db_conn.get_loan_accounts(username)  # New function to fetch loans
    else:
        st.error("You must be logged in to manage loans.")
        loan_accounts = []

    # Select option: Add, Update, or Delete
    add_or_update = st.selectbox("Would you like to?",
                                 ["", "Add new loan", "Update existing loan", "Delete loan"])

    # Add New Loan
    if add_or_update == "Add new loan":
        st.write("### Add New Loan")
        loan_name = st.text_input("Loan Name")
        loan_amount_left = st.number_input("Loan Amount Left", min_value=0.00)
        loan_start_date = st.date_input("Loan Start Date", max_value=datetime.date.today())
        loan_end_date = st.date_input("Enter Loan End Date", max_value=datetime.date.today())
        loan_Amount_monthly_payment = st.number_input("Monthly payment", min_value=0.00)
        loan_interest = st.number_input("Interest Rate (APR%)", min_value=0.00)

        # Save the new Loan
        if st.button("Save Loan"):
            # Check if the loan name already exists
            existing_names = [loan["loan_name"] for loan in loan_accounts]
            if loan_name.strip() in existing_names:
                st.error(f"The loan name '{loan_name}' already exists. Please use a different name.")
            elif loan_name.strip() == "":
                st.error("Loan name cannot be empty.")
            else:
                loan_data = {
                    "loan_name": loan_name,
                    "amount": loan_amount_left,
                    "start date": str(loan_start_date),
                    "end date": str(loan_end_date),
                    "monthly payment": loan_Amount_monthly_payment,
                    "interest": loan_interest,
                }
                db_conn.save_loan_account(username, loan_data)  # New function to save loans
                st.success(f"New loan '{loan_name}' added successfully!")
                # st.experimental_rerun()
                st.rerun()

    # Update Existing Loan
    elif add_or_update == "Update existing Loan":
        st.write("### Update Existing Loan")
        loan_names = [loan["loan_name"] for loan in loan_accounts]
        selected_loan = st.selectbox("Select loan to Update", [""] + loan_names)

        if selected_loan:
            loan_data = next(loan for loan in loan_accounts if loan["loan_name"] == selected_loan)
            loan_name = st.text_input("Loan Name", value=loan_data["loan_name"])
            loan_amount_left = st.number_input("Loan Amount", min_value=0.00, value=loan_data["amount"])
            loan_start_date = st.date_input("Loan start date", value=datetime.date.fromisoformat(loan_data["start date"]
                                                                                                 ))
            loan_end_date = st.date_input("Loan End date", value=datetime.date.fromisoformat(loan_data["end date"]
                                                                                             ))
            loan_Amount_monthly_payment = st.number_input("Monthly payment", min_value=0.00, value=loan_data["monthly "
                                                                                                             "payment"])
            loan_interest = st.number_input("Interest Rate (APR%)", min_value=0.00, value=loan_data["interest"])

            # Save updates
            if st.button("Update Loan"):
                updated_data = {
                    "loan_name": loan_name,
                    "amount": loan_amount_left,
                    "start date": str(loan_start_date),
                    "end date": str(loan_end_date),
                    "monthly payment": loan_Amount_monthly_payment,
                    "interest": loan_interest,
                }
                db_conn.update_loan_account(username, selected_loan,
                                            updated_data)  # New function to update loan
                st.success(f"Loan '{selected_loan}' updated successfully!")
                # st.experimental_rerun()
                st.rerun()

    # Delete Loan
    elif add_or_update == "Delete loan":
        loan_names = [loan["loan_name"] for loan in loan_accounts]
        selected_loan = st.selectbox("Select Loan to Delete", [""] + loan_names)

        if selected_loan:
            if st.button("Confirm Delete"):
                db_conn.delete_loan_account(username, selected_loan)  # New function to delete loan
                st.success(f"Loan '{selected_loan}' deleted successfully!")
                # st.experimental_rerun()
                st.rerun()

with credit:
    st.subheader("Manage Credit Cards")
    # Fetch existing Credit Cards for the logged-in user
    if "username" in st.session_state:
        username = st.session_state["username"]
        credit_accounts = db_conn.get_credit_accounts(username)  # New function to fetch credit cards
    else:
        st.error("You must be logged in to manage Credit Cards.")
        credit_accounts = []

    # Select option: Add, Update, or Delete
    add_or_update = st.selectbox("Would you like to?",
                                 ["", "Add new Credit Card", "Update existing Credit Card", "Delete Credit Card"])

    # Add New Card
    if add_or_update == "Add new Credit Card":
        st.write("### Add New Credit Card")
        credit_name = st.text_input("Credit Card Name")
        credit_statement_amount = st.number_input("Statement Balance", min_value=0.00)
        credit_statement_date = st.date_input("Statement Date", max_value=datetime.date.today())
        credit_due_date = st.date_input("Enter Statement Due Date", max_value=datetime.date.today())
        credit_interest = st.number_input("Credit Card Interest Rate (APR%)", min_value=0.00)
        annual_fee = st.checkbox("Annual Fee")
        if annual_fee:
            fee_amount = st.number_input("Fee Amount", min_value=0.00)
        else:
            fee_amount = 0.0
        # Save the new card
        if st.button("Save Credit Card"):
            # Check if the card name already exists
            existing_names = [credit["credit_name"] for credit in credit_accounts]
            if credit_name.strip() in existing_names:
                st.error(f"The Credit Card name '{credit_name}' already exists. Please use a different name.")
            elif credit_name.strip() == "":
                st.error("credit card name cannot be empty.")
            else:
                credit_data = {
                    "credit_name": credit_name,
                    "credit_statement_amount": credit_statement_amount,
                    "statement date": str(credit_statement_date),
                    "due date": str(credit_due_date),
                    "annual fee": annual_fee,
                    "fee amount": fee_amount,
                    "interest": credit_interest,
                }
                db_conn.save_credit_account(username, credit_data)  # New function to save loans
                st.success(f"New Credit Card '{credit_name}' added successfully!")
                # st.experimental_rerun()
                st.rerun()

    # Update Existing card
    elif add_or_update == "Update existing Credit Card":
        st.write("### Update Existing Credit Card")
        credit_names = [credit["loan_name"] for credit in credit_accounts]
        selected_credit = st.selectbox("Select credit to Update", [""] + credit_names)

        if selected_credit:
            credit_data = next(credit for credit in credit_accounts if credit["credit_name"] == selected_credit)
            credit_name = st.text_input("Credit Card Name", value=credit_data["credit_name"])
            credit_statement_amount = st.number_input("Statement Balance", min_value=0.00,
                                                      value=credit_data["credit_statement_amount"])

            credit_statement_date = st.date_input("Statement Date", max_value=datetime.date.today(), value=
            datetime.date.fromisoformat(credit_data["statement date"]))

            credit_due_date = st.date_input("Enter Statement Due Date", max_value=datetime.date.today(), value=
            datetime.date.fromisoformat(credit_data["due date"]))

            credit_interest = st.number_input("Credit Card Interest Rate (APR%)", min_value=0.00, value=credit_data["interest"])
            annual_fee = st.checkbox("Annual Fee")
            if annual_fee:
                fee_amount = st.number_input("Fee Amount", min_value=0.00, value=credit_data["annual fee"])
            else:
                fee_amount = 0.0
            # Save updates
            if st.button("Update Credit Card"):
                updated_data = {
                    "credit_name": credit_name,
                    "credit_statement_amount": credit_statement_amount,
                    "statement date": str(credit_statement_date),
                    "due date": str(credit_due_date),
                    "annual fee": annual_fee,
                    "fee amount": fee_amount,
                    "interest": credit_interest,
                }
                db_conn.update_credit_account(username, selected_credit,
                                              updated_data)  # New function to update loan
                st.success(f"Credit card '{selected_credit}' updated successfully!")
                # st.experimental_rerun()
                st.rerun()

    # Delete credit card
    elif add_or_update == "Delete credit card":
        credit_names = [credit["credit_name"] for credit in credit_accounts]
        selected_credit = st.selectbox("Select Credit Card to Delete", [""] + credit_names)

        if selected_credit:
            if st.button("Confirm Delete"):
                db_conn.delete_credit_account(username, selected_credit)  # New function to delete loan
                st.success(f"Credit Card '{selected_credit}' deleted successfully!")
                # st.experimental_rerun()
                st.rerun()
with financial_tools:
    choice = st.selectbox("Choose Tool", ("Quick Payoff Calculator", "Currency Exchange Calculator"))
    if choice == "Quick Payoff Calculator":
        loan_Amount = st.number_input("Amount of loan")
        interest = st.number_input("Interest rate (APR%)")
        pay_by = st.number_input("Payoff in how many months", min_value=0)
        if st.button("Calculate Payment"):
            helpperFunctions.quick_payoff(pay_by, interest, loan_Amount)
    elif choice == "Currency Exchange Calculator":
        base_currency = st.selectbox("Select the currency to be exchanged:", helpperFunctions.currency_codes,
                                     index=helpperFunctions.currency_codes.index("USD"))
        target_currency = st.selectbox("Select the desired currency:", helpperFunctions.currency_codes,
                                       index=helpperFunctions.currency_codes.index("EUR"))
        amount = st.number_input("Enter the amount to convert:", min_value=0.0)
        convertButton = st.button("Convert")
        if convertButton and base_currency == target_currency:
            st.write("Please select two different currencies")
        else:
            rate = helpperFunctions.get_exchange_rate(base_currency, target_currency)
            if rate and convertButton:
                converted_amount = helpperFunctions.convert_currency(amount, rate)
                st.success(f"{amount:.2f} {base_currency} is equal to {converted_amount:.2f} {target_currency}.")

with search:
    st.write("WIP")
    # need to understand database
with overview:
    st.write("WIP")
    # need to understand database
with settings:
    if st.button("Log Out"):
        st.switch_page("Homepage.py")
