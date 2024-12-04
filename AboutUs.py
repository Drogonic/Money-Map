from PIL import Image
import os
import streamlit as st
import base64
import helpperFunctions

helpperFunctions.hide_sidebar()


def get_base64_image(image_path):
    # Resolve the absolute path dynamically
    abs_path = os.path.join(os.path.dirname(__file__), image_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Image not found at path: {abs_path}")
    with open(abs_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Base64 strings for images
logo_base64 = get_base64_image("MoneyMapLogo.png")
calc_base64 = get_base64_image("Calculator.png")
coins_base64 = get_base64_image("Coins.png")
pie_base64 = get_base64_image("piChart.png")

# Add navigation buttons at the top-right corner using Streamlit
nav_col1, nav_col2, nav_col3 = st.columns([6, 1, 1])

with nav_col2:
    if st.button("About"):
        st.switch_page("pages/About.py")

with nav_col3:
    if st.button("Login"):
        st.switch_page("pages/Homepage.py")

# Create an empty container for layout control
container = st.container()

# Add the logo and title to the container (upper-left corner of the main page)
with container:
    # Define the layout with two columns for logo and title
    col1, col2 = st.columns([1, 5])  # Narrow column for logo, wide column for title

    with col1:
        # Place the logo using base64-encoded image
        st.markdown(
            f"""
            <img src="data:image/png;base64,{logo_base64}" width="100" height="100" />
            """,
            unsafe_allow_html=True,
        )

    with col2:
        # Place the title in the second column
        st.markdown(
            """
            <h1 style="font-size: 2.5em;">
                Money <span style="color: red;">Map</span>
            </h1>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            '<span style="color:gray;">Be mindful of your finances all in one place.</span>',
            unsafe_allow_html=True,
        )

# Continue with the rest of your Streamlit code
st.title("Track. Plan. Prosper.")
st.subheader("Take control of your money.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
- Monthly Income and Expenses Tracking
- Currency Exchange 
- Net Income Calculator
- API and APY Calculator
""")

with col2:
    st.write("Try as a guest for our basic features or log in to have full access to your own money map! ")

col3, col4, col5 = st.columns([2, 1, 2])

with col3:
    if st.button("Continue as a Guest"):
        st.switch_page("pages/guestPage.py")

with col4:
    st.write("OR")

with col5:
    if st.button ("Create an Account Today"):
        st.switch_page("pages/signup.py")

st.write()
st.write()
col6, col7, col8 = st.columns(3)

# Use base64 images inside HTML bubbles
with col6:
    bubble_html = f"""
    <div style="
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 20px;
        margin: 20px auto;
        width: 80%;
        background-color: #f9f9f9;
        text-align: center;
    ">
        <h2 style="color: #4CAF50; font-size: 1.5em; margin-bottom: 10px;">Expense Tracker</h2>
        <img src="data:image/png;base64,{calc_base64}" alt="Calculator Image" style="width: 100px; height: 80px; margin-bottom: 15px;">
        <p style="font-size: 1em; color: #333;">
            Easily calculate your net income by entering your earnings and expenses.
        </p>
    </div>
    """
    st.markdown(bubble_html, unsafe_allow_html=True)

with col7:
    bubble_html = f"""
    <div style="
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 20px;
        margin: 20px auto;
        width: 80%;
        background-color: #f9f9f9;
        text-align: center;
    ">
        <h2 style="color: #4CAF50; font-size: 1.5em; margin-bottom: 10px;">Net Income Calculator</h2>
        <img src="data:image/png;base64,{coins_base64}" alt="Coins Image" style="width: 100px; height: 80px; margin-bottom: 15px;">
        <p style="font-size: 1em; color: #333;">
            Calculate your monthly income and understand your financial trends.
        </p>
    </div>
    """
    st.markdown(bubble_html, unsafe_allow_html=True)

with col8:
    bubble_html = f"""
    <div style="
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 20px;
        margin: 20px auto;
        width: 80%;
        background-color: #f9f9f9;
        text-align: center;
    ">
        <h2 style="color: #4CAF50; font-size: 1.5em; margin-bottom: 10px;">Currency Exchange</h2>
        <img src="data:image/png;base64,{pie_base64}" alt="Pie Chart Image" style="width: 100px; height: 70px; margin-bottom: 15px;">
        <p style="font-size: 1em; color: #333;">
            Get the latest currency exchange rates for smarter financial decisions.
        </p>
    </div>
    """
    st.markdown(bubble_html, unsafe_allow_html=True)

st.subheader("More features reserved for registered members!")
