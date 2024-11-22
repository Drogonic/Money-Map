import streamlit as st
import DatabaseConnection as db_conn
import pandas as pd
from datetime import datetime
from datetime import timedelta
from calendar import monthrange


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
            "Compounding Type": account.get("compounding_type", "None") if account.get("has_interest",
                                                                                       False) else "None",
        }
        # Appending the formatted account to the array
        formatted_checking_data.append(formatted_checking_account)

    # Creating DataFrame
    df = pd.DataFrame(formatted_checking_data)

    # Sum of amount in accounts
    total_amount = 0
    checkNone = df.get("Amount", 0)
    if checkNone is 0:
        st.write("")
    else:
        total_amount = df["Amount"].sum()
    # Start rows at 1
    df.index = df.index + 1

    # Display
    st.write("### Checking Accounts")
    st.dataframe(df)

    # Display total
    st.write(f"**Total Amount in Checking:** ${total_amount:,.2f}")


def load_format_display_saving_data(username):
    # Same process as checking
    saving_accounts = db_conn.get_savings_accounts(username)
    formatted_saving_data = []

    for account in saving_accounts:
        formatted_saving_account = {
            "Account Name": account.get("account_name", "N/A"),
            "Amount": account.get("amount", 0.0),  # Keep numeric for calculations
            "Has Fee?": "Yes" if account.get("has_fee", False) else "No",
            "Fee Period": account.get("fee_period", "None") if account.get("has_fee", False) else "None",
            "Fee Amount": account.get("fee_amount", 0.0) if account.get("has_fee", False) else "None",
            "Has Interest?": "Yes" if account.get("has_interest", False) else "No",
            "APY%": account.get("interest_rate_apy", 0.0) if account.get("has_interest", False) else "None",
            "Compounding Type": account.get("compounding_type", "None") if account.get("has_interest",
                                                                                       False) else "None",
        }
        formatted_saving_data.append(formatted_saving_account)

    df = pd.DataFrame(formatted_saving_data)

    total_amount = 0
    checkNone = df.get("Amount", 0)
    if checkNone is 0:
        st.write("")
    else:
        total_amount = df["Amount"].sum()
    # Start rows at 1
    df.index = df.index + 1

    df.index = df.index + 1

    st.write("### Saving Accounts")
    st.dataframe(df)

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
                # Nonrecurring expense in the current month
                if expense_date.month == current_month and expense_date.year == current_year:
                    monthly_expense = amount
                else:
                    monthly_expense = 0

            # Add to total monthly expense
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
    # same as expenses
    incomes = db_conn.get_income_accounts(username)

    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    formatted_incomes = []
    total_monthly_income = 0

    for income in incomes:
        income_date = datetime.strptime(income.get("date", "1970-01-01"), "%Y-%m-%d")
        is_recurring = income.get("is_recurring", False)
        period = income.get("period", "None")
        amount = income.get("amount", 0.0)

        if income_date.year <= current_year and income_date.month <= current_month:
            if is_recurring:
                if period == "Daily":

                    days_in_month = monthrange(current_year, current_month)[1]
                    monthly_income = amount * days_in_month
                elif period == "Weekly":

                    weeks_in_month = (current_date.day + 6) // 7
                    monthly_income = amount * weeks_in_month
                elif period == "Biweekly":

                    days_in_month = monthrange(current_year, current_month)[1]
                    biweekly_in_month = days_in_month // 14
                    monthly_income = amount * biweekly_in_month
                elif period == "Monthly":

                    monthly_income = amount
                else:

                    monthly_income = 0
            else:

                if income_date.month == current_month and income_date.year == current_year:
                    monthly_income = amount
                else:
                    monthly_income = 0

            total_monthly_income += monthly_income

            formatted_incomes.append({
                "Income Name": income.get("income_name", "N/A"),
                "Amount": f"{monthly_income:,.2f}",
                "Recurring?": "Yes" if is_recurring else "No",
                "Period": period,
                "Date Created": income_date.strftime("%Y-%m-%d"),
            })

    df_month = pd.DataFrame(formatted_incomes)
    df_month.index = df_month.index + 1

    st.write("### Income for This Month")
    st.dataframe(df_month)

    st.write(f"**Total Amount of Income for This Month:** ${total_monthly_income:,.2f}")


def load_income_for_year(username):
    # Same as expenses
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
            current_date = income_date

            while current_date <= now:
                if current_date >= start_of_year:
                    total_recurring += income_amount
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
