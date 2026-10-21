import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Data Cleaner", page_icon="🧹", layout="wide")

st.title("🧹 CSV Data Cleaner")
st.write("Upload a CSV file and clean missing values or duplicate rows.")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        st.success(f"File loaded successfully: "f"{len(df)} rows × {len(df.columns)} columns")
        st.write("Original Data")
        st.dataframe(df, use_container_width=True, hide_index=True)
        duplicate_count = df.duplicated().sum()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Rows", len(df))

        with col2:
            st.metric("Columns", len(df.columns))

        with col3:
            st.metric("Missing Values", df.isna().sum().sum())

        st.info(f"Duplicate rows found: **{duplicate_count}**")
        st.write("Choose Cleaning Operation")
        option = st.radio("What would you like to do?", ["Delete rows containing NaN", "Delete columns containing NaN", "Fill NaN with mean", "Remove duplicate rows"])

        modified_df = None

        if option == "Delete rows containing NaN":
            if st.button("Delete NaN Rows"):
                modified_df = df.dropna(axis=0)
                removed = len(df) - len(modified_df)
                st.success(f"Successfully deleted {removed} rows containing NaN.")

        elif option == "Delete columns containing NaN":
            if st.button("Delete NaN Columns"):
                modified_df = df.dropna(axis=1)
                removed = len(df.columns) - len(modified_df.columns)
                st.success(f"Successfully deleted {removed} columns containing NaN.")

        elif option == "Fill NaN with mean":
            st.write("NaN values in numeric columns will be replaced with the mean of the non-NaN values.")

            if st.button("Fill NaN Values"):
                modified_df = df.copy()
                numeric_columns = modified_df.select_dtypes(include="number").columns
                filled_count = 0

                for column in numeric_columns:
                    nan_before = modified_df[column].isna().sum()

                    if nan_before > 0:
                        mean_value = modified_df[column].mean()
                        modified_df[column] = (modified_df[column].fillna(mean_value))
                        filled_count += nan_before

                st.success(f"Successfully filled {filled_count} NaN values with column means.")
                remaining_nan = modified_df.isna().sum().sum()

                if remaining_nan > 0:
                    st.warning(f"{remaining_nan} NaN values remain because they are in non-numeric columns.")

        elif option == "Remove duplicate rows":
            st.write("This removes completely duplicated rows and keeps the first occurrence.")

            if duplicate_count == 0:
                st.info("No duplicate rows were found.")

            if st.button("Remove Duplicates"):
                modified_df = df.drop_duplicates(keep="first").reset_index(drop=True)
                removed = len(df) - len(modified_df)
                st.success(f"Successfully removed {removed} duplicate rows.")

        if modified_df is not None:
            st.write("Modified Data")
            st.dataframe(modified_df, use_container_width=True)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Rows", len(modified_df))

            with col2:
                st.metric("Columns", len(modified_df.columns))

            with col3:
                st.metric("Remaining NaN", modified_df.isna().sum().sum())

            st.write(f"Remaining duplicate rows: "f"**{modified_df.duplicated().sum()}**")
            csv_data = modified_df.to_csv(index=False).encode("utf-8")
            st.download_button(label="⬇ Download Modified CSV", data=csv_data, file_name="modified_data.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Error reading or processing the CSV: {e}")