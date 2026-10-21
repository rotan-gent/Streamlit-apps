import pandas as pd
import streamlit as st

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'submit' not in st.session_state:
    st.session_state['submit'] = 'false'
if 'cart' not in st.session_state:
    st.session_state['cart'] = {'abc': [0, 100], 'def': [0, 200], 'ghi': [0, 300], 'jkl': [0, 400], 'mno': [0, 500]}

if not st.session_state['logged_in']:
    st.title("Login")
    if st.button("Login"):
        if st.text_input("Username") == "admin" and st.text_input("Password", type="password") == "1234":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Invalid username or password")
    st.stop()
    
cart = st.session_state['cart']

if st.button("Logout"):
    st.session_state['logged_in'] = False
    st.rerun()

addition = st.selectbox("Choose a product to add:", list(cart.keys()), key="add_selectbox")

if st.button("Add to Cart", key="add_btn"):
    st.session_state['submit'] = 'true'
    cart[addition][0] += 1

cart_df = pd.DataFrame({prod: values for prod, values in cart.items() if values[0] > 0},index=['Quantity', 'Rate'])

if not cart_df.empty:
    st.table(cart_df)
else:
    st.write("Your cart is empty.")

st.metric("My Cart Total", value=sum(qty * price for qty, price in cart.values()))

products = [prod for prod, values in cart.items() if values[0] > 0]
removal = st.selectbox("Choose a product to remove:", products, key="remove_selectbox")

if st.button("Remove from Cart", key="rem_btn"):
    cart[removal][0] = max(0, cart[removal][0] - 1)
    st.rerun()

if st.button("Clear cart"):
    for i in products:
        cart[i][0] = 0
    st.rerun()