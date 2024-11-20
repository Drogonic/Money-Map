import time
import streamlit as st
import DatabaseConnection as db_conn
import helpperFunctions


def initialize_session_state_saving():
    default_state = {
        # New saving account keys
        "new_savings_account": "",
        "new_saving_amount": 0.00,
        "new_saving_fee": False,
        "new_saving_fee_period": "Monthly",
        "new_saving_fee_amount": 0.00,
        "new_saving_interest": False,
        "new_saving_interest_rate": 0.00,
        "new_saving_compounding_type": "Daily",
        "reset_saving_state": False,
        # Update saving account keys
        "update_saving_account": "",
        "update_saving_amount": 0.00,
        "update_saving_fee": False,
        "update_saving_fee_period": "Monthly",
        "update_saving_fee_amount": 0.00,
        "update_saving_interest": False,
        "update_saving_interest_rate": 0.00,
        "update_saving_compounding_type": "Daily",
        "reset_update_saving_state": False,
        # Selection keys
        "add_or_update_saving_account": "",
        "select_update_saving": "",
        "last_selected_saving_account": None,
    }
    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_new_savings_account_state():
    st.session_state["new_saving_account"] = ""
    st.session_state["new_saving_amount"] = 0.00
    st.session_state["new_saving_fee"] = False
    st.session_state["new_saving_fee_period"] = "Monthly"
    st.session_state["new_saving_fee_amount"] = 0.00
    st.session_state["new_saving_interest"] = False
    st.session_state["new_saving_interest_rate"] = 0.00
    st.session_state["new_saving_compounding_type"] = "Daily"
    st.session_state["reset_saving_state"] = False


def reset_update_savings_account_state():
    st.session_state["select_update_saving"] = ""
    st.session_state["update_saving_account"] = ""
    st.session_state["update_saving_amount"] = 0.00
    st.session_state["update_saving_fee"] = False
    st.session_state["update_saving_fee_period"] = "Monthly"
    st.session_state["update_saving_fee_amount"] = 0.00
    st.session_state["update_saving_interest"] = False
    st.session_state["update_saving_interest_rate"] = 0.00
    st.session_state["update_saving_compounding_type"] = "Daily"
    st.session_state["last_selected_saving_account"] = None
    st.session_state["reset_update_saving_state"] = False


def saving_account():

    initialize_session_state_saving()  # Ensure session state is initialized

    st.subheader("Manage Savings Accounts")

    # Pull accounts for the logged-in user
    if "username" in st.session_state:
        username = st.session_state["username"]
        saving_accounts = db_conn.get_savings_accounts(username)
    else:
        st.error("You must be logged in to manage accounts.")
        saving_accounts = []

    # Handle reset flags
    if st.session_state.get("reset_saving_state", False):
        reset_new_savings_account_state()
    if st.session_state.get("reset_update_saving_state", False):
        reset_update_savings_account_state()

    # Select options
    add_or_update = st.selectbox(
        "Would you like to?",
        ["", "Add new account", "Update existing account", "Delete Account"],
        key="add_or_update_saving_account"
    )

    # Adding New saving Account
    if add_or_update == "Add new account":
        st.write("### Add New Savings Account")

        saving_name = st.text_input("Name of Savings Account", key="new_saving_account")
        saving_amount = st.number_input("Amount", min_value=0.00, key="new_saving_amount")
        has_fee = st.checkbox("Savings Account Fee", key="new_saving_fee")
        if has_fee:
            fee_period = st.selectbox("Fee Period", ["Monthly", "Yearly"], key="new_saving_fee_period")
            saving_fee = st.number_input("Fee Amount", min_value=0.00, key="new_saving_fee_amount")
        else:
            fee_period = None
            saving_fee = 0.00

        has_interest = st.checkbox("Calculate Interest Return", key="new_saving_interest")
        if has_interest:
            interest_rate_apy = st.number_input("Interest Rate (APY%)", min_value=0.00, key="new_saving_interest_rate")
            compounding_type = st.selectbox(
                "Compounding Type",
                ["Daily", "Monthly", "Quarterly", "Annual", "Don't Know"],
                key="new_saving_compounding_type"
            )
            if compounding_type == "Don't Know":
                compounding_type = helpperFunctions.account_type()
        else:
            interest_rate_apy = 0.00
            compounding_type = None

        if st.button("Save Savings Account", key="save_new_saving_account"):
            if not saving_name.strip():
                st.error("saving account name cannot be empty.")
            else:
                existing_names = [account["account_name"] for account in saving_accounts]
                if saving_name.strip() in existing_names:
                    st.error(f"The account name '{saving_name}' already exists. Please use a different name.")
                else:
                    account_data = {
                        "account_name": saving_name.strip(),
                        "amount": saving_amount,
                        "has_fee": has_fee,
                        "fee_period": fee_period,
                        "fee_amount": saving_fee,
                        "has_interest": has_interest,
                        "interest_rate_apy": interest_rate_apy,
                        "compounding_type": compounding_type,
                    }
                    db_conn.save_savings_account(username, account_data)
                    st.success(f"New Savings account '{saving_name}' added successfully!")
                    st.session_state["reset_saving_state"] = True
                    time.sleep(2)
                    st.rerun()

    # Update Existing Savings Account
    elif add_or_update == "Update existing account":
        st.write("### Update Existing Savings Account")
        account_names = [account["account_name"] for account in saving_accounts]

        selected_account = st.selectbox(
            "Select Savings Account to Update",
            [""] + account_names,
            key="select_update_saving"
        )

        if selected_account:
            if st.session_state.get("last_selected_saving_account") != selected_account:
                account_data = next(acc for acc in saving_accounts if acc["account_name"] == selected_account)
                st.session_state.update({
                    "update_saving_account": account_data["account_name"],
                    "update_saving_amount": account_data["amount"],
                    "update_saving_fee": account_data["has_fee"],
                    "update_saving_fee_period": account_data["fee_period"] or "Monthly",
                    "update_saving_fee_amount": account_data["fee_amount"],
                    "update_saving_interest": account_data["has_interest"],
                    "update_saving_interest_rate": account_data["interest_rate_apy"],
                    "update_saving_compounding_type": account_data["compounding_type"] or "Daily",
                    "last_selected_saving_account": selected_account
                })

            saving_name = st.text_input("Name of saving Account", key="update_saving_account")
            saving_amount = st.number_input("Amount", min_value=0.00, key="update_saving_amount")
            has_fee = st.checkbox("Savings Account Fee", key="update_saving_fee")
            if has_fee:
                fee_period = st.selectbox("Fee Period", ["Monthly", "Yearly"], key="update_saving_fee_period")
                saving_fee = st.number_input("Fee Amount", min_value=0.00, key="update_saving_fee_amount")
            else:
                fee_period = None
                saving_fee = 0.00

            has_interest = st.checkbox("Calculate Interest Return", key="update_saving_interest")
            if has_interest:
                interest_rate_apy = st.number_input("Interest Rate (APY%)", min_value=0.00,
                                                    key="update_saving_interest_rate")
                compounding_type = st.selectbox("Compounding Type",
                                                ["Daily", "Monthly", "Quarterly", "Annual", "Don't Know"],
                                                key="update_saving_compounding_type")
            else:
                interest_rate_apy = 0.00
                compounding_type = None

            if st.button("Update Savings Account", key="update_saving_save"):
                updated_data = {
                    "account_name": st.session_state["update_saving_account"],
                    "amount": st.session_state["update_saving_amount"],
                    "has_fee": st.session_state["update_saving_fee"],
                    "fee_period": st.session_state["update_saving_fee_period"],
                    "fee_amount": st.session_state["update_saving_fee_amount"],
                    "has_interest": st.session_state["update_saving_interest"],
                    "interest_rate_apy": st.session_state["update_saving_interest_rate"],
                    "compounding_type": st.session_state["update_saving_compounding_type"],
                }

                db_conn.update_savings_account(username, selected_account, updated_data)
                st.success(f"Savings account '{selected_account}' updated successfully!")
                st.session_state["reset_update_saving_state"] = True
                time.sleep(2)
                st.rerun()

    # Delete Account
    elif add_or_update == "Delete Account":
        st.write("### Delete Savings Account")
        account_names = [account["account_name"] for account in saving_accounts]
        selected_account = st.selectbox("Select Account to Delete", [""] + account_names)
        if selected_account:
            if st.button("Confirm Delete", key="delete_saving_account"):
                db_conn.delete_savings_account(username, selected_account)
                st.success(f"Savings account '{selected_account}' deleted successfully!")
                time.sleep(2)
                st.rerun()

