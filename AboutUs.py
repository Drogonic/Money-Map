from PIL import Image
import streamlit as st



def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo


my_logo = add_logo(logo_path="MoneyMapLogo.png", width=100, height=100)

# Add navigation buttons at the top-right corner using Streamlit
nav_col1, nav_col2, nav_col3 = st.columns([6, 1, 1])

with nav_col2:
    if st.button("About"):
        st.write("Redirecting to About Page...")  # Replace with actual navigation
        st.experimental_rerun()  # Replace with st.switch_page("about") for multipage apps

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
        # Place the logo in the first column
        st.image(my_logo)

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
imageCalc = Image.open("Calculator.png")
imageCoins = Image.open("Coins.png")
imagePi = Image.open("PiChart.png")

# Render the HTML in Streamlit
#st.markdown(bubble_html, unsafe_allow_html=True)

#with st.container():
with col6:
        #st.markdown(bubble_html, unsafe_allow_html = True)
        # Display the image inside the bubble
        #st.image(imageCalc, width=100, caption="Feature Image", use_container_width=False)

        # Create the HTML content with the bubble and image inside it
        bubble_html = """
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
        <img src="Calculator.png" alt="Feature Image" style="width: 100px; height: 100px; margin-bottom: 15px;">
        <p style="font-size: 1em; color: #333;">
            Easily calculate your net income by entering your earnings and expenses.
        </p>
    </div>
    """

        # Render the HTML bubble with image inside using Markdown
        st.markdown(bubble_html, unsafe_allow_html=True)

with col7:
    bubble_html = """
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
        <p style="font-size: 1em; color: #333;">
            Easily calculate your net income by entering your earnings and expenses. 
        </p>
    </div>
    """


    # Render the HTML in Streamlit
    st.markdown(bubble_html, unsafe_allow_html=True)

    #st.markdown(" ##### Net Income Ratio Calculator")
with col8:
    bubble_html = """
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
        <img src="https://via.placeholder.com/150" alt="Feature Image" style="width: 100px; height: 100px; margin-bottom: 15px;">
        <p style="font-size: 1em; color: #333;">
            Easily calculate your net income by entering your earnings and expenses. 
        </p>
    </div>
    """

    # Render the HTML in Streamlit
    st.markdown(bubble_html, unsafe_allow_html=True)

    #st.markdown(" ##### Currency Exchange")

st.write("AND MORE!")


