import time
import streamlit as st
import DatabaseConnection as db_conn
import datetime


def initialize_session_state_expenses():
    default_state = {
        # New expense keys
        "new_expense_name": "",
        "new_expense_amount": 0.00,
        "new_expense_date": datetime.date.today(),
        "new_expense_recurring": False,
        "new_expense_period": "Monthly",
        # Update expense keys
        "update_expense_name": "",
        "update_expense_amount": 0.00,
        "update_expense_date": datetime.date.today(),
        "update_expense_recurring": False,
        "update_expense_period": "Monthly",
        # Selection keys
        "add_or_update_expense_account": "",
        "selected_expense": "",
        "last_selected_expense_account": None,
    }
    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_new_expense_state():
    st.session_state[f"new_expense_name"] = ""
    st.session_state[f"new_expense_amount"] = 0.00
    st.session_state[f"new_expense_date"] = datetime.date.today()
    st.session_state[f"new_expense_recurring"] = False
    st.session_state[f"new_expense_period"] = "Monthly"
    st.session_state[f"reset_new_expense_state"] = False
def reset_update_expense_state():
    st.session_state[f"update_expense_name"] = ""
    st.session_state[f"update_expense_amount"] = 0.00
    st.session_state[f"update_expense_date"] = datetime.date.today()
    st.session_state[f"update_expense_recurring"] = False
    st.session_state[f"update_expense_period"] = "Monthly"
    st.session_state[f"reset_update_expense_state"] = False


def expenses_account():
    initialize_session_state_expenses()  # Initialize session state

    st.subheader("Manage Expenses Accounts")

    # Pull expenses for the logged-in user
    if "username" in st.session_state:
        username = st.session_state["username"]
        expense_accounts = db_conn.get_expense_accounts(username)  # Fetch expenses from DB
    else:
        st.error("You must be logged in to manage expenses.")
        expense_accounts = []

    # Handle reset flags
    if st.session_state.get("reset_new_expense_state", False):
        reset_new_expense_state()
    if st.session_state.get("reset_update_expense_state", False):
        reset_update_expense_state()

    # Select option
    add_or_update = st.selectbox(
        "Would you like to?",
        ["", "Add new expense", "Update existing expense", "Delete expense"],
        key="add_or_update_expense_account"
    )

    # Add New Expense
    if add_or_update == "Add new expense":
        st.write("### Add New Expense")
        expense_name = st.text_input("Expense Name", key="new_expense_name")
        expense_amount = st.number_input("Expense Amount", min_value=0.00, key="new_expense_amount")
        expense_date = st.date_input("Expense Date", max_value=datetime.date.today(), key="new_expense_date")
        is_recurring = st.checkbox("Expense Recurring", key="new_expense_recurring")
        expense_period = st.selectbox(
            "Recurring Period", ["Daily", "Weekly", "Biweekly", "Monthly", "Yearly"],
            key="new_expense_period"
        ) if is_recurring else None

        # Save the new expense
        if st.button("Save Expense", key="save_new_expense"):
            # Check if the expense name already exists
            existing_names = [expense["expense_name"] for expense in expense_accounts]
            if expense_name.strip() in existing_names:
                st.error(f"The expense name '{expense_name}' already exists. Please use a different name.")
            elif expense_name.strip() == "":
                st.error("Expense name cannot be empty.")
            else:
                expense_data = {
                    "expense_name": expense_name.strip(),
                    "amount": expense_amount,
                    "date": str(expense_date),
                    "is_recurring": is_recurring,
                    "period": expense_period,
                }
                db_conn.save_expense_account(username, expense_data)  # Save to database
                st.success(f"New expense '{expense_name}' added successfully!")

                # Set reset flag to clear inputs
                st.session_state["reset_new_expense_state"] = True
                time.sleep(2)
                st.rerun()

    # Update Existing Expense
    elif add_or_update == "Update existing expense":
        st.write("### Update Existing Expense")
        expense_names = [expense["expense_name"] for expense in expense_accounts]

        selected_expense = st.selectbox("Select Expense to Update", [""] + expense_names, key="select_update_expense")

        if selected_expense:
            if st.session_state.get("last_selected_expense_account") != selected_expense:
                expense_data = next(exp for exp in expense_accounts if exp["expense_name"] == selected_expense)

                # Initialize or update session state
                st.session_state["update_expense_name"] = expense_data["expense_name"]
                st.session_state["update_expense_amount"] = expense_data["amount"]
                try:
                    st.session_state["update_expense_date"] = datetime.date.fromisoformat(expense_data["date"])
                except ValueError:
                    st.session_state["update_expense_date"] = datetime.date.today()  # Fallback for invalid dates
                st.session_state["update_expense_recurring"] = expense_data["is_recurring"]
                st.session_state["update_expense_period"] = expense_data["period"]

                st.session_state["last_selected_expense_account"] = selected_expense

            # Input fields bound to session state
            expense_name = st.text_input("Expense Name", key="update_expense_name")
            expense_amount = st.number_input("Expense Amount", min_value=0.00, key="update_expense_amount")
            expense_date = st.date_input(
                "Expense Date",
                value=st.session_state["update_expense_date"],
                max_value=datetime.date.today(),
                key="update_expense_date"
            )
            is_recurring = st.checkbox("Expense Recurring", key="update_expense_recurring")
            expense_period = st.selectbox(
                "Recurring Period", ["Daily", "Weekly", "Biweekly", "Monthly", "Yearly"],
                key="update_expense_period"
            ) if is_recurring else None

            # Save updates
            if st.button("Update Expense", key="update_expense_save"):
                updated_data = {
                    "expense_name": st.session_state["update_expense_name"],
                    "amount": st.session_state["update_expense_amount"],
                    "date": st.session_state["update_expense_date"].isoformat(),
                    "is_recurring": st.session_state["update_expense_recurring"],
                    "period": st.session_state["update_expense_period"],
                }
                db_conn.update_expense_account(username, selected_expense, updated_data)  # Update expense in DB
                st.success(f"Expense '{selected_expense}' updated successfully!")

                # Reset flag to clear session state
                st.session_state["reset_update_expense_state"] = True
                time.sleep(2)
                st.rerun()

    # Delete Expense
    elif add_or_update == "Delete expense":
        st.write("### Delete Expense")
        expense_names = [expense["expense_name"] for expense in expense_accounts]
        selected_expense = st.selectbox("Select Expense to Delete", [""] + expense_names)

        if selected_expense:
            if st.button("Confirm Delete", key="delete_expense"):
                db_conn.delete_expense_account(username, selected_expense)  # Delete expense in DB
                st.success(f"Expense '{selected_expense}' deleted successfully!")
                time.sleep(2)
                st.rerun()
