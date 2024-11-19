import helpperFunctions
import streamlit as st
import DatabaseConnection as db_conn


def checking_account():
    st.subheader("Manage Checking Accounts")

    # Pull accounts for the logged-in user
    if "username" in st.session_state:
        username = st.session_state["username"]
        checking_accounts = db_conn.get_checking_accounts(username)
    else:
        st.error("You must be logged in to manage accounts.")
        checking_accounts = []

    # Select options
    add_or_update = st.selectbox("Would you like to?", ["", "Add new account", "Update existing account",
                                                        "Delete Account"], key="add_or_update_checking_account")

    # If adding another account reset state
    if "reset_checking_state" in st.session_state and st.session_state["reset_checking_state"]:
        st.session_state["new_checking_account"] = ""
        st.session_state["new_checking_amount"] = 0.00
        st.session_state["new_checking_fee"] = False
        st.session_state["new_checking_fee_period"] = "Monthly"
        st.session_state["new_checking_fee_amount"] = 0.00
        st.session_state["new_checking_interest"] = False
        st.session_state["new_checking_interest_rate"] = 0.00
        st.session_state["new_checking_compounding_type"] = "Daily"
        st.session_state["reset_checking_state"] = False  # Turn off the reset flag

    # If updating another account reset state
    if "reset_update_checking_state" in st.session_state and st.session_state["reset_update_checking_state"]:
        st.session_state["update_checking_account"] = ""
        st.session_state["update_checking_amount"] = 0.00
        st.session_state["update_checking_fee"] = False
        st.session_state["update_checking_fee_period"] = "Monthly"
        st.session_state["update_checking_fee_amount"] = 0.00
        st.session_state["update_checking_interest"] = False
        st.session_state["update_checking_interest_rate"] = 0.00
        st.session_state["update_checking_compounding_type"] = "Daily"
        st.session_state["reset_update_checking_state"] = False  # Turn off the reset flag

    # Adding New Checking Account
    if add_or_update == "Add new account":
        st.write("### Add New Checking Account")

        checking_name = st.text_input("Name of Checking Account", key="new_checking_account")
        checking_amount = st.number_input("Amount", min_value=0.00, key="new_checking_amount")
        has_fee = st.checkbox("Checking Account Fee", key="new_checking_fee")
        if has_fee:
            fee_period = st.selectbox("Fee Period", ["Monthly", "Yearly"], key="new_checking_fee_period")
            checking_fee = st.number_input("Fee Amount", min_value=0.00, key="new_checking_fee_amount")
        else:
            fee_period = None
            checking_fee = 0.00

        has_interest = st.checkbox("Calculate Interest Return", key="new_checking_interest")
        if has_interest:
            interest_rate_apy = st.number_input("Interest Rate (APY%)", min_value=0.00, key="new_checking_interest_rate")
            compounding_type = st.selectbox("Compounding Type", ["Daily", "Monthly", "Quarterly", "Annual", "Don't Know"],
                                            key="new_checking_compounding_type")
            if compounding_type == "Don't Know":
                compounding_type = helpperFunctions.account_type()
        else:
            interest_rate_apy = 0.00
            compounding_type = None

        # Saving new account
        if st.button("Save Checking Account", key="save_new_checking_account"):
            # Validating
            if not checking_name.strip():
                st.error("Checking account name cannot be empty.")
            else:
                # Check if name already exists
                existing_names = [account["account_name"] for account in checking_accounts]
                if checking_name.strip() in existing_names:
                    st.error(f"The account name '{checking_name}' already exists. Please use a different name.")
                else:
                    # Create account data to save to database
                    account_data = {
                        "account_name": checking_name.strip(),
                        "amount": checking_amount,
                        "has_fee": has_fee,
                        "fee_period": fee_period,
                        "fee_amount": checking_fee,
                        "has_interest": has_interest,
                        "interest_rate_apy": interest_rate_apy,
                        "compounding_type": compounding_type,
                    }

                    # Saving to the database
                    db_conn.save_checking_account(username, account_data)
                    st.success(f"New checking account '{checking_name}' added successfully!")

                    # Reset flag to clear
                    st.session_state["reset_checking_state"] = True

                    # Add another account/reload
                    if st.button("Add Another Checking Account", key="add_other_checking_account"):
                        st.rerun()

    # Update Existing Checking Account
    elif add_or_update == "Update existing account":
        st.write("### Update Existing Checking Account")
        account_names = [account["account_name"] for account in checking_accounts]

        # Check selection
        if "selected_checking_account" not in st.session_state:
            st.session_state["selected_checking_account"] = ""

        selected_account = st.selectbox("Select Checking Account to Update", [""] + account_names,
                                        key="select_update_checking")

        # Detect if user switches between accounts
        if selected_account and selected_account != st.session_state["selected_checking_account"]:
            st.session_state["selected_checking_account"] = selected_account
            account_data = next(acc for acc in checking_accounts if acc["account_name"] == selected_account)

            # Reset session state
            st.session_state["update_checking_account"] = account_data["account_name"]
            st.session_state["update_checking_amount"] = account_data["amount"]
            st.session_state["update_checking_fee"] = account_data["has_fee"]
            st.session_state["update_checking_fee_period"] = account_data["fee_period"] or "Monthly"
            st.session_state["update_checking_fee_amount"] = account_data["fee_amount"]
            st.session_state["update_checking_interest"] = account_data["has_interest"]
            st.session_state["update_checking_interest_rate"] = account_data["interest_rate_apy"]
            st.session_state["update_checking_compounding_type"] = account_data["compounding_type"] or "Daily"

        if selected_account:
            checking_name = st.text_input("Name of Checking Account", key="update_checking_account")
            checking_amount = st.number_input("Amount", min_value=0.00, key="update_checking_amount")
            has_fee = st.checkbox("Checking Account Fee", key="update_checking_fee")
            if has_fee:
                fee_period = st.selectbox("Fee Period", ["Monthly", "Yearly"], key="update_checking_fee_period")
                checking_fee = st.number_input("Fee Amount", min_value=0.00, key="update_checking_fee_amount")
            else:
                fee_period = None
                checking_fee = 0.00

            has_interest = st.checkbox("Calculate Interest Return", key="update_checking_interest")
            if has_interest:
                interest_rate_apy = st.number_input("Interest Rate (APY%)", min_value=0.00,
                                                    key="update_checking_interest_rate")
                compounding_type = st.selectbox("Compounding Type", ["Daily", "Monthly", "Quarterly", "Annual"],
                                                key="update_checking_compounding_type")
            else:
                interest_rate_apy = 0.00
                compounding_type = None

            # Save Updates
            if st.button("Update Checking Account", key="update_checking_save"):
                updated_data = {
                    "account_name": st.session_state["update_checking_account"],
                    "amount": st.session_state["update_checking_amount"],
                    "has_fee": st.session_state["update_checking_fee"],
                    "fee_period": st.session_state["update_checking_fee_period"],
                    "fee_amount": st.session_state["update_checking_fee_amount"],
                    "has_interest": st.session_state["update_checking_interest"],
                    "interest_rate_apy": st.session_state["update_checking_interest_rate"],
                    "compounding_type": st.session_state["update_checking_compounding_type"],
                }
                db_conn.update_checking_account(username, selected_account, updated_data)
                st.success(f"Checking account '{selected_account}' updated successfully!")

                # Reset update state after saving
                st.session_state["reset_update_checking_state"] = True
                if st.button("Update Another Checking Account", key="update_other_checking_account"):
                    st.rerun()

    # Delete Account
    elif add_or_update == "Delete Account":
        account_names = [account["account_name"] for account in checking_accounts]
        selected_account = st.selectbox("Select Account to Delete", [""] + account_names)
        if selected_account:
            if st.button("Confirm Delete", key="delete_checking_account"):
                db_conn.delete_checking_account(username, selected_account)
                st.success(f"Checking account '{selected_account}' deleted successfully!")
                if st.button("Delete Another Checking Account", key="delete_other_checking_account"):
                    st.rerun()
