import streamlit as st
import DatabaseConnection as db_conn
import pandas as pd
from datetime import datetime
from datetime import timedelta
from calendar import monthrange


def overview_selection():
    if "username" in st.session_state:
        username = st.session_state["username"]

        # Overview options
        overview_options = ["View All", "Checking", "Savings", "Expenses", "Income", "Credit Cards", "Loans"]

        # Multiselect for account selection
        account_selection = st.multiselect("Choose what information you would like to view", overview_options)

        # Logic to display data based on selection
        if "View All" in account_selection:
            # If "View All" is selected or nothing is selected, display all
            load_format_display_checking_data(username)
            load_format_display_saving_data(username)
            load_expenses_for_month(username)
            load_expenses_for_year(username)
            load_income_for_month(username)
            load_income_for_year(username)
            load_format_display_credit_card_data(username)
            load_format_display_loan_data(username)
        else:
            # Display data based on individual selections
            if "Checking" in account_selection:
                load_format_display_checking_data(username)
            if "Savings" in account_selection:
                load_format_display_saving_data(username)
            if "Expenses" in account_selection:
                load_expenses_for_month(username)
                load_expenses_for_year(username)
            if "Income" in account_selection:
                load_income_for_month(username)
                load_income_for_year(username)
            if "Credit Cards" in account_selection:
                load_format_display_credit_card_data(username)
            if "Loans" in account_selection:
                load_format_display_loan_data(username)


def load_format_display_checking_data(username):
    # Pull checking accounts from db
    checking_accounts = db_conn.get_checking_accounts(username)

    # Initialize array
    formatted_checking_data = []

    # Pull from each account in the db
    for account in checking_accounts:
        # Format the fields as desired
        formatted_checking_account = {
            "Account Name": account.get("account_name", "N/A"),
            "Amount": account.get("amount", 0.0),  # Keep numeric for calculations
            "Has Fee?": "Yes" if account.get("has_fee", False) else "No",
            "Fee Period": account.get("fee_period", "None") if account.get("has_fee", False) else "None",
            "Fee Amount": account.get("fee_amount", 0.0) if account.get("has_fee", False) else "None",
            "Has Interest?": "Yes" if account.get("has_interest", False) else "No",
            "APY%": account.get("interest_rate_apy", 0.0) if account.get("has_interest", False) else "None",
            "Compounding Type": account.get("compounding_type", "None") if account.get("has_interest", False) else "None",
        }
        # Append the formatted account to the array
        formatted_checking_data.append(formatted_checking_account)

    # Create DataFrame
    if formatted_checking_data:
        df = pd.DataFrame(formatted_checking_data)
    else:
        df = pd.DataFrame(columns=["Account Name", "Amount", "Has Fee?", "Fee Period", "Fee Amount", "Has Interest?", "APY%", "Compounding Type"])

    # Sum of amount in accounts
    if "Amount" in df.columns:
        total_amount = df["Amount"].sum()
    else:
        st.error("The 'Amount' column is missing in the data.")
        total_amount = 0.0

    # Start rows at 1
    df.index = df.index + 1

    # Display
    st.write("### Checking Accounts")
    st.dataframe(df)

    # Display total
    st.write(f"**Total Amount in Checking:** ${total_amount:,.2f}")


def load_format_display_saving_data(username):
    # Pull savings accounts from db
    savings_accounts = db_conn.get_savings_accounts(username)

    # Initialize array
    formatted_saving_data = []

    # Pull from each account in the db
    for account in savings_accounts:
        # Format the fields as desired
        formatted_saving_account = {
            "Account Name": account.get("account_name", "N/A"),
            "Amount": account.get("amount", 0.0),  # Ensure numeric for calculations
            "Has Fee?": "Yes" if account.get("has_fee", False) else "No",
            "Fee Period": account.get("fee_period", "None") if account.get("has_fee", False) else "None",
            "Fee Amount": account.get("fee_amount", 0.0) if account.get("has_fee", False) else "None",
            "Has Interest?": "Yes" if account.get("has_interest", False) else "No",
            "APY%": account.get("interest_rate_apy", 0.0) if account.get("has_interest", False) else "None",
            "Compounding Type": account.get("compounding_type", "None") if account.get("has_interest", False) else "None",
        }
        # Append the formatted account to the array
        formatted_saving_data.append(formatted_saving_account)

    # Create DataFrame
    if formatted_saving_data:
        df = pd.DataFrame(formatted_saving_data)
    else:
        # Create an empty DataFrame with the expected structure
        df = pd.DataFrame(columns=["Account Name", "Amount", "Has Fee?", "Fee Period", "Fee Amount", "Has Interest?", "APY%", "Compounding Type"])

    # Sum of amount in accounts
    if "Amount" in df.columns:
        total_amount = df["Amount"].sum()
    else:
        st.error("The 'Amount' column is missing in the data.")
        total_amount = 0.0

    # Start rows at 1
    df.index = df.index + 1

    # Display
    st.write("### Savings Accounts")
    st.dataframe(df)

    # Display total
    st.write(f"**Total Amount in Savings:** ${total_amount:,.2f}")


def load_expenses_for_month(username):
    # Pull expenses from db
    expenses = db_conn.get_expense_accounts(username)

    # Current month and year
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    # Preparing formatted data
    formatted_expenses = []
    total_monthly_expense = 0

    for expense in expenses:
        expense_date = datetime.strptime(expense.get("date", "1970-01-01"), "%Y-%m-%d")
        is_recurring = expense.get("is_recurring", False)
        period = expense.get("period", "None")
        amount = expense.get("amount", 0.0)

        # Calculate recurrence for current month
        if expense_date.year <= current_year and expense_date.month <= current_month:
            if is_recurring:
                if period == "Daily":
                    # Get the number of days in current month
                    days_in_month = monthrange(current_year, current_month)[1]
                    monthly_expense = amount * days_in_month
                elif period == "Weekly":
                    # Get the number of weeks in current month
                    weeks_in_month = (current_date.day + 6) // 7
                    monthly_expense = amount * weeks_in_month
                elif period == "Biweekly":
                    # Calculate the number of biweekly occurrences
                    days_in_month = monthrange(current_year, current_month)[1]
                    biweekly_in_month = days_in_month // 14
                    monthly_expense = amount * biweekly_in_month
                elif period == "Monthly":
                    # Add the monthly amount
                    monthly_expense = amount
                else:
                    monthly_expense = 0
            else:
                # Non-recurring expense must strictly match the current month and year
                if expense_date.month == current_month and expense_date.year == current_year:
                    monthly_expense = amount
                else:
                    monthly_expense = 0

            # Add to total monthly expense
            if monthly_expense > 0:  # Only include expenses with non-zero values
                total_monthly_expense += monthly_expense
                # Add formatted data
                formatted_expenses.append({
                    "expense Name": expense.get("expense_name", "N/A"),
                    "Amount": f"{monthly_expense:,.2f}",
                    "Recurring?": "Yes" if is_recurring else "No",
                    "Period": period,
                    "Date Created": expense_date.strftime("%Y-%m-%d"),
                })

    # Convert to DataFrame and display
    df_month = pd.DataFrame(formatted_expenses)
    df_month.index = df_month.index + 1  # Start rows at 1

    # Display table
    st.write("### Expenses for This Month")
    st.dataframe(df_month)

    # Total monthly expense
    st.write(f"**Total Amount Expenses for This Month:** ${total_monthly_expense:,.2f}")


def load_expenses_for_year(username):
    # Pull expenses from the db
    expenses = db_conn.get_expense_accounts(username)

    # Initialize array
    current_year_expenses = []

    # current year date range
    now = datetime.now()
    start_of_year = datetime(now.year, 1, 1)

    # Process expenses
    for expense in expenses:
        expense_date = datetime.strptime(expense.get("date", "1970-01-01"), "%Y-%m-%d")
        recurring = expense.get("is_recurring", False)
        expense_amount = expense.get("amount", 0.0)

        # Calculate rec totals
        total_recurring = 0
        if recurring:
            period = expense.get("period", "None")
            current_date = expense_date

            while current_date <= now:
                if current_date >= start_of_year:
                    total_recurring += expense_amount
                if period == "Daily":
                    current_date += timedelta(days=1)
                elif period == "Weekly":
                    current_date += timedelta(weeks=1)
                elif period == "Biweekly":
                    current_date += timedelta(weeks=2)
                elif period == "Monthly":
                    next_month = current_date.month % 12 + 1
                    current_date = current_date.replace(month=next_month)
                elif period == "Yearly":
                    current_date = current_date.replace(year=current_date.year + 1)

        # Format expense data
        formatted_expense = {
            "Expense Name": expense.get("expense_name", "N/A"),
            "Amount": round(total_recurring if recurring else expense_amount, 2),
            "Recurring?": "Yes" if recurring else "No",
            "Period": expense.get("period", "None") if recurring else "None",
            "Date Created": expense_date.strftime("%Y-%m-%d"),
        }

        # Include expense yearly table
        current_year_expenses.append(formatted_expense)

    # DataFrame
    df_year = pd.DataFrame(current_year_expenses)

    # Calculate total amount
    total_year = sum(expense["Amount"] for expense in current_year_expenses)

    # Rows starting at 1
    df_year.index = range(1, len(df_year) + 1)

    # Display
    st.write("### Expenses for This Year")
    if not df_year.empty:
        st.dataframe(df_year)
        st.write(f"**Total Amount of Expenses for This Year:** ${total_year:,.2f}")
    else:
        st.write("No expenses recorded for this year.")


def load_income_for_month(username):
    # Pull income from db
    income = db_conn.get_income_accounts(username)

    # Current month and year
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    # Preparing formatted data
    formatted_income = []
    total_monthly_income = 0

    for item in income:
        income_date = datetime.strptime(item.get("date", "1970-01-01"), "%Y-%m-%d")
        is_recurring = item.get("is_recurring", False)
        period = item.get("period", "None")
        amount = item.get("amount", 0.0)

        # Calculate recurrence for current month
        if income_date.year <= current_year and income_date.month <= current_month:
            if is_recurring:
                if period == "Daily":
                    # Get the number of days in current month
                    days_in_month = monthrange(current_year, current_month)[1]
                    monthly_income = amount * days_in_month
                elif period == "Weekly":
                    # Get the number of weeks in current month
                    weeks_in_month = (current_date.day + 6) // 7
                    monthly_income = amount * weeks_in_month
                elif period == "Biweekly":
                    # Calculate the number of biweekly occurrences
                    days_in_month = monthrange(current_year, current_month)[1]
                    biweekly_in_month = days_in_month // 14
                    monthly_income = amount * biweekly_in_month
                elif period == "Monthly":
                    # Add the monthly amount
                    monthly_income = amount
                else:
                    monthly_income = 0
            else:
                # Non-recurring income must strictly match the current month and year
                if income_date.month == current_month and income_date.year == current_year:
                    monthly_income = amount
                else:
                    monthly_income = 0

            # Add to total monthly income
            if monthly_income > 0:  # Only include income with non-zero values
                total_monthly_income += monthly_income
                # Add formatted data
                formatted_income.append({
                    "Income Source": item.get("income_name", "N/A"),
                    "Amount": f"{monthly_income:,.2f}",
                    "Recurring?": "Yes" if is_recurring else "No",
                    "Period": period,
                    "Date Created": income_date.strftime("%Y-%m-%d"),
                })

    # Convert to DataFrame and display
    df_month = pd.DataFrame(formatted_income)
    df_month.index = df_month.index + 1  # Start rows at 1

    # Display table
    st.write("### Income for This Month")
    st.dataframe(df_month)

    # Total monthly income
    st.write(f"**Total Amount Income for This Month:** ${total_monthly_income:,.2f}")


def load_income_for_year(username):
    incomes = db_conn.get_income_accounts(username)
    current_year_incomes = []
    now = datetime.now()
    start_of_year = datetime(now.year, 1, 1)

    for income in incomes:
        income_date = datetime.strptime(income.get("date", "1970-01-01"), "%Y-%m-%d")
        recurring = income.get("is_recurring", False)
        income_amount = income.get("amount", 0.0)
        total_recurring = 0

        if recurring:
            period = income.get("period", "None")
            if period == "Daily":
                days_in_year = (now - start_of_year).days + 1
                total_recurring = income_amount * days_in_year
            elif period == "Weekly":
                weeks_in_year = ((now - start_of_year).days + 1) // 7
                total_recurring = income_amount * weeks_in_year
            elif period == "Biweekly":
                biweekly_in_year = ((now - start_of_year).days + 1) // 14
                total_recurring = income_amount * biweekly_in_year
            elif period == "Monthly":
                months_in_year = now.month - start_of_year.month + 1
                total_recurring = income_amount * months_in_year
            elif period == "Yearly" and income_date.year <= now.year:
                total_recurring = income_amount

        formatted_income = {
            "Income Name": income.get("income_name", "N/A"),
            "Amount": round(total_recurring if recurring else income_amount, 2),
            "Recurring?": "Yes" if recurring else "No",
            "Period": income.get("period", "None") if recurring else "None",
            "Date Created": income_date.strftime("%Y-%m-%d"),
        }

        current_year_incomes.append(formatted_income)

    df_year = pd.DataFrame(current_year_incomes)
    total_year = sum(income["Amount"] for income in current_year_incomes)
    df_year.index = range(1, len(df_year) + 1)

    st.write("### Income for This Year")
    if not df_year.empty:
        st.dataframe(df_year)
        st.write(f"**Total Amount of Income for This Year:** ${total_year:,.2f}")
    else:
        st.write("No income recorded for this year.")

def load_format_display_credit_card_data(username):
    # Pull credit card accounts from the database
    credit_card_accounts = db_conn.get_credit_accounts(username)

    # Initialize array for formatted data
    formatted_credit_card_data = []

    # Format data for each credit card account
    for account in credit_card_accounts:
        formatted_credit_card = {
            "Card Name": account.get("credit_name", "N/A"),
            "Total Balance": account.get("total_balance", 0.0),  # Ensure numeric for calculations
            "Statement Amount": account.get("statement_amount", 0.0),
            "Due Date": account.get("due_date", "N/A"),
            "Has Promo Rate?": "Yes" if account.get("has_promo", False) else "No",
            "Promo Interest Rate (%)": account.get("promo_interest", "None") if account.get("has_promo", False) else "None",
            "Promo End Date": account.get("promo_end_date", "None") if account.get("has_promo", False) else "None",
            "Annual Fee?": "Yes" if account.get("annual_fee", False) else "No",
            "Fee Amount": account.get("fee_amount", 0.0) if account.get("annual_fee", False) else "None",
        }
        formatted_credit_card_data.append(formatted_credit_card)

    # Create DataFrame
    if formatted_credit_card_data:
        df = pd.DataFrame(formatted_credit_card_data)
    else:
        # Create an empty DataFrame with the expected structure
        df = pd.DataFrame(columns=["Card Name", "Total Balance", "Statement Amount", "Due Date",
                                   "Has Promo Rate?", "Promo Interest Rate (%)", "Promo End Date",
                                   "Annual Fee?", "Fee Amount"])
    # Calculate total balance
    if "Total Balance" in df.columns:
        total_balance = df["Total Balance"].sum()
    else:
        st.error("The 'Total Balance' column is missing in the data.")
        total_balance = 0.0

    # Renumber rows to start at 1
    df.index = df.index + 1

    # Display the credit card accounts
    st.write("### Credit Card Accounts")
    st.dataframe(df)

    # Display total balance
    st.write(f"**Total Balance on Credit Cards:** ${total_balance:,.2f}")


def load_format_display_loan_data(username):
    # Pull loan accounts from the database
    loan_accounts = db_conn.get_loan_accounts(username)

    # Initialize array for formatted data
    formatted_loan_data = []

    # Format data for each loan account
    for account in loan_accounts:
        formatted_loan = {
            "Loan Name": account.get("loan_name", "N/A"),
            "Total Amount": account.get("initial_amount", 0.0),  # Ensure numeric for calculations
            "Remaining Balance": account.get("amount_left", 0.0),
            "Monthly Payment": account.get("monthly_payment", 0.0),
            "Interest Rate (%)": account.get("interest_rate", "None"),
            "Start Date": account.get("start_date", "N/A"),
            "End Date": account.get("end_date", "N/A"),
        }
        formatted_loan_data.append(formatted_loan)

    # Create DataFrame
    if formatted_loan_data:
        df = pd.DataFrame(formatted_loan_data)
    else:
        # Create an empty DataFrame with the expected structure
        df = pd.DataFrame(columns=["Loan Name", "Total Amount", "Remaining Balance",
                                   "Monthly Payment", "Interest Rate (%)",
                                   "Start Date", "End Date"])

    # Calculate total loan amount
    if "Total Amount" in df.columns:
        total_loan_amount = df["Total Amount"].sum()
    else:
        st.error("The 'Total Amount' column is missing in the data.")
        total_loan_amount = 0.0

    # Renumber rows to start at 1
    df.index = df.index + 1

    # Display the loan accounts
    st.write("### Loan Accounts")
    st.dataframe(df)

    # Display total loan amount
    st.write(f"**Total Loan Amount:** ${total_loan_amount:,.2f}")
