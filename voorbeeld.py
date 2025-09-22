import streamlit as st

st.title("My Streamlit App")
st.header("Section Header")
st.subheader("Subsection")
st.text("Plain text")

# Input
name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=0, max_value=120)

# Button
if st.button("Submit"):
    st.write(f"Hello {name}, you are {age} years old.")

# Checkbox
if st.checkbox("Show details"):
    st.write("Details are shown here.")

# Selectbox
option = st.selectbox("Choose an option", ["A", "B", "C"])
st.write("You selected:", option)

# Slider
value = st.slider("Pick a number", 0, 100, 50)
st.write("Slider value:", value)

# Chart
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
st.line_chart(df)
