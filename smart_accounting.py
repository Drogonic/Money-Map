import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import DatabaseConnection as db
from datetime import datetime, timedelta
import calendar

import helpperFunctions


def smart_selection():
    if "username" in st.session_state:
        username = st.session_state["username"]
    else:
        st.error("You must be logged in to manage Credit Cards.")
        return

    # Multiselect for account selection
    smart_selection = st.selectbox("What would you like to do?", ("View Account History", "View Account Projections",
                                                                  "Analyse Income and Spending"))
    if smart_selection == "Analyse Income and Spending":
        analyse_income_to_spend(username)


def analyse_income_to_spend(username):
    st.subheader("Analyse Income and Spending Analysis")

    # Fetch data
    income_data = db.get_income_accounts(username)
    expense_data = db.get_expense_accounts(username)

    # Convert to DataFrame for analysis
    income_df = pd.DataFrame(income_data)
    expense_df = pd.DataFrame(expense_data)

    # Parse dates and filter the last year's data
    income_df['date'] = pd.to_datetime(income_df['date'])
    expense_df['date'] = pd.to_datetime(expense_df['date'])

    one_year_ago = datetime.now() - timedelta(days=365)
    income_df = income_df[income_df['date'] >= one_year_ago]
    expense_df = expense_df[expense_df['date'] >= one_year_ago]

    # Add recurring contributions for income
    monthly_income = calculate_monthly_totals(income_df, is_income=True)

    # Add recurring contributions for expenses
    monthly_expenses = calculate_monthly_totals(expense_df, is_income=False)

    # Align months for both income and expenses
    all_months = pd.period_range(start=one_year_ago.strftime('%Y-%m'), end=datetime.now().strftime('%Y-%m'), freq="M")
    monthly_income = monthly_income.reindex(all_months, fill_value=0)
    monthly_expenses = monthly_expenses.reindex(all_months, fill_value=0)

    # Calculate income-to-spend ratio
    spending_percentage = (monthly_expenses / monthly_income.replace(0, float('inf'))) * 100

    # Plot Monthly Income
    st.write("### Monthly Income History")
    fig_income = go.Figure()
    fig_income.add_trace(go.Bar(
        x=monthly_income.index.strftime('%b %Y'),
        y=monthly_income.values,
        name="Income",
        marker_color="lightblue"
    ))
    fig_income.update_layout(
        title="Monthly Income History",
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        template="plotly_white"
    )
    st.plotly_chart(fig_income)

    # Plot Monthly Expenses
    st.write("### Monthly Expenses History")
    fig_expenses = go.Figure()
    fig_expenses.add_trace(go.Bar(
        x=monthly_expenses.index.strftime('%b %Y'),
        y=monthly_expenses.values,
        name="Expenses",
        marker_color="lightcoral"
    ))
    fig_expenses.update_layout(
        title="Monthly Expenses History",
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        template="plotly_white"
    )
    st.plotly_chart(fig_expenses)

    # Calculate marker colors based on the condition
    marker_colors = ["lightgreen" if value < 80 else "lightcoral" for value in spending_percentage]

    # Plot Income-to-Spend Ratio with dynamic colors
    fig_ratio = go.Figure()
    fig_ratio.add_trace(go.Bar(
        x=spending_percentage.index.strftime('%b %Y'),
        y=spending_percentage.values,
        name="Spend-to-Income Ratio",
        marker_color=marker_colors  # Apply the dynamic colors
    ))
    fig_ratio.update_layout(
        title="Spend-to-Income Ratio History",
        xaxis_title="Month",
        yaxis_title="Percentage (%)",
        template="plotly_white"
    )
    st.plotly_chart(fig_ratio)



def calculate_monthly_totals(df, is_income):
    """
    Calculate monthly totals for income or expenses, including recurring amounts.
    :param df: DataFrame with income or expense data
    :param is_income: Boolean indicating whether the data is income
    :return: Series with monthly totals
    """
    df['month'] = df['date'].dt.to_period('M')
    monthly_totals = pd.Series(0, index=pd.period_range(df['month'].min(), df['month'].max(), freq='M'))

    for _, row in df.iterrows():
        start_date = row['date']
        amount = row['amount']
        is_recurring = row.get('is_recurring', False)
        period = row.get('period', None)

        current_date = start_date
        while current_date <= datetime.now():
            current_month = pd.Period(current_date.strftime('%Y-%m'), freq='M')

            if current_month in monthly_totals.index:
                if is_recurring:
                    if period == "Daily":
                        days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
                        monthly_totals[current_month] += amount * days_in_month
                    elif period == "Weekly":
                        weeks_in_month = len(pd.date_range(current_date, current_date + timedelta(days=30), freq='W'))
                        monthly_totals[current_month] += amount * weeks_in_month
                    elif period == "Biweekly":
                        biweekly_in_month = len(pd.date_range(current_date, current_date + timedelta(days=30), freq='2W'))
                        monthly_totals[current_month] += amount * biweekly_in_month
                    elif period == "Monthly":
                        monthly_totals[current_month] += amount
                    elif period == "Yearly" and current_date.month == start_date.month:
                        monthly_totals[current_month] += amount
                else:
                    if current_date.month == start_date.month and current_date.year == start_date.year:
                        monthly_totals[current_month] += amount

            if not is_recurring:
                break

            # Advance to the next recurrence
            if period == "Daily":
                current_date += timedelta(days=1)
            elif period == "Weekly":
                current_date += timedelta(weeks=1)
            elif period == "Biweekly":
                current_date += timedelta(weeks=2)
            elif period == "Monthly":
                next_month = current_date.month % 12 + 1
                current_date = current_date.replace(month=next_month, year=current_date.year + (next_month == 1))
            elif period == "Yearly":
                current_date = current_date.replace(year=current_date.year + 1)

    return monthly_totals
