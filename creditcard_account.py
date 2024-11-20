import time
import streamlit as st
import DatabaseConnection as db_conn
import datetime


def initialize_session_state_credits():
    default_state = {
        # New credit card keys
        "new_credit_card_name": "",
        "new_credit_total_balance": 0.00,
        "new_credit_statement_amount": 0.00,
        "new_credit_statement_date": datetime.date.today(),
        "new_credit_due_date": datetime.date.today(),
        "new_credit_minimum_due": 0.00,
        "new_credit_interest_regular": 0.00,
        "new_credit_has_promo_interest": False,
        "new_credit_interest_promo": 0.00,
        "new_credit_promo_end_date": datetime.date.today(),
        "new_credit_annual_fee": False,
        "new_credit_fee_amount": 0.00,
        # Update credit card keys
        "update_credit_card_name": "",
        "update_credit_total_balance": 0.00,
        "update_credit_statement_amount": 0.00,
        "update_credit_statement_date": datetime.date.today(),
        "update_credit_due_date": datetime.date.today(),
        "update_credit_minimum_due": 0.00,
        "update_credit_interest_regular": 0.00,
        "update_credit_has_promo_interest": False,
        "update_credit_interest_promo": 0.00,
        "update_credit_promo_end_date": datetime.date.today(),
        "update_credit_annual_fee": False,
        "update_credit_fee_amount": 0.00,
        # Selection keys
        "add_or_update_credit": "",
        "selected_credit": "",
        "last_selected_credit": None,
    }
    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_new_credit_state():
    st.session_state["new_credit_card_name"] = ""
    st.session_state["new_credit_total_balance"] = 0.00
    st.session_state["new_credit_statement_amount"] = 0.00
    st.session_state["new_credit_statement_date"] = datetime.date.today()
    st.session_state["new_credit_due_date"] = datetime.date.today()
    st.session_state["new_credit_minimum_due"] = 0.00
    st.session_state["new_credit_interest_regular"] = 0.00
    st.session_state["new_credit_has_promo_interest"] = False
    st.session_state["new_credit_interest_promo"] = 0.00
    st.session_state["new_credit_promo_end_date"] = datetime.date.today()
    st.session_state["new_credit_annual_fee"] = False
    st.session_state["new_credit_fee_amount"] = 0.00
    st.session_state["reset_new_credit_state"] = False


def reset_update_credit_state():
    st.session_state["update_credit_card_name"] = ""
    st.session_state["update_credit_total_balance"] = 0.00
    st.session_state["update_credit_statement_amount"] = 0.00
    st.session_state["update_credit_statement_date"] = datetime.date.today()
    st.session_state["update_credit_due_date"] = datetime.date.today()
    st.session_state["update_credit_minimum_due"] = 0.00
    st.session_state["update_credit_interest_regular"] = 0.00
    st.session_state["update_credit_has_promo_interest"] = False
    st.session_state["update_credit_interest_promo"] = 0.00
    st.session_state["update_credit_promo_end_date"] = datetime.date.today()
    st.session_state["update_credit_annual_fee"] = False
    st.session_state["update_credit_fee_amount"] = 0.00
    st.session_state["reset_update_credit_state"] = False


def credit_accounts():
    initialize_session_state_credits()

    st.subheader("Manage Credit Cards")

    if "username" in st.session_state:
        username = st.session_state["username"]
        credit_accounts = db_conn.get_credit_accounts(username)
    else:
        st.error("You must be logged in to manage Credit Cards.")
        return

    # Handle reset flags
    if st.session_state.get("reset_new_credit_state", False):
        reset_new_credit_state()
    if st.session_state.get("reset_update_credit_state", False):
        reset_update_credit_state()

    add_or_update = st.selectbox(
        "Would you like to?",
        ["", "Add new Credit Card", "Update existing Credit Card", "Delete Credit Card"],
        key="add_or_update_credit",
    )

    # Add New Credit Card
    if add_or_update == "Add new Credit Card":
        st.write("### Add New Credit Card")
        credit_name = st.text_input("Credit Card Name", key="new_credit_card_name")
        credit_total_balance = st.number_input("Enter Total Balance", min_value=0.00, key="new_credit_total_balance")
        credit_statement_amount = st.number_input("Statement Balance", min_value=0.00, key="new_credit_statement_amount")
        credit_statement_date = st.date_input("Statement Date", max_value=datetime.date.today(), key="new_credit_statement_date")
        credit_due_date = st.date_input("Statement Due Date", key="new_credit_due_date")
        credit_minimum_due = st.number_input("Minimum Due", min_value=0.00, key="new_credit_minimum_due")
        credit_interest_regular = st.number_input("Regular Interest Rate (APR%)", min_value=0.00, key="new_credit_interest_regular")

        has_promo = st.checkbox("Promotional Interest Rate (APR%)", key="new_credit_has_promo_interest")
        credit_interest_promo = st.number_input("Promo Interest Rate (APR%)", min_value=0.00, key="new_credit_interest_promo") if has_promo else 0.00
        promo_end_date = st.date_input("Promo End Date", key="new_credit_promo_end_date") if has_promo else datetime.date.today()

        annual_fee = st.checkbox("Annual Fee", key="new_credit_annual_fee")
        fee_amount = st.number_input("Fee Amount", min_value=0.00, key="new_credit_fee_amount") if annual_fee else 0.00

        if st.button("Save Credit Card", key="save_new_credit_card"):
            if any(credit["credit_name"] == credit_name.strip() for credit in credit_accounts):
                st.error(f"The Credit Card name '{credit_name}' already exists.")
            elif not credit_name.strip():
                st.error("Credit Card name cannot be empty.")
            else:
                credit_data = {
                    "credit_name": credit_name.strip(),
                    "total_balance": credit_total_balance,
                    "statement_amount": credit_statement_amount,
                    "statement_date": str(credit_statement_date),
                    "due_date": str(credit_due_date),
                    "minimum_due": credit_minimum_due,
                    "regular_interest": credit_interest_regular,
                    "has_promo": has_promo,
                    "promo_interest": credit_interest_promo,
                    "promo_end_date": str(promo_end_date),
                    "annual_fee": annual_fee,
                    "fee_amount": fee_amount,
                }
                db_conn.save_credit_account(username, credit_data)
                st.success(f"New Credit Card '{credit_name}' added successfully!")
                st.session_state["reset_new_credit_state"] = True
                st.rerun()

    # Update Existing Credit Card
    elif add_or_update == "Update existing Credit Card":
        st.write("### Update Existing Credit Card")
        credit_names = [credit["credit_name"] for credit in credit_accounts]
        selected_credit = st.selectbox("Select Credit Card to Update", [""] + credit_names, key="select_update_credit")

        if selected_credit:
            if st.session_state.get("last_selected_credit") != selected_credit:
                credit_data = next(credit for credit in credit_accounts if credit["credit_name"] == selected_credit)
                st.session_state["update_credit_card_name"] = credit_data["credit_name"]
                st.session_state["update_credit_total_balance"] = credit_data["total_balance"]
                st.session_state["update_credit_statement_amount"] = credit_data["statement_amount"]
                try:
                    st.session_state["update_credit_statement_date"] = (
                        datetime.date.fromisoformat(credit_data["statement_date"])
                        if credit_data.get("statement_date")
                        else datetime.date.today()
                    )
                except (ValueError, TypeError):
                    st.session_state["update_credit_statement_date"] = datetime.date.today()

                try:
                    st.session_state["update_credit_due_date"] = (
                        datetime.date.fromisoformat(credit_data["due_date"])
                        if credit_data.get("due_date")
                        else datetime.date.today()
                    )
                except (ValueError, TypeError):
                    st.session_state["update_credit_due_date"] = datetime.date.today()

                st.session_state["update_credit_minimum_due"] = credit_data["minimum_due"]
                st.session_state["update_credit_interest_regular"] = credit_data["regular_interest"]
                st.session_state["update_credit_has_promo_interest"] = credit_data.get("has_promo", False)
                st.session_state["update_credit_interest_promo"] = credit_data.get("promo_interest", 0.00)
                try:
                    st.session_state["update_credit_promo_end_date"] = (
                        datetime.date.fromisoformat(credit_data["promo_end_date"])
                        if credit_data.get("promo_end_date")
                        else datetime.date.today()
                    )
                except (ValueError, TypeError):
                    st.session_state["update_credit_promo_end_date"] = datetime.date.today()

                st.session_state["update_credit_annual_fee"] = credit_data.get("annual_fee", False)
                st.session_state["update_credit_fee_amount"] = credit_data.get("fee_amount", 0.00)
                st.session_state["last_selected_credit"] = selected_credit

            # Input fields bound to session state
            credit_name = st.text_input("Credit Card Name", key="update_credit_card_name")
            credit_total_balance = st.number_input("Enter Total Balance", min_value=0.00, key="update_credit_total_balance")
            credit_statement_amount = st.number_input("Statement Balance", min_value=0.00, key="update_credit_statement_amount")
            credit_statement_date = st.date_input("Statement Date", key="update_credit_statement_date")
            credit_due_date = st.date_input("Statement Due Date", key="update_credit_due_date")
            credit_minimum_due = st.number_input("Minimum Due", min_value=0.00, key="update_credit_minimum_due")
            credit_interest_regular = st.number_input("Regular Interest Rate (APR%)", min_value=0.00, key="update_credit_interest_regular")

            has_promo = st.checkbox("Promotional Interest Rate (APR%)", key="update_credit_has_promo_interest")
            credit_interest_promo = st.number_input("Promo Interest Rate (APR%)", min_value=0.00, key="update_credit_interest_promo") if has_promo else 0.00
            promo_end_date = st.date_input("Promo End Date", key="update_credit_promo_end_date") if has_promo else datetime.date.today()

            annual_fee = st.checkbox("Annual Fee", key="update_credit_annual_fee")
            fee_amount = st.number_input("Fee Amount", min_value=0.00, key="update_credit_fee_amount") if annual_fee else 0.00

            if st.button("Update Credit Card", key="update_credit_card"):
                updated_data = {
                    "credit_name": credit_name.strip(),
                    "total_balance": credit_total_balance,
                    "statement_amount": credit_statement_amount,
                    "statement_date": str(credit_statement_date),
                    "due_date": str(credit_due_date),
                    "minimum_due": credit_minimum_due,
                    "regular_interest": credit_interest_regular,
                    "has_promo": has_promo,
                    "promo_interest": credit_interest_promo,
                    "promo_end_date": str(promo_end_date),
                    "annual_fee": annual_fee,
                    "fee_amount": fee_amount,
                }
                db_conn.update_credit_account(username, selected_credit, updated_data)
                st.success(f"Credit Card '{selected_credit}' updated successfully!")
                st.session_state["reset_update_credit_state"] = True
                time.sleep(2)
                st.rerun()

    # Delete Credit Card
    elif add_or_update == "Delete Credit Card":
        st.write("### Delete Credit Card")
        credit_names = [credit["credit_name"] for credit in credit_accounts]
        selected_credit = st.selectbox("Select Credit Card to Delete", [""] + credit_names, key="select_delete_credit")

        if selected_credit:
            if st.button("Confirm Delete", key="delete_credit_card"):
                db_conn.delete_credit_account(username, selected_credit)
                st.success(f"Credit Card '{selected_credit}' deleted successfully!")
                time.sleep(2)
                st.rerun()
