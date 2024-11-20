import time
import streamlit as st
import DatabaseConnection as db_conn
import helpperFunctions


def initialize_session_state_checking():
    default_state = {
        # New checking account keys
        "new_checking_account": "",
        "new_checking_amount": 0.00,
        "new_checking_fee": False,
        "new_checking_fee_period": "Monthly",
        "new_checking_fee_amount": 0.00,
        "new_checking_interest": False,
        "new_checking_interest_rate": 0.00,
        "new_checking_compounding_type": "Daily",
        "reset_checking_state": False,
        # Update checking account keys
        "update_checking_account": "",
        "update_checking_amount": 0.00,
        "update_checking_fee": False,
        "update_checking_fee_period": "Monthly",
        "update_checking_fee_amount": 0.00,
        "update_checking_interest": False,
        "update_checking_interest_rate": 0.00,
        "update_checking_compounding_type": "Daily",
        "reset_update_checking_state": False,
        # Selection keys
        "add_or_update_checking_account": "",
        "select_update_checking": "",
        "last_selected__checking_account": None,
    }
    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_new_checking_account_state():
    st.session_state["new_checking_account"] = ""
    st.session_state["new_checking_amount"] = 0.00
    st.session_state["new_checking_fee"] = False
    st.session_state["new_checking_fee_period"] = "Monthly"
    st.session_state["new_checking_fee_amount"] = 0.00
    st.session_state["new_checking_interest"] = False
    st.session_state["new_checking_interest_rate"] = 0.00
    st.session_state["new_checking_compounding_type"] = "Daily"
    st.session_state["reset_checking_state"] = False


def reset_update_checking_account_state():
    st.session_state["select_update_checking"] = ""
    st.session_state["update_checking_account"] = ""
    st.session_state["update_checking_amount"] = 0.00
    st.session_state["update_checking_fee"] = False
    st.session_state["update_checking_fee_period"] = "Monthly"
    st.session_state["update_checking_fee_amount"] = 0.00
    st.session_state["update_checking_interest"] = False
    st.session_state["update_checking_interest_rate"] = 0.00
    st.session_state["update_checking_compounding_type"] = "Daily"
    st.session_state["last_selected_checking_account"] = None
    st.session_state["reset_update_checking_state"] = False


def checking_account():
    initialize_session_state_checking()  # Ensure session state is initialized

    st.subheader("Manage Checking Accounts")

    # Pull accounts for the logged-in user
    if "username" in st.session_state:
        username = st.session_state["username"]
        checking_accounts = db_conn.get_checking_accounts(username)
    else:
        st.error("You must be logged in to manage accounts.")
        checking_accounts = []

    # Handle reset flags
    if st.session_state.get("reset_checking_state", False):
        reset_new_checking_account_state()
    if st.session_state.get("reset_update_checking_state", False):
        reset_update_checking_account_state()

    # Select options
    add_or_update = st.selectbox(
        "Would you like to?",
        ["", "Add new account", "Update existing account", "Delete Account"],
        key="add_or_update_checking_account"
    )

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
            interest_rate_apy = st.number_input("Interest Rate (APY%)", min_value=0.00,
                                                key="new_checking_interest_rate")
            compounding_type = st.selectbox("Compounding Type",
                                            ["Daily", "Monthly", "Quarterly", "Annual", "Don't Know"],
                                            key="new_checking_compounding_type")
            if compounding_type == "Don't Know":
                compounding_type = helpperFunctions.account_type()
        else:
            interest_rate_apy = 0.00
            compounding_type = None

        # Save the new Checking
        if st.button("Save Checking Account", key="save_new_checking_account"):
            if not checking_name.strip():
                st.error("Checking account name cannot be empty.")
            else:
                existing_names = [account["account_name"] for account in checking_accounts]
                if checking_name.strip() in existing_names:
                    st.error(f"The account name '{checking_name}' already exists. Please use a different name.")
                else:
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
                    db_conn.save_checking_account(username, account_data)
                    st.success(f"New checking account '{checking_name}' added successfully!")
                    st.session_state["reset_checking_state"] = True
                    time.sleep(2)
                    st.rerun()

    # Update Existing Checking Account
    elif add_or_update == "Update existing account":
        st.write("### Update Existing Checking Account")
        account_names = [account["account_name"] for account in checking_accounts]

        selected_account = st.selectbox(
            "Select Checking Account to Update",
            [""] + account_names,
            key="select_update_checking"
        )

        if selected_account:
            if st.session_state.get("last_selected_checking_account") != selected_account:
                account_data = next(acc for acc in checking_accounts if acc["account_name"] == selected_account)
                st.session_state.update({
                    "update_checking_account": account_data["account_name"],
                    "update_checking_amount": account_data["amount"],
                    "update_checking_fee": account_data["has_fee"],
                    "update_checking_fee_period": account_data["fee_period"] or "Monthly",
                    "update_checking_fee_amount": account_data["fee_amount"],
                    "update_checking_interest": account_data["has_interest"],
                    "update_checking_interest_rate": account_data["interest_rate_apy"],
                    "update_checking_compounding_type": account_data["compounding_type"] or "Daily",
                    "last_selected_checking_account": selected_account
                })

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
                compounding_type = st.selectbox("Compounding Type",
                                                ["Daily", "Monthly", "Quarterly", "Annual", "Don't Know"],
                                                key="update_checking_compounding_type")
            else:
                interest_rate_apy = 0.00
                compounding_type = None

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
                st.session_state["reset_update_checking_state"] = True
                time.sleep(2)
                st.rerun()

    # Delete Account
    elif add_or_update == "Delete Account":
        st.write("### Delete Checking Account")
        account_names = [account["account_name"] for account in checking_accounts]
        selected_account = st.selectbox("Select Account to Delete", [""] + account_names)
        if selected_account:
            if st.button("Confirm Delete", key="delete_checking_account"):
                db_conn.delete_checking_account(username, selected_account)
                st.success(f"Checking account '{selected_account}' deleted successfully!")
                time.sleep(2)
                st.rerun()

