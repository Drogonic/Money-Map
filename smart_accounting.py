import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import DatabaseConnection as db
from datetime import datetime, timedelta
import calendar
import helpperFunctions
import savings_goals


def smart_selection():
    if "username" in st.session_state:
        username = st.session_state["username"]
    else:
        st.error("You must be logged in to manage accounts.")
        return

    # Selection for analysis
    smart_selection = st.selectbox("What would you like to do?", ("Analyse Income and Spending", "Saving Goal Tracker",
                                                                  "View APY Projections"))
    if smart_selection == "Analyse Income and Spending":
        analyse_income_to_spend(username)
    elif smart_selection == "View APY Projections":
        view_account_projections(username)
    elif smart_selection == "Saving Goal Tracker":
        savings_goals.savings_goal_tracker(username)






def analyse_income_to_spend(username):
    st.subheader("Analyse Income and Spending Analysis")

    # Fetch data
    income_data = db.get_income_accounts(username)
    expense_data = db.get_expense_accounts(username)
    # Handle empty data
    if not income_data:
        st.info("No income data found. Please add income accounts to start analysis.")
        return
    if not expense_data:
        st.info("No expense data found. Please add expense accounts to start analysis.")
        return

    else:

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
        monthly_income = calculate_monthly_totals(income_df)

        # Add recurring contributions for expenses
        monthly_expenses = calculate_monthly_totals(expense_df)

        # Align months for both income and expenses
        all_months = pd.period_range(start=one_year_ago.strftime('%Y-%m'), end=datetime.now().strftime('%Y-%m'), freq="M")
        monthly_income = monthly_income.reindex(all_months, fill_value=0)
        monthly_expenses = monthly_expenses.reindex(all_months, fill_value=0)

        # Calculate spend-to-income ratio
        spending_percentage = (monthly_expenses / monthly_income.replace(0, float('inf'))) * 100

        # Calculate totals for the year
        total_income_year = monthly_income.sum()
        total_expenses_year = monthly_expenses.sum()
        spend_to_income_year = helpperFunctions.spending_percentage(total_income_year, total_expenses_year)

        # Allow user to select a specific month
        selected_month = st.selectbox("Select a Month to View Totals:", all_months.to_timestamp().strftime('%B %Y'))
        st.info("The recommended Spend-to-Income Ratio is less than 80%.")
        selected_month = pd.to_datetime(selected_month).to_period('M')

        # Totals for the selected month
        total_income_month = monthly_income[selected_month]
        total_expenses_month = monthly_expenses[selected_month]
        spend_to_income_month = helpperFunctions.spending_percentage(total_income_month, total_expenses_month)

        # Display monthly totals
        st.write(f"### Selected Month: {selected_month.strftime('%B %Y')}")
        st.write(f"- **Total Income:** ${total_income_month:,.2f}")
        st.write(f"- **Total Expenses:** ${total_expenses_month:,.2f}")
        st.write(f"- **Spend-to-Income Ratio:** {spend_to_income_month:.2f}%")

        # Display yearly totals
        st.write(f"### This Year Totals:")
        st.write(f"- **Total Income for the Year:** ${total_income_year:,.2f}")
        st.write(f"- **Total Expenses for the Year:** ${total_expenses_year:,.2f}")
        st.write(f"- **Spend-to-Income Ratio for the Year:** {spend_to_income_year:.2f}%")

        multi_options = ["Income History", "Expenses History", "Spend-to-Income History", "View All"]

        view_selections = st.multiselect("Which history would you like to graph?", multi_options)

        # Marker colors for income and expenses
        marker_colors_income = [
            "lightcoral" if income < expense else "lightblue" if income == expense else "lightgreen"
            for expense, income in zip(monthly_expenses.values, monthly_income.values)]

        marker_colors_expenses = [
            "lightcoral" if expense > income else "lightblue" if expense == income else "lightgreen"
            for expense, income in zip(monthly_expenses.values, monthly_income.values)]

        if "View All" in view_selections:
            # Plot Monthly Income
            st.write("### Monthly Income History")
            fig_income = go.Figure()
            fig_income.add_trace(go.Bar(x=monthly_income.index.strftime('%b %Y'), y=monthly_income.values,name="Income",
                                        marker_color=marker_colors_income))
            fig_income.update_layout(title="Monthly Income History", xaxis_title="Month", yaxis_title="Amount ($)",
                                     template="plotly_white")
            st.plotly_chart(fig_income)
            st.write("**Color Key for Income Graph:**")
            st.write("- **Green:** Income is greater than expenses.")
            st.write("- **Blue:** Income is equal to expenses.")
            st.write("- **Red:** Income is less than expenses.")

            # Plot Monthly Expenses
            st.write("### Monthly Expenses History")
            fig_expenses = go.Figure()
            fig_expenses.add_trace(go.Bar(x=monthly_expenses.index.strftime('%b %Y'), y=monthly_expenses.values,
                                          name="Expenses", marker_color=marker_colors_expenses))
            fig_expenses.update_layout(title="Monthly Expenses History", xaxis_title="Month", yaxis_title="Amount ($)",
                                       template="plotly_white")
            st.plotly_chart(fig_expenses)
            st.write("**Color Key for Expenses Graph:**")
            st.write("- **Green:** Expenses are less than income.")
            st.write("- **Blue:** Expenses are equal to income.")
            st.write("- **Red:** Expenses are greater than income.")

            # Plot Spend-to-Income Ratio
            marker_colors_ratio = ["lightgreen" if value < 80 else "lightcoral" for value in spending_percentage]
            st.write("### Spend-to-Income Ratio History")
            fig_ratio = go.Figure()
            fig_ratio.add_trace(go.Bar(x=spending_percentage.index.strftime('%b %Y'), y=spending_percentage.values,
                                       name="Spend-to-Income Ratio", marker_color=marker_colors_ratio))
            fig_ratio.update_layout(title="Spend-to-Income Ratio History", xaxis_title="Month",
                                    yaxis_title="Percentage (%)",template="plotly_white")
            st.plotly_chart(fig_ratio)
            st.write("**Color Key for Spend-to-Income Ratio Graph:**")
            st.write("- **Green:** Ratio is less than 80%.")
            st.write("- **Red:** Ratio is greater than or equal to 80%.")
        else:
            if "Income History" in view_selections:
                # Plot Monthly Income
                st.write("### Monthly Income History")
                fig_income = go.Figure()
                fig_income.add_trace(
                    go.Bar(x=monthly_income.index.strftime('%b %Y'), y=monthly_income.values, name="Income",
                           marker_color=marker_colors_income))
                fig_income.update_layout(title="Monthly Income History", xaxis_title="Month", yaxis_title="Amount ($)",
                                         template="plotly_white")
                st.plotly_chart(fig_income)
                st.write("**Color Key for Income Graph:**")
                st.write("- **Green:** Income is greater than expenses.")
                st.write("- **Blue:** Income is equal to expenses.")
                st.write("- **Red:** Income is less than expenses.")

            if "Expenses History" in view_selections:
                # Plot Monthly Expenses
                st.write("### Monthly Expenses History")
                fig_expenses = go.Figure()
                fig_expenses.add_trace(go.Bar(x=monthly_expenses.index.strftime('%b %Y'), y=monthly_expenses.values,
                                              name="Expenses", marker_color=marker_colors_expenses))
                fig_expenses.update_layout(title="Monthly Expenses History", xaxis_title="Month", yaxis_title="Amount ($)",
                                           template="plotly_white")
                st.plotly_chart(fig_expenses)
                st.write("**Color Key for Expenses Graph:**")
                st.write("- **Green:** Expenses are less than income.")
                st.write("- **Blue:** Expenses are equal to income.")
                st.write("- **Red:** Expenses are greater than income.")
            if "Spend-to-Income History" in view_selections:
                # Plot Spend-to-Income Ratio
                marker_colors_ratio = ["lightgreen" if value < 80 else "lightcoral" for value in spending_percentage]
                st.write("### Spend-to-Income Ratio History")
                fig_ratio = go.Figure()
                fig_ratio.add_trace(go.Bar(x=spending_percentage.index.strftime('%b %Y'), y=spending_percentage.values,
                                           name="Spend-to-Income Ratio", marker_color=marker_colors_ratio))
                fig_ratio.update_layout(title="Spend-to-Income Ratio History", xaxis_title="Month",
                                        yaxis_title="Percentage (%)", template="plotly_white")
                st.plotly_chart(fig_ratio)
                st.write("**Color Key for Spend-to-Income Ratio Graph:**")
                st.write("- **Green:** Ratio is less than 80%.")
                st.write("- **Red:** Ratio is greater than or equal to 80%.")



def calculate_monthly_totals(df):
    df['month'] = df['date'].dt.to_period('M')
    # Initialize monthly totals for the entire range
    monthly_totals = pd.Series(0, index=pd.period_range(df['month'].min(), pd.to_datetime("now").to_period("M"), freq='M'))

    for _, row in df.iterrows():
        start_date = row['date']
        amount = row['amount']
        is_recurring = row.get('is_recurring', False)
        period = row.get('period', None)

        # If not recurring, only add for the specific month
        if not is_recurring:
            transaction_month = pd.Period(start_date.strftime('%Y-%m'), freq='M')
            if transaction_month in monthly_totals.index:
                monthly_totals[transaction_month] += amount
            continue

        # For recurring transactions, apply to all months from the start date
        current_date = start_date
        while current_date <= datetime.now():
            transaction_month = pd.Period(current_date.strftime('%Y-%m'), freq='M')

            if transaction_month in monthly_totals.index:
                if period == "Daily":
                    days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
                    monthly_totals[transaction_month] += amount * days_in_month
                elif period == "Weekly":
                    weeks_in_month = len(pd.date_range(current_date, current_date + timedelta(days=30), freq='W'))
                    monthly_totals[transaction_month] += amount * weeks_in_month
                elif period == "Biweekly":
                    biweekly_in_month = len(pd.date_range(current_date, current_date + timedelta(days=30), freq='2W'))
                    monthly_totals[transaction_month] += amount * biweekly_in_month
                elif period == "Monthly":
                    monthly_totals[transaction_month] += amount
                elif period == "Yearly" and current_date.month == start_date.month:
                    monthly_totals[transaction_month] += amount

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



def view_account_projections(username):
    st.subheader("View Account Projections")

    # Select number of years for projection
    years = st.slider("Select number of years for projection (up to 5 years):", 0, 5, 2)

    # Fetch accounts data
    checking_accounts = db.get_checking_accounts(username)
    savings_accounts = db.get_savings_accounts(username)

    # Combine data for all accounts with APY
    accounts = [
        *[
            {
                "Account Name": account.get("account_name", "N/A"),
                "Account Type": "Checking",
                "Balance": account.get("amount", 0.0),
                "APY%": account.get("interest_rate_apy", 0.0),
                "Fee Type": account.get("fee_period", "None"),
                "Fee Amount": account.get("fee_amount", 0.0),
            }
            for account in checking_accounts if account.get("interest_rate_apy", 0.0) > 0
        ],
        *[
            {
                "Account Name": account.get("account_name", "N/A"),
                "Account Type": "Savings",
                "Balance": account.get("amount", 0.0),
                "APY%": account.get("interest_rate_apy", 0.0),
                "Fee Type": account.get("fee_period", "None"),
                "Fee Amount": account.get("fee_amount", 0.0),
            }
            for account in savings_accounts if account.get("interest_rate_apy", 0.0) > 0
        ],
    ]

    if not accounts:
        st.write("No accounts with APY available for projection.")
        return

    # Allow the user to filter accounts
    account_names = [account["Account Name"] for account in accounts]
    selected_accounts = st.multiselect("Accounts with APY filter:", account_names)

    # Prepare data for projection and graphing
    projection_data = []
    for account in accounts:
        if account["Account Name"] not in selected_accounts:
            continue

        balance = account["Balance"]
        apy = account["APY%"] / 100
        fee_type = account["Fee Type"]
        fee_amount = account["Fee Amount"]

        for year in range(years + 1):  # Include year 0
            # Deduct fees if applicable
            if fee_type == "Monthly":
                total_fees = fee_amount * 12 * year
            elif fee_type == "Yearly":
                total_fees = fee_amount * year
            else:
                total_fees = 0

            # Calculate projected balance
            projected_balance = round(balance * ((1 + apy) ** year) - total_fees,2)

            projection_data.append({
                "Account Name": account["Account Name"],
                "Account Type": account["Account Type"],
                "Year": year,
                "Projected Balance": max(0, projected_balance),  # Ensure no negative balances
            })

    # Convert projection data to DataFrame
    df_projection = pd.DataFrame(projection_data)

    if selected_accounts:

        # Display the table
        st.write("### Projected Growth (After Fees)")
        st.dataframe(df_projection[df_projection["Year"] == 0] if years == 0 else df_projection)

        # Create a combined graph with filtering functionality
        st.write("### Visualize Projected Growth")
        fig = go.Figure()

        for account_name in selected_accounts:
            account_data = df_projection[df_projection["Account Name"] == account_name]
            fig.add_trace(go.Scatter(x=account_data["Year"], y=account_data["Projected Balance"], mode='lines+markers',
                                     name=account_name))

        fig.update_layout(title="Projected Growth by Account", xaxis_title="Year", yaxis_title="Projected Balance ($)",
                          template="plotly_white", legend_title="Filter Graph",)

        st.plotly_chart(fig)
    else:
        st.info("Select Accounts to Display")




























