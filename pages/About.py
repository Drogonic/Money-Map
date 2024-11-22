from PIL import Image
import streamlit as st
import helpperFunctions

helpperFunctions.hide_sidebar()

logo = "MoneyMapLogo.png"  # Replace with the path to your logo file


col1, col2, col3 = st.columns([1, 7, 1])

with col1:
    st.image(logo, width=70)

with col2:
    st.markdown("<h1 style='font-size: 30px;'>Money <span style='color: red;'>Map</span></h1>", unsafe_allow_html=True)

with col3:
    if st.button("Login"):
        st.switch_page("pages/Homepage.py")


st.markdown("<h1 style='text-align: center;'>About Us</h1>", unsafe_allow_html=True)

st.markdown("""
    <p style='text-align: center; font-size: 18px;'>
        Money Map is your ultimate budgeting companion, designed to help you take control of your finances. 
        Track your income and expenses effortlessly while gaining a clear picture of your spending-to-income 
        ratio. With features like loan calculators, spending and income trend analysis, real-time currency 
        exchange rates, and much more, Money Map simplifies financial management and empowers you to make 
        informed decisions.
    </p>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Key Features</h2>", unsafe_allow_html=True)

col3, col4 = st.columns([4, 3])

with col3:
    st.subheader("Currency Exchange")
    st.write("Need to convert currency for travel, business, or curiosity? "
             "Our Currency Exchange tool lets you easily check exchange "
             "rates and find out how much your money is worth in any currency "
             "worldwide. Quick, accurate, and user-friendly—your go-to solution "
             "for staying informed on global currency values.")

with col4:
    st.subheader("      ")
    st.image("Coins.png", width=150)

col5, col6 = st.columns([3, 5])

with col5:
    st.subheader("      ")
    st.image("Calculator.png", width=200)

with col6:
    st.subheader("Net Income Ratio Calculator")
    st.write("Keep track of your financial health with our Net Income Ratio feature! "
             "Simply enter your monthly income and expenses, and our tool will calculate "
             "your net income ratio. Based on this, you'll receive tailored recommendations"
             " on how much to save or adjust your spending to stay on track with your financial goals.")


st.subheader("Advanced Financial Tools for Logged-In Users")
st.write("Create an account to unlock powerful tools like our Savings and Checking Account Tracker, "
         "Loan Management Tool, and APR/APY Calculator. These features make it easy to monitor your "
         "accounts, manage loans, and track your financial progress to stay on top of your goals.")
st.write("")

col7, col8, col9 = st.columns([3, 3, 3])

with col7:
    st.subheader("    ")

with col8:
    if st.button("Sign up to try it yourself!"):
        st.switch_page("pages/signup.py")


with col9:
    st.subheader("    ")