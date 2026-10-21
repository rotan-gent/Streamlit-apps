import streamlit as st

st.title("BMI Calculator")

height = st.number_input("Enter your height in meters:", min_value=0.0, step=0.01)
weight = st.number_input("Enter your weight in kg:", min_value=0.0, step=0.01)


def bmi_category(height, weight):
    bmi = weight / (height ** 2)

    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 31.5:
        return "Overweight"
    else:
        return "Obese"


if st.button("Calculate"):
    if height > 0:
        bmi = weight / (height ** 2)
        st.write(f"Your BMI is **{bmi:.2f}** ({bmi_category(height, weight)})")
    else:
        st.error("Please enter a valid height greater than 0.")