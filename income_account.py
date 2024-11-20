import time
import streamlit as st
import DatabaseConnection as db_conn
import datetime


def initialize_session_state_income():
    default_state = {
        # New income keys
        "new_income_name": "",
        "new_income_amount": 0.00,
        "new_income_date": datetime.date.today(),
        "new_income_recurring": False,
        "new_income_period": "Monthly",
        # Update income keys
        "update_income_name": "",
        "update_income_amount": 0.00,
        "update_income_date": datetime.date.today(),
        "update_income_recurring": False,
        "update_income_period": "Monthly",
        # Selection keys
        "add_or_update_income": "",
        "selected_income": "",
        "last_selected_income": None,
    }
    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_new_income_state():
    st.session_state[f"new_income_name"] = ""
    st.session_state[f"new_income_amount"] = 0.00
    st.session_state[f"new_income_date"] = datetime.date.today()
    st.session_state[f"new_income_recurring"] = False
    st.session_state[f"new_income_period"] = "Monthly"
    st.session_state[f"reset_new_income_state"] = False

def reset_update_income_state():
    st.session_state[f"update_income_name"] = ""
    st.session_state[f"update_income_amount"] = 0.00
    st.session_state[f"update_income_date"] = datetime.date.today()
    st.session_state[f"update_income_recurring"] = False
    st.session_state[f"update_income_period"] = "Monthly"
    st.session_state[f"reset_update_income_state"] = False


def income_account():
    initialize_session_state_income()  # Initialize session state

    st.subheader("Manage Income")

    # Fetch existing income for the logged-in user
    if "username" in st.session_state:
        username = st.session_state["username"]
        income_accounts = db_conn.get_income_accounts(username)  # Fetch income from DB
    else:
        st.error("You must be logged in to manage income.")
        return

    # Handle reset flags
    if st.session_state.get("reset_new_income_state", False):
        reset_new_income_state()
    if st.session_state.get("reset_update_income_state", False):
        reset_update_income_state()

    # Select option
    add_or_update = st.selectbox(
        "Would you like to?",
        ["", "Add new income", "Update existing income", "Delete income"],
        key="add_or_update_income"
    )

    # Add New Income
    if add_or_update == "Add new income":
        st.write("### Add New Income")
        income_name = st.text_input("Income Name", key="new_income_name")
        income_amount = st.number_input("Income Amount", min_value=0.00, key="new_income_amount")
        income_date = st.date_input("Income Date", max_value=datetime.date.today(), key="new_income_date")
        is_recurring = st.checkbox("Income Recurring", key="new_income_recurring")
        income_period = st.selectbox(
            "Recurring Period", ["Daily", "Weekly", "Biweekly", "Monthly", "Yearly"],
            key="new_income_period"
        ) if is_recurring else None

        # Save the new income
        if st.button("Save Income", key="save_new_income"):
            existing_names = [income["income_name"] for income in income_accounts]
            if income_name.strip() in existing_names:
                st.error(f"The income name '{income_name}' already exists. Please use a different name.")
            elif income_name.strip() == "":
                st.error("Income name cannot be empty.")
            else:
                income_data = {
                    "income_name": income_name.strip(),
                    "amount": income_amount,
                    "date": str(income_date),
                    "is_recurring": is_recurring,
                    "period": income_period,
                }
                db_conn.save_income_account(username, income_data)  # Save to database
                st.success(f"New income '{income_name}' added successfully!")

                # Update cached data and reset state
                st.session_state["reset_new_income_state"] = True
                time.sleep(2)
                st.rerun()

    # Update Existing Income
    elif add_or_update == "Update existing income":
        st.write("### Update Existing Income")
        income_names = [income["income_name"] for income in income_accounts]
        selected_income = st.selectbox("Select Income to Update", [""] + income_names, key="select_update_income")

        if selected_income:
            if st.session_state.get("last_selected_income") != selected_income:
                income_data = next(inc for inc in income_accounts if inc["income_name"] == selected_income)
                st.session_state["update_income_name"] = income_data["income_name"]
                st.session_state["update_income_amount"] = income_data["amount"]
                try:
                    st.session_state["update_income_date"] = datetime.date.fromisoformat(income_data["date"])
                except ValueError:
                    st.session_state["update_income_date"] = datetime.date.today()
                st.session_state["update_income_recurring"] = income_data["is_recurring"]
                st.session_state["update_income_period"] = income_data.get("period", "Monthly")
                st.session_state["last_selected_income"] = selected_income

            # Input fields bound to session state
            income_name = st.text_input("Income Name", key="update_income_name")
            income_amount = st.number_input("Income Amount", min_value=0.00, key="update_income_amount")
            income_date = st.date_input(
                "Income Date",
                value=st.session_state["update_income_date"],
                max_value=datetime.date.today(),
                key="update_income_date"
            )
            is_recurring = st.checkbox("Income Recurring", key="update_income_recurring")
            income_period = st.selectbox(
                "Recurring Period", ["Daily", "Weekly", "Biweekly", "Monthly", "Yearly"],
                key="update_income_period"
            ) if is_recurring else None

            # Save updates
            if st.button("Update Income", key="update_income_save"):
                updated_data = {
                    "income_name": st.session_state["update_income_name"],
                    "amount": st.session_state["update_income_amount"],
                    "date": st.session_state["update_income_date"].isoformat(),
                    "is_recurring": st.session_state["update_income_recurring"],
                    "period": st.session_state["update_income_period"],
                }
                db_conn.update_income_account(username, selected_income, updated_data)
                st.success(f"Income '{selected_income}' updated successfully!")

                # Reset state
                st.session_state["reset_update_income_state"] = True
                time.sleep(2)
                st.rerun()

    # Delete Income
    elif add_or_update == "Delete income":
        st.write("### Delete Income")
        income_names = [income["income_name"] for income in income_accounts]
        selected_income = st.selectbox("Select Income to Delete", [""] + income_names, key="select_delete_income")

        if selected_income:
            if st.button("Confirm Delete", key="delete_income"):
                db_conn.delete_income_account(username, selected_income)
                st.success(f"Income '{selected_income}' deleted successfully!")
                time.sleep(2)
                st.rerun()
