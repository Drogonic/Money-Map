import time
import streamlit as st
import DatabaseConnection as db_conn
import datetime


def initialize_session_state_loans():
    default_state = {
        # New loan keys
        "new_loan_name": "",
        "new_loan_initial_amount": 0.00,
        "new_loan_amount_left": 0.00,
        "new_loan_start_date": datetime.date.today(),
        "new_loan_end_date": datetime.date.today(),
        "new_loan_monthly_payment": 0.00,
        "new_loan_interest": 0.00,
        # Update loan keys
        "update_loan_name": "",
        "update_loan_initial_amount": 0.00,
        "update_loan_amount_left": 0.00,
        "update_loan_start_date": datetime.date.today(),
        "update_loan_end_date": datetime.date.today(),
        "update_loan_monthly_payment": 0.00,
        "update_loan_interest": 0.00,
        # Selection keys
        "add_or_update_loan": "",
        "selected_loan": "",
        "last_selected_loan": None,
    }
    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_new_loan_state():
    st.session_state[f"new_loan_name"] = ""
    st.session_state[f"new_loan_initial_amount"] = 0.00
    st.session_state[f"new_loan_amount_left"] = 0.00
    st.session_state[f"new_loan_start_date"] = datetime.date.today()
    st.session_state[f"new_loan_end_date"] = datetime.date.today()
    st.session_state[f"new_loan_monthly_payment"] = 0.00
    st.session_state[f"new_loan_interest"] = 0.00
    st.session_state[f"reset_new_loan_state"] = False


def reset_update_loan_state():
    st.session_state[f"update_loan_name"] = ""
    st.session_state[f"update_loan_initial_amount"] = 0.00
    st.session_state[f"update_loan_amount_left"] = 0.00
    st.session_state[f"update_loan_start_date"] = datetime.date.today()
    st.session_state[f"update_loan_end_date"] = datetime.date.today()
    st.session_state[f"update_loan_monthly_payment"] = 0.00
    st.session_state[f"update_loan_interest"] = 0.00
    st.session_state[f"reset_update_loan_state"] = False


def loan_accounts():
    initialize_session_state_loans()  # Initialize session state

    st.subheader("Manage Loans")

    # Fetch loans for the logged-in user
    if "username" in st.session_state:
        username = st.session_state["username"]
        loan_accounts = db_conn.get_loan_accounts(username)  # Fetch loans from DB
    else:
        st.error("You must be logged in to manage loans.")
        return

    # Handle reset flags
    if st.session_state.get("reset_new_loan_state", False):
        reset_new_loan_state()
    if st.session_state.get("reset_update_loan_state", False):
        reset_update_loan_state()

    # Select option
    add_or_update = st.selectbox(
        "Would you like to?",
        ["", "Add new loan", "Update existing loan", "Delete loan"],
        key="add_or_update_loan"
    )

    # Add New Loan
    if add_or_update == "Add new loan":
        st.write("### Add New Loan")
        loan_name = st.text_input("Loan Name", key="new_loan_name")
        loan_initial_amount = st.number_input("Loan Initial Amount", min_value=0.00, key="new_loan_initial_amount")
        loan_amount_left = st.number_input("Loan Amount Left", min_value=0.00, key="new_loan_amount_left")
        loan_start_date = st.date_input("Loan Start Date", max_value=datetime.date.today(), key="new_loan_start_date")
        loan_end_date = st.date_input("Loan End Date", key="new_loan_end_date")
        loan_monthly_payment = st.number_input("Monthly Payment", min_value=0.00, key="new_loan_monthly_payment")
        loan_interest = st.number_input("Interest Rate (APR%)", min_value=0.00, key="new_loan_interest")

        # Save the new loan
        if st.button("Save Loan", key="save_new_loan"):
            existing_names = [loan["loan_name"] for loan in loan_accounts]
            if loan_name.strip() in existing_names:
                st.error(f"The loan name '{loan_name}' already exists. Please use a different name.")
            elif loan_name.strip() == "":
                st.error("Loan name cannot be empty.")
            else:
                loan_data = {
                    "loan_name": loan_name.strip(),
                    "initial_amount": loan_initial_amount,
                    "amount_left": loan_amount_left,
                    "start_date": str(loan_start_date),
                    "end_date": str(loan_end_date),
                    "monthly_payment": loan_monthly_payment,
                    "interest_rate": loan_interest,
                }
                db_conn.save_loan_account(username, loan_data)  # Save to DB
                st.success(f"New loan '{loan_name}' added successfully!")

                # Reset state
                st.session_state["reset_new_loan_state"] = True
                time.sleep(2)
                st.rerun()

    # Update Existing Loan
    elif add_or_update == "Update existing loan":
        st.write("### Update Existing Loan")
        loan_names = [loan["loan_name"] for loan in loan_accounts]
        selected_loan = st.selectbox("Select Loan to Update", [""] + loan_names, key="select_update_loan")

        if selected_loan:
            if st.session_state.get("last_selected_loan") != selected_loan:
                loan_data = next(loan for loan in loan_accounts if loan["loan_name"] == selected_loan)
                st.session_state["update_loan_name"] = loan_data["loan_name"]
                st.session_state["update_loan_initial_amount"] = loan_data["initial_amount"]
                st.session_state["update_loan_amount_left"] = loan_data["amount_left"]
                try:
                    st.session_state["update_loan_start_date"] = datetime.date.fromisoformat(loan_data["start_date"])
                    st.session_state["update_loan_end_date"] = datetime.date.fromisoformat(loan_data["end_date"])
                except ValueError:
                    st.session_state["update_loan_start_date"] = datetime.date.today()
                    st.session_state["update_loan_end_date"] = datetime.date.today()
                st.session_state["update_loan_monthly_payment"] = loan_data["monthly_payment"]
                st.session_state["update_loan_interest"] = loan_data["interest_rate"]
                st.session_state["last_selected_loan"] = selected_loan

            # Input fields bound to session state
            loan_name = st.text_input("Loan Name", key="update_loan_name")
            loan_initial_amount = st.number_input("Initial Loan Amount", min_value=0.00, key="update_loan_initial_amount")
            loan_amount_left = st.number_input("Loan Amount Left", min_value=0.00, key="update_loan_amount_left")
            loan_start_date = st.date_input("Loan Start Date", key="update_loan_start_date")
            loan_end_date = st.date_input("Loan End Date", key="update_loan_end_date")
            loan_monthly_payment = st.number_input("Monthly Payment", min_value=0.00, key="update_loan_monthly_payment")
            loan_interest = st.number_input("Interest Rate (APR%)", min_value=0.00, key="update_loan_interest")

            # Save updates
            if st.button("Update Loan", key="update_loan_save"):
                updated_data = {
                    "loan_name": st.session_state["update_loan_name"],
                    "initial_amount": st.session_state["update_loan_initial_amount"],
                    "amount_left": st.session_state["update_loan_amount_left"],
                    "start_date": str(st.session_state["update_loan_start_date"]),
                    "end_date": str(st.session_state["update_loan_end_date"]),
                    "monthly_payment": st.session_state["update_loan_monthly_payment"],
                    "interest_rate": st.session_state["update_loan_interest"],
                }
                db_conn.update_loan_account(username, selected_loan, updated_data)  # Update loan in DB
                st.success(f"Loan '{selected_loan}' updated successfully!")

                # Reset state
                st.session_state["reset_update_loan_state"] = True
                time.sleep(2)
                st.rerun()

    # Delete Loan
    elif add_or_update == "Delete loan":
        st.write("### Delete Loan")
        loan_names = [loan["loan_name"] for loan in loan_accounts]
        selected_loan = st.selectbox("Select Loan to Delete", [""] + loan_names, key="select_delete_loan")

        if selected_loan:
            if st.button("Confirm Delete", key="delete_loan"):
                db_conn.delete_loan_account(username, selected_loan)  # Delete loan in DB
                st.success(f"Loan '{selected_loan}' deleted successfully!")
                time.sleep(2)
                st.rerun()
