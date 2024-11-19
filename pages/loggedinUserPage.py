import datetime
import streamlit as st
import helpperFunctions
import DatabaseConnection as db_conn
import checking_account
import savings_account
import expenses_account


helpperFunctions.hide_sidebar()
st.title("Money Map")

checking, saving, expenses, income, loans, credit, search, overview, financial_tools, settings = st.tabs(
    ["Checking", "Savings", "Expenses", "Income"
        , "Loans", "Credit Cards", "Search", "Overview", "Financial Tools", "Settings"])
with checking:
    checking_account.checking_account()

with saving:
    savings_account.savings_account()

with expenses:
    expenses_account.expenses_account()
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
