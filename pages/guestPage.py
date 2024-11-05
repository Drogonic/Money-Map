import streamlit as st
import helpperFunctions

helpperFunctions.hide_sidebar()
recommended_ratio = 1.2  # Suggested income-to-spend ratio
recommended_spending_percentage = 80  # Suggested max spending as a percentage of income
st.title("Money Map")
currencyExchange, savingsCalulator,settings = st.tabs(["Currency Exchanger", "Income to Spend Ratio Calculator","Settings"])

with currencyExchange:
    base_currency = st.selectbox("Select the currency to be exchanged:", helpperFunctions.currency_codes,
                                 index=helpperFunctions.currency_codes.index("USD"))
    target_currency = st.selectbox("Select the desired currency:", helpperFunctions.currency_codes,
                                   index=helpperFunctions.currency_codes.index("EUR"))
    amount = st.number_input("Enter the amount to convert:", min_value=0.0)
    if st.button("Convert"):
        rate = helpperFunctions.get_exchange_rate(base_currency, target_currency)
        if rate:
            converted_amount = helpperFunctions.convert_currency(amount, rate)
            st.success(f"{amount} {base_currency} is equal to {converted_amount:.2f} {target_currency}.")
with savingsCalulator:
    monthly_income = st.number_input("Please enter your Monthly Income", min_value=0.0)
    monthly_expenses = st.number_input("Please enter your Monthly Expenses", min_value=0.0)
    ratio = helpperFunctions.income_to_spend_ratio(monthly_income, monthly_expenses)
    percentage_spent = helpperFunctions.spending_percentage(monthly_income, monthly_expenses)
    amount_saved_or_spent = monthly_income - monthly_expenses  # Positive if saving, negative if overspending

    # Determine message color based on savings
    if amount_saved_or_spent < 0:
        message_color = "error"  # Red for overspending (negative savings)
        message_text = f"You are overspending by ${abs(amount_saved_or_spent):,.2f}."
    elif percentage_spent <= recommended_spending_percentage:
        message_color = "success"  # Green if spending within or below recommended amount
        message_text = f"Good job! You are saving ${amount_saved_or_spent:,.2f}."
    else:
        message_color = "warning"  # Yellow if spending over the recommended amount but still saving
        message_text = f"You are spending more than recommended, but saving ${amount_saved_or_spent:,.2f}."
    if st.button("Calculate"):
        # Display the results
        st.success(f"**Income to Spend Ratio**: {ratio:.2f}")
        st.info(
            f"You are spending {percentage_spent:.2f}% of your income, which means you are saving"
            f" {100 - percentage_spent:.2f}%.")
        st.info(
            f"**Recommended Income to Spend Ratio**: {recommended_ratio:.2f} "
            f"(Spending {recommended_spending_percentage}" f"% of income or less).")
        if message_color == "success":
            st.success(message_text)
        elif message_color == "warning":
            st.warning(message_text)
        else:
            st.error(message_text)
with settings:
    st.write("Currently using: Guest Account")
    if st.button("Logout"):
        st.switch_page("Homepage.py")
