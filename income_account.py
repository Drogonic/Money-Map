import streamlit as st
import DatabaseConnection as db_conn
import datetime


def income_account():
    st.subheader("Manage Income")

    # Fetch existing income for the logged-in user
    if "username" in st.session_state:
        username = st.session_state["username"]
        income_accounts = db_conn.get_income_accounts(username)  # Fetch income from DB
    else:
        st.error("You must be logged in to manage income.")
        income_accounts = []

    # Select option
    add_or_update = st.selectbox(
        "Would you like to?",
        ["", "Add new income", "Update existing income", "Delete income"],
        key="add_or_update_income",
    )

    # Reset state for adding new income
    if "reset_income_state" in st.session_state and st.session_state["reset_income_state"]:
        st.session_state["new_income_name"] = ""
        st.session_state["new_income_amount"] = 0.00
        st.session_state["new_income_date"] = datetime.date.today()
        st.session_state["new_income_recurring"] = False
        st.session_state["new_income_period"] = "Daily"
        st.session_state["reset_income_state"] = False

    # Add New Income
    if add_or_update == "Add new income":
        st.write("### Add New Income")
        income_name = st.text_input("Income Name", key="new_income_name")
        income_amount = st.number_input("Income Amount", min_value=0.00, key="new_income_amount")
        income_date = st.date_input("Income Date", max_value=datetime.date.today(), key="new_income_date")
        is_recurring = st.checkbox("Income Recurring", key="new_income_recurring")
        if is_recurring:
            income_period = st.selectbox("Recurring Period", ["Daily", "Weekly", "Biweekly", "Monthly", "Yearly"], key="new_income_period")
        else:
            income_period = None

        # Save the new income
        if st.button("Save Income"):
            # Check if the income name already exists
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

                # Set reset flag to clear inputs
                st.session_state["reset_income_state"] = True

                # Option to add another income or reload
                if st.button("Add Another Income"):
                    st.rerun()

    # Update Existing Income
    elif add_or_update == "Update existing income":
        st.write("### Update Existing Income")
        income_names = [income["income_name"] for income in income_accounts]
        selected_income = st.selectbox("Select Income to Update", [""] + income_names, key="select_update_income")

        # Reset session state for updating income
        if "reset_update_income" not in st.session_state:
            st.session_state["reset_update_income"] = False

        # Reset state if the reset flag is True
        if st.session_state["reset_update_income"]:
            st.session_state["update_income_name"] = ""
            st.session_state["update_income_amount"] = 0.00
            st.session_state["update_income_date"] = datetime.date.today()
            st.session_state["update_income_recurring"] = False
            st.session_state["update_income_period"] = "Daily"
            st.session_state["reset_update_income"] = False

        # Handle selecting a different income
        if selected_income:
            if "selected_income" not in st.session_state or selected_income != st.session_state["selected_income"]:
                st.session_state["selected_income"] = selected_income
                income_data = next(inc for inc in income_accounts if inc["income_name"] == selected_income)
                st.session_state["update_income_name"] = income_data["income_name"]
                st.session_state["update_income_amount"] = income_data["amount"]
                st.session_state["update_income_date"] = datetime.date.fromisoformat(income_data["date"])
                st.session_state["update_income_recurring"] = income_data["is_recurring"]
                st.session_state["update_income_period"] = income_data.get("period", "Daily")

        # Displaying inputs for the selected income
        if selected_income:
            income_name = st.text_input("Income Name", key="update_income_name")
            income_amount = st.number_input("Income Amount", min_value=0.00, key="update_income_amount")
            income_date = st.date_input("Income Date", key="update_income_date")
            is_recurring = st.checkbox("Income Recurring", key="update_income_recurring")
            if is_recurring:
                income_period = st.selectbox(
                    "Recurring Period", ["Daily", "Weekly", "Biweekly", "Monthly", "Yearly"],
                    key="update_income_period",
                )
            else:
                income_period = None

            # Save updates
            if st.button("Update Income", key="update_income_save"):
                updated_data = {
                    "income_name": st.session_state["update_income_name"],
                    "amount": st.session_state["update_income_amount"],
                    "date": str(st.session_state["update_income_date"]),
                    "is_recurring": st.session_state["update_income_recurring"],
                    "period": st.session_state["update_income_period"],
                }
                db_conn.update_income_account(username, selected_income, updated_data)  # Update income in DB
                st.success(f"Income '{selected_income}' updated successfully!")

                # Reset flag to clear session state
                st.session_state["reset_update_income"] = True

                # Update another income
                if st.button("Update Another Income", key="update_another_income"):
                    st.rerun()

    # Delete Income
    elif add_or_update == "Delete income":
        st.write("### Delete Income")
        income_names = [income["income_name"] for income in income_accounts]
        selected_income = st.selectbox("Select Income to Delete", [""] + income_names, key="select_delete_income")

        if selected_income:
            if st.button("Confirm Delete", key="delete_income"):
                db_conn.delete_income_account(username, selected_income)  # Delete income in DB
                st.success(f"Income '{selected_income}' deleted successfully!")
                if st.button("Delete Another Income", key="delete_another_income"):
                    st.rerun()
