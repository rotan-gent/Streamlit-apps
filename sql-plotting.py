import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import streamlit as st


@st.cache_resource
def get_in_memory_connection():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    pd.DataFrame({"Name": ["Aarav Sharma", "Ananya Verma", "Rohan Gupta", "Priya Singh", "Kabir Patel", 
                 "Neha Iyer", "Aditya Kumar", "Sneha Rao", "Vikram Malhotra", "Meera Joshi"],
        "Branch": ["CSE", "ECE", "CSE", "Mechanical", "CSE", "ECE", "Civil", "Mechanical", "CSE", "Civil"],
        "Gender": ["Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Female"],
        "Attendance": [85.5, 90.2, 78.4, 65.0, 92.1, 88.3, 74.5, 81.0, 95.6, 69.2],
        "Marks": [88.5, 92.0, 76.0, 58.5, 95.0, 89.0, 70.0, 82.5, 98.0, 64.0]}).to_sql("students", conn, index=False)
    return conn


df = pd.read_sql("SELECT * FROM students;", get_in_memory_connection())

st.title("Student Data Portal")

st.sidebar.header("Filters")
min_, max_ = float(df["Attendance"].min()), float(df["Attendance"].max())
attendance = st.sidebar.slider("Attendance Range", min_, max_, (min_, max_))

df = df[(df["Branch"].isin(st.sidebar.multiselect("Branch", options=df["Branch"].unique(), default=df["Branch"].unique()))) & (df["Gender"].isin(st.sidebar.multiselect("Gender", options=df["Gender"].unique(), default=df["Gender"].unique()))) & (df["Attendance"] >= attendance[0]) & (df["Attendance"] <= attendance[1])]

total = len(df)

c1, c2, c3 = st.columns(3)
c1.metric("Total Students", total)
c2.metric("Average Attendance", f"{df['Attendance'].mean() if total > 0 else 0:.2f}%")
c3.metric("Average Marks", f"{df['Marks'].mean() if total > 0 else 0:.2f}")

st.dataframe(df, hide_index=True)

conn_f = sqlite3.connect(":memory:")
df.to_sql("filtered_students", conn_f, index=False, if_exists="replace")

st.write("Branch-wise Average Marks")
fig1, ax1 = plt.subplots()
fig1.patch.set_facecolor("#0E1117")
ax1.set_facecolor("#0E1117")
brarks = pd.read_sql("SELECT Branch, AVG(Marks) AS Avg_Marks FROM filtered_students GROUP BY Branch;", conn_f)
ax1.bar(brarks["Branch"], brarks["Avg_Marks"], color="#FF4B4B")
ax1.set_xlabel("Branch", color="white")
ax1.set_ylabel("Marks", color="white")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["bottom"].set_color("white")
ax1.spines["left"].set_color("white")
ax1.tick_params(axis="x", colors="white")
ax1.tick_params(axis="y", colors="white")
st.pyplot(fig1)

st.write("Branch-wise Average Attendance")
fig2, ax2 = plt.subplots()
fig2.patch.set_facecolor("#0E1117")
ax2.set_facecolor("#0E1117")
brance = pd.read_sql("SELECT Branch, AVG(Attendance) AS Avg_Attendance FROM filtered_students GROUP BY Branch;", conn_f)
ax2.bar(brance["Branch"], brance["Avg_Attendance"], color="#FF4B4B")
ax2.set_xlabel("Branch", color="white")
ax2.set_ylabel("Attendance", color="white")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["bottom"].set_color("white")
ax2.spines["left"].set_color("white")
ax2.tick_params(axis="x", colors="white")
ax2.tick_params(axis="y", colors="white")
st.pyplot(fig2)

st.write("Top 5 Students")
fig3, ax3 = plt.subplots()
fig3.patch.set_facecolor("#0E1117")
ax3.set_facecolor("#0E1117")
top = pd.read_sql("SELECT * FROM filtered_students ORDER BY Marks DESC LIMIT 5;", conn_f)
ax3.bar(top["Name"], top["Marks"], color="#FF4B4B")
ax3.set_xlabel("Name", color="white")
ax3.set_ylabel("Marks", color="white")
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.spines["bottom"].set_color("white")
ax3.spines["left"].set_color("white")
ax3.tick_params(axis="x", colors="white")
ax3.tick_params(axis="y", colors="white")
st.pyplot(fig3)

st.write("Gender-wise Student Count")
fig4, ax4 = plt.subplots()
fig4.patch.set_facecolor("#0E1117")
ax4.set_facecolor("#0E1117")
count = pd.read_sql("SELECT Gender, COUNT(*) AS cnt FROM filtered_students GROUP BY Gender;", conn_f)
pie_colors = ["#FF4B4B" if str(c).lower() == "female" else "#00B4B4" for c in count["Gender"]]
ax4.pie(count["cnt"], labels=count["Gender"], autopct="%1.1f%%", colors=pie_colors, textprops={"color": "white"})
st.pyplot(fig4)