import streamlit as st

st.set_page_config(layout="wide")
# Sidebar
st.sidebar.title("Range")
range_value = st.sidebar.slider("Max Delay (mins)", min_value=0, max_value=100, value=50)




st.image("airplane.png", use_container_width=True)

# Grid layout
col1, col2 = st.columns(2)
col1.text_input("Departure Airport")
col2.text_input("Arrival Airport")

col3, col4 = st.columns(2)
col3.text_input("Departure Date")
col4.text_input("Departure Time")

col5, col6 = st.columns(2)
col5.text_input("Airlines")
# col6.text_input("Input Field 6")
