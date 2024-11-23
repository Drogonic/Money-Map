import time
import streamlit as st
import DatabaseConnection as db_conn
import datetime
import plotly.graph_objects as go


def initialize_session_state_goals():
    default_state = {
        # New goal keys
        "new_goal_name": "",
        "new_goal_target": 0.00,
        "new_goal_date": datetime.date.today(),
        # Update goal keys
        "update_goal_name": "",
        "update_goal_target": 0.00,
        "update_goal_date": datetime.date.today(),
        # Selection keys
        "add_or_update_goal": "",
        "selected_goal": "",
        "last_selected_goal": None,
    }
    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_new_goal_state():
    st.session_state["new_goal_name"] = ""
    st.session_state["new_goal_target"] = 0.00
    st.session_state["new_goal_date"] = datetime.date.today()
    st.session_state["reset_new_goal_state"] = False


def reset_update_goal_state():
    st.session_state["update_goal_name"] = ""
    st.session_state["update_goal_target"] = 0.00
    st.session_state["update_goal_date"] = datetime.date.today()
    st.session_state["reset_update_goal_state"] = False


def savings_goal_tracker(username):
    initialize_session_state_goals()

    st.subheader("Manage Savings Goals")

    # Fetch savings goals for the user
    savings_goals = db_conn.get_savings_goals(username)
    savings_accounts = db_conn.get_savings_accounts(username)

    # Calculate total savings balance
    total_savings = sum(account["amount"] for account in savings_accounts)

    # Handle reset flags
    if st.session_state.get("reset_new_goal_state", False):
        reset_new_goal_state()
    if st.session_state.get("reset_update_goal_state", False):
        reset_update_goal_state()

    # Select option
    add_or_update = st.selectbox(
        "Would you like to?",
        ["", "Add new goal", "Update existing goal", "Delete goal", "View Progress"],
        key="add_or_update_goal"
    )

    # Add New Goal
    if add_or_update == "Add new goal":
        st.write("### Add New Goal")
        goal_name = st.text_input("Goal Name", key="new_goal_name")
        target_amount = st.number_input("Target Amount ($)", min_value=0.00, key="new_goal_target")
        target_date = st.date_input(
            "Target Date",
            value=max(datetime.date.today() + datetime.timedelta(days=1),
                      datetime.date.today() + datetime.timedelta(days=1)),
            min_value=datetime.date.today() + datetime.timedelta(days=1),
            max_value=datetime.date.today().replace(year=datetime.date.today().year + 10),
            key="new_goal_date"
        )

        if st.button("Save Goal", key="save_new_goal"):
            existing_names = [goal["goal_name"] for goal in savings_goals]
            if goal_name.strip() in existing_names:
                st.error(f"The goal name '{goal_name}' already exists. Please use a different name.")
            elif goal_name.strip() == "":
                st.error("Goal name cannot be empty.")
            else:
                goal_data = {
                    "goal_name": goal_name.strip(),
                    "target_amount": target_amount,
                    "target_date": target_date.isoformat(),
                }
                db_conn.save_savings_goal(username, goal_data)
                st.success(f"New savings goal '{goal_name}' added successfully!")
                st.session_state["reset_new_goal_state"] = True
                time.sleep(2)
                st.rerun()

    # Update Existing Goal
    elif add_or_update == "Update existing goal":
        st.write("### Update Existing Goal")
        goal_names = [goal["goal_name"] for goal in savings_goals]

        selected_goal = st.selectbox("Select Goal to Update", [""] + goal_names, key="select_update_goal")

        if selected_goal:
            if st.session_state.get("last_selected_goal") != selected_goal:
                goal_data = next(goal for goal in savings_goals if goal["goal_name"] == selected_goal)

                st.session_state["update_goal_name"] = goal_data["goal_name"]
                st.session_state["update_goal_target"] = goal_data["target_amount"]
                st.session_state["update_goal_date"] = datetime.date.fromisoformat(goal_data["target_date"])

                st.session_state["last_selected_goal"] = selected_goal

            goal_name = st.text_input("Goal Name", key="update_goal_name")
            target_amount = st.number_input("Target Amount ($)", min_value=0.00, key="update_goal_target")
            target_date = st.date_input(
                "Target Date",
                min_value=datetime.date.today(),
                key="update_goal_date"
            )

            if st.button("Update Goal", key="update_goal_save"):
                updated_data = {
                    "goal_name": st.session_state["update_goal_name"],
                    "target_amount": st.session_state["update_goal_target"],
                    "target_date": st.session_state["update_goal_date"].isoformat(),
                }
                db_conn.update_savings_goal(username, selected_goal, updated_data)
                st.success(f"Savings goal '{selected_goal}' updated successfully!")
                st.session_state["reset_update_goal_state"] = True
                time.sleep(2)
                st.rerun()

    # Delete Goal
    elif add_or_update == "Delete goal":
        st.write("### Delete Goal")
        goal_names = [goal["goal_name"] for goal in savings_goals]
        selected_goal = st.selectbox("Select Goal to Delete", [""] + goal_names)

        if selected_goal:
            if st.button("Confirm Delete", key="delete_goal"):
                db_conn.delete_savings_goal(username, selected_goal)
                st.success(f"Savings goal '{selected_goal}' deleted successfully!")
                time.sleep(2)
                st.rerun()

    # View Progress
    elif add_or_update == "View Progress":
        if not savings_goals:
            st.info("No savings goals found. Please add a goal to view progress.")
            return

        st.write("### Savings Goals Progress")
        goal_names = [goal["goal_name"] for goal in savings_goals]
        selected_goal = st.selectbox("Select Goal to View Progress", [""] + goal_names)

        if selected_goal:
            goal_data = next(goal for goal in savings_goals if goal["goal_name"] == selected_goal)

            # Calculate progress
            current_progress = min(total_savings, goal_data["target_amount"])
            remaining = max(0, goal_data["target_amount"] - current_progress)
            months_left = max(
                (datetime.date.fromisoformat(goal_data["target_date"]) - datetime.date.today()).days // 30, 1)
            suggested_monthly_savings = remaining / months_left if months_left > 0 else 0
            progress_percentage = min((current_progress / goal_data["target_amount"]) * 100, 100)

            # Display progress using progress bar
            st.write(f"**Progress for Goal: {goal_data['goal_name']}**")
            st.progress(progress_percentage / 100)
            st.write(f"Progress: {progress_percentage:.2f}%")

            # Display detailed progress information
            st.write(f"- **Goal Name:** {goal_data['goal_name']}")
            st.write(f"- **Total Target:** ${goal_data['target_amount']:.2f}")
            st.write(f"- **Current Savings Balance:** ${total_savings:.2f}")
            st.write(f"- **Remaining Amount:** ${remaining:.2f}")
            st.write(f"- **Months Left:** {months_left} months")
            st.write(f"- **Suggested Monthly Savings:** ${suggested_monthly_savings:.2f}")
            st.write(f"- **Goal End Date:** {goal_data['target_date']}")
