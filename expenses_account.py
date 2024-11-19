import streamlit as st
import DatabaseConnection as db_conn
import datetime


def expenses_account():
    st.subheader("Manage Expenses")

    # Pull expenses for the logged-in user
    if "username" in st.session_state:
        username = st.session_state["username"]
        expense_accounts = db_conn.get_expense_accounts(username)  # Fetch expenses from DB
    else:
        st.error("You must be logged in to manage expenses.")
        expense_accounts = []

    # Select option
    add_or_update = st.selectbox("Would you like to?",
                                 ["", "Add new expense", "Update existing expense", "Delete expense"],
                                 key="add_or_update_expense")

    # If user is adding another account then reset state
    if "reset_expense_state" in st.session_state and st.session_state["reset_expense_state"]:
        st.session_state["new_expense_name"] = ""
        st.session_state["new_expense_amount"] = 0.00
        st.session_state["new_expense_date"] = datetime.date.today()
        st.session_state["new_expense_recurring"] = False
        st.session_state["new_expense_period"] = "Daily"
        st.session_state["reset_expense_state"] = False  # Turn off the reset flag

    # Add New Expense
    if add_or_update == "Add new expense":
        st.write("### Add New Expense")
        expense_name = st.text_input("Expense Name", key="new_expense_name")
        expense_amount = st.number_input("Expense Amount", min_value=0.00, key="new_expense_amount")
        expense_date = st.date_input("Expense Date", max_value=datetime.date.today(), key="new_expense_date")
        is_recurring = st.checkbox("Expense Recurring", key="new_expense_recurring")
        if is_recurring:
            expense_period = st.selectbox("Recurring Period", ["Daily", "Weekly", "Biweekly", "Monthly", "Yearly"],
                                          key="new_expense_period")
        else:
            expense_period = None

        # Save the new expense
        if st.button("Save Expense"):
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
                st.session_state["reset_expense_state"] = True

                # Option to add another expense or reload
                if st.button("Add Another Expense"):
                    st.rerun()

    # Update Existing Expense
    elif add_or_update == "Update existing expense":
        st.write("### Update Existing Expense")
        expense_names = [expense["expense_name"] for expense in expense_accounts]
        selected_expense = st.selectbox("Select Expense to Update", [""] + expense_names, key="select_update_expense")

        # Reset flag for session state
        if "reset_update_expense" not in st.session_state:
            st.session_state["reset_update_expense"] = False

        # Reset session state if the reset flag is True
        if st.session_state["reset_update_expense"]:
            st.session_state["update_expense_name"] = ""
            st.session_state["update_expense_amount"] = 0.00
            st.session_state["update_expense_date"] = datetime.date.today()
            st.session_state["update_expense_recurring"] = False
            st.session_state["update_expense_period"] = "Daily"
            st.session_state["reset_update_expense"] = False  # Turn off the reset flag

        # Handle selecting a different expense
        if selected_expense:
            if "selected_expense" not in st.session_state or selected_expense != st.session_state["selected_expense"]:
                st.session_state["selected_expense"] = selected_expense
                expense_data = next(exp for exp in expense_accounts if exp["expense_name"] == selected_expense)
                st.session_state["update_expense_name"] = expense_data["expense_name"]
                st.session_state["update_expense_amount"] = expense_data["amount"]
                st.session_state["update_expense_date"] = datetime.date.fromisoformat(expense_data["date"])
                st.session_state["update_expense_recurring"] = expense_data["is_recurring"]
                st.session_state["update_expense_period"] = expense_data.get("period", "Daily")

        # Displaying inputs for the selected expense
        if selected_expense:
            expense_name = st.text_input("Expense Name", key="update_expense_name")
            expense_amount = st.number_input("Expense Amount", min_value=0.00, key="update_expense_amount")
            expense_date = st.date_input("Expense Date", key="update_expense_date")
            is_recurring = st.checkbox("Expense Recurring", key="update_expense_recurring")
            if is_recurring:
                expense_period = st.selectbox(
                    "Recurring Period", ["Daily", "Weekly", "Biweekly", "Monthly", "Yearly"],
                    key="update_expense_period"
                )
            else:
                expense_period = None

            # Save updates
            if st.button("Update Expense", key="update_expense_save"):
                updated_data = {
                    "expense_name": st.session_state["update_expense_name"],
                    "amount": st.session_state["update_expense_amount"],
                    "date": str(st.session_state["update_expense_date"]),
                    "is_recurring": st.session_state["update_expense_recurring"],
                    "period": st.session_state["update_expense_period"],
                }
                db_conn.update_expense_account(username, selected_expense, updated_data)  # Update expense in DB
                st.success(f"Expense '{selected_expense}' updated successfully!")

                # Reset flag to clear session state
                st.session_state["reset_update_expense"] = True

                # Update another expense
                if st.button("Update Another Expense", key="update_another_expense"):
                    st.rerun()

    # Delete Expense
    elif add_or_update == "Delete expense":
        st.write("### Delete Expense")
        expense_names = [expense["expense_name"] for expense in expense_accounts]
        selected_expense = st.selectbox("Select Expense to Delete", [""] + expense_names, key="select_delete_expense")

        if selected_expense:
            if st.button("Confirm Delete", key="delete_expense"):
                db_conn.delete_expense_account(username, selected_expense)  # Delete expense in DB
                st.success(f"Expense '{selected_expense}' deleted successfully!")
                st.rerun()
