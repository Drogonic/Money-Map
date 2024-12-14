Money-Map Project Directory Structure

Overview

The Money-Map project is a financial management tool designed to help users track their income, expenses, and savings goals. This README outlines the directory structure and provides details about the contents of each file and folder.

Root Directory

Files:

AboutUs.py: The main entry point of the application. Run this file to start the application.

requirements.txt: Lists all the dependencies required to run the project. Install them using:

pip install -r requirements.txt

README.txt: Documentation providing an overview of the project and its structure.

finalUML.puml: UML diagram of the project, created with PlantUML.

1. /pages

This directory contains all the modules responsible for managing the application's user interface and pages.

Files:

Homepage.py: Logic and layout for the homepage of the application.

guestPage.py: Manages the content and features available to guest users.

About.py: Handles the "About Us" page functionality.

loggedinUserPage.py: Manages the dashboard for logged-in users.

signup.py: Implements the sign-up process and user registration.

2. Core Functional Files

These files implement the primary functionalities and backend logic of the application.

Files:

checking_account.py: Handles logic related to managing checking accounts.

creditcard_account.py: Manages operations related to credit card accounts.

expenses_account.py: Tracks and reports expenses.

financial_tools.py: Contains utility functions for financial calculations.

helperFunctions.py: Includes reusable helper functions used across the application.

income_account.py: Tracks and manages income data.

loans_account.py: Implements logic for managing loans and repayments.

overview_accounts.py: Provides a summary view of all user accounts and activities.

savings_account.py: Handles the logic for savings accounts.

savings_goals.py: Tracks and manages user-defined savings goals.

smart_accounting.py: Advanced accounting logic and automation features.

test_connection.py: A utility to test database or API connections.

3. Media Files

This section contains images and other visual assets used in the project.

Files:

Calculator.png: Image used for the calculator feature.

Coins.png: Icon representing financial transactions.

MoneyMapLogo.jpg / MoneyMapLogo.png: Logos for the Money-Map project.

piChart.png: Example pie chart image for visualization.


4. Database

Files:

DatabaseConnection.py: Establishes and manages the connection to the database.

Note: If the database requires an SQL dump file, include it in a password-protected zip file and provide the password separately.

