import streamlit as st
import helpperFunctions

helpperFunctions.hide_sidebar()
recommended_saving_ratio = 0.2  # Suggested ratio for savings
recommended_saving_percentage = 20  # Suggested max spending as a percentage of income
recommended_spending_percentage = 80  # Spend 80% or less
st.title("Money Map")
currencyExchange, savingsCalculator, Return = st.tabs(
    ["Currency Exchanger", "Spending Analyzer", "Return to Homepage"])

with currencyExchange:
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
with savingsCalculator:
    monthly_income = st.number_input("Please enter your Monthly Income", min_value=0.0)
    monthly_expenses = st.number_input("Please enter your Monthly Expenses", min_value=0.0)
    ratio = helpperFunctions.saving_calculator(monthly_income, monthly_expenses)
    percentage_spent = helpperFunctions.spending_percentage(monthly_income, monthly_expenses)
    amount_saved_or_spent = monthly_income - monthly_expenses  # Positive if saving, negative if overspending

    # Determine message color based on savings
    if st.button("Calculate"):
        # Display the results
        st.info(f"**Recommended Saving Ratio**: {recommended_saving_ratio:.2f} (Saving {recommended_saving_percentage}" 
                f"% of income or more)  \n**Your Savings Ratio is**: {ratio:.2f}  \nYou are spending "
                f"{percentage_spent:.2f}% of your income.")
        if amount_saved_or_spent < 0:
            message_color = "error"  # Red for overspending (negative savings)
            message_text = f"You are overspending by ${abs(amount_saved_or_spent):,.2f}."
        elif percentage_spent <= recommended_spending_percentage:
            message_color = "success"  # Green if spending within or below recommended amount
            message_text = f"Good job! You are saving ${amount_saved_or_spent:,.2f}."
        else:
            message_color = "warning"  # Yellow if spending over the recommended amount but still saving
            message_text = f"You are spending more than recommended, but saving ${amount_saved_or_spent:,.2f}."
        if message_color == "success":
            st.success(message_text)
        elif message_color == "warning":
            st.warning(message_text)
        else:
            st.error(message_text)
with Return:
    st.write("Currently using: Guest Account")
    if st.button("Back to Login"):
        st.switch_page("pages/Homepage.py")
