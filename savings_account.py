import helpperFunctions
import streamlit as st
import DatabaseConnection as db_conn


def savings_account():
    st.subheader("Manage Savings Accounts")

    # Pull accounts for the logged-in user
    if "username" in st.session_state:
        username = st.session_state["username"]
        savings_accounts = db_conn.get_savings_accounts(username)
    else:
        st.error("You must be logged in to manage accounts.")
        savings_accounts = []

    # Select options
    add_or_update = st.selectbox("Would you like to?", ["", "Add new account", "Update existing account",
                                                        "Delete Account"], key="add_or_update_savings_account")

    # If user is adding another account then reset state
    if "reset_savings_state" in st.session_state and st.session_state["reset_savings_state"]:
        st.session_state["new_savings_account"] = ""
        st.session_state["new_savings_amount"] = 0.00
        st.session_state["new_savings_fee"] = False
        st.session_state["new_savings_fee_period"] = "Monthly"
        st.session_state["new_savings_fee_amount"] = 0.00
        st.session_state["new_savings_interest"] = False
        st.session_state["new_savings_interest_rate"] = 0.00
        st.session_state["new_savings_compounding_type"] = "Daily"
        st.session_state["reset_savings_state"] = False  # Turn off the reset flag

    # If user is updating another account then reset state
    if "reset_update_savings_state" in st.session_state and st.session_state["reset_update_savings_state"]:
        st.session_state["update_savings_account"] = ""
        st.session_state["update_savings_amount"] = 0.00
        st.session_state["update_savings_fee"] = False
        st.session_state["update_savings_fee_period"] = "Monthly"
        st.session_state["update_savings_fee_amount"] = 0.00
        st.session_state["update_savings_interest"] = False
        st.session_state["update_savings_interest_rate"] = 0.00
        st.session_state["update_savings_compounding_type"] = "Daily"
        st.session_state["reset_update_savings_state"] = False  # Turn off the reset flag

    # Add New Savings Account
    if add_or_update == "Add new account":
        st.write("### Add New Savings Account")
        savings_name = st.text_input("Name of Savings Account", key="new_savings_account")
        savings_amount = st.number_input("Amount", min_value=0.00, key="new_savings_amount")
        has_fee = st.checkbox("Savings Account Fee", key="new_savings_fee")
        if has_fee:
            fee_period = st.selectbox("Fee Period", ["Monthly", "Yearly"], key="new_savings_fee_period")
            savings_fee = st.number_input("Fee Amount", min_value=0.00, key="new_savings_fee_amount")
        else:
            fee_period = None
            savings_fee = 0.00

        has_interest = st.checkbox("Calculate Interest Return", key="new_savings_interest")
        if has_interest:
            interest_rate_apy = st.number_input("Interest Rate (APY%)", min_value=0.00, key="new_savings_interest_rate")
            compounding_type = st.selectbox("Compounding Type", ["Daily", "Monthly", "Quarterly", "Annual", "Don't Know"],
                                            key="new_savings_compounding_type")
            if compounding_type == "Don't Know":
                compounding_type = helpperFunctions.account_type()
        else:
            interest_rate_apy = 0.00
            compounding_type = None

        # Save the new account
        if st.button("Save Savings Account", key="save_new_savings_account"):
            # Validate
            if not savings_name.strip():
                st.error("Savings account name cannot be empty.")
            else:
                # Check if account name already exists
                existing_names = [account["account_name"] for account in savings_accounts]
                if savings_name.strip() in existing_names:
                    st.error(f"The account name '{savings_name}' already exists. Please use a different name.")
                else:
                    # Create account data
                    account_data = {
                        "account_name": savings_name.strip(),
                        "amount": savings_amount,
                        "has_fee": has_fee,
                        "fee_period": fee_period,
                        "fee_amount": savings_fee,
                        "has_interest": has_interest,
                        "interest_rate_apy": interest_rate_apy,
                        "compounding_type": compounding_type,
                    }

                    # Save to the database
                    db_conn.save_savings_account(username, account_data)
                    st.success(f"New savings account '{savings_name}' added successfully!")

                    # Reset flag to clear state
                    st.session_state["reset_savings_state"] = True

                    # Add another account/reload
                    if st.button("Add Another Savings Account", key="add_other_savings_account"):
                        st.rerun()

    # Update Existing Savings Account
    elif add_or_update == "Update existing account":
        st.write("### Update Existing Savings Account")
        account_names = [account["account_name"] for account in savings_accounts]

        # Check previous selection
        if "selected_savings_account" not in st.session_state:
            st.session_state["selected_savings_account"] = ""

        selected_account = st.selectbox("Select Savings Account to Update", [""] + account_names,
                                        key="select_update_savings")

        # Detecting if user switches accounts and reset fields if yes
        if selected_account and selected_account != st.session_state["selected_savings_account"]:
            st.session_state["selected_savings_account"] = selected_account
            account_data = next(acc for acc in savings_accounts if acc["account_name"] == selected_account)

            # Reset session state for the selected account
            st.session_state["update_savings_account"] = account_data["account_name"]
            st.session_state["update_savings_amount"] = account_data["amount"]
            st.session_state["update_savings_fee"] = account_data["has_fee"]
            st.session_state["update_savings_fee_period"] = account_data["fee_period"] or "Monthly"
            st.session_state["update_savings_fee_amount"] = account_data["fee_amount"]
            st.session_state["update_savings_interest"] = account_data["has_interest"]
            st.session_state["update_savings_interest_rate"] = account_data["interest_rate_apy"]
            st.session_state["update_savings_compounding_type"] = account_data["compounding_type"] or "Daily"

        if selected_account:
            savings_name = st.text_input("Name of Savings Account", key="update_savings_account")
            savings_amount = st.number_input("Amount", min_value=0.00, key="update_savings_amount")
            has_fee = st.checkbox("Savings Account Fee", key="update_savings_fee")
            if has_fee:
                fee_period = st.selectbox("Fee Period", ["Monthly", "Yearly"], key="update_savings_fee_period")
                savings_fee = st.number_input("Fee Amount", min_value=0.00, key="update_savings_fee_amount")
            else:
                fee_period = None
                savings_fee = 0.00

            has_interest = st.checkbox("Calculate Interest Return", key="update_savings_interest")
            if has_interest:
                interest_rate_apy = st.number_input("Interest Rate (APY%)", min_value=0.00,
                                                    key="update_savings_interest_rate")
                compounding_type = st.selectbox("Compounding Type", ["Daily", "Monthly", "Quarterly", "Annual"],
                                                key="update_savings_compounding_type")
            else:
                interest_rate_apy = 0.00
                compounding_type = None

            # Save Updates
            if st.button("Update Savings Account", key="update_savings_save"):
                updated_data = {
                    "account_name": st.session_state["update_savings_account"],
                    "amount": st.session_state["update_savings_amount"],
                    "has_fee": st.session_state["update_savings_fee"],
                    "fee_period": st.session_state["update_savings_fee_period"],
                    "fee_amount": st.session_state["update_savings_fee_amount"],
                    "has_interest": st.session_state["update_savings_interest"],
                    "interest_rate_apy": st.session_state["update_savings_interest_rate"],
                    "compounding_type": st.session_state["update_savings_compounding_type"],
                }
                db_conn.update_savings_account(username, selected_account, updated_data)
                st.success(f"Savings account '{selected_account}' updated successfully!")

                # Reset state after saving
                st.session_state["reset_update_savings_state"] = True
                if st.button("Update Another Savings Account", key="update_other_savings_account"):
                    st.rerun()

    # Deleting Account
    elif add_or_update == "Delete Account":
        account_names = [account["account_name"] for account in savings_accounts]
        selected_account = st.selectbox("Select Account to Delete", [""] + account_names)
        if selected_account:
            if st.button("Confirm Delete", key="delete_savings_account"):
                db_conn.delete_savings_account(username, selected_account)
                st.success(f"Savings account '{selected_account}' deleted successfully!")
                if st.button("Delete Another Savings Account", key="delete_other_savings_account"):
                    st.rerun()

