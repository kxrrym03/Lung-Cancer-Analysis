import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(page_title="Lung Cancer Analysis", layout="wide")

# App title
st.title("Lung Cancer Analysis Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload Lung Cancer CSV file", type="csv")

if uploaded_file is not None:
    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.success("✅ Data loaded successfully!")

    # Dataset overview
    st.header("Dataset Overview")
    st.write(f"Shape of dataset: {df.shape}")

    if st.checkbox("Show raw data"):
        st.subheader("Raw Data")
        st.write(df.head())

    # Data Exploration
    st.header("Data Exploration")

    # Cancer Level Distribution
    if 'Level' in df.columns:
        st.subheader("Cancer Level Distribution")
        fig, ax = plt.subplots(figsize=(8, 5))
        df['Level'].value_counts().plot(kind='pie', autopct='%.2f%%', ax=ax)
        ax.set_ylabel('')
        st.pyplot(fig)
    else:
        st.warning("Column 'Level' not found in dataset.")

    # Age Distribution
    if 'Age' in df.columns:
        st.subheader("Age Distribution")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df['Age'], bins=20, kde=True, ax=ax)
        st.pyplot(fig)
    else:
        st.warning("Column 'Age' not found in dataset.")

    # Interactive Analysis
    st.header("Interactive Analysis")

    # Select column
    numeric_columns = df.select_dtypes(include=['int64', 'float64', 'object']).columns.tolist()
    excluded = ['Patient Id', 'Level']
    options = [col for col in numeric_columns if col not in excluded]

    if options:
        selected_column = st.selectbox("Select a feature to analyze:", options)

        st.subheader(f"Distribution of {selected_column}")
        fig, ax = plt.subplots(figsize=(10, 5))
        try:
            sns.countplot(x=selected_column, data=df, ax=ax)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Could not create plot: {e}")
    else:
        st.warning("No suitable columns available for analysis.")

    # Correlation Heatmap
    if st.button("Show Correlation Heatmap"):
        st.subheader("Correlation Heatmap")
        corr = df.select_dtypes(include=['float64', 'int64']).corr()
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    # About
    st.markdown("""
    ### About This Dashboard
    This interactive dashboard analyzes lung cancer patient data. Key features:
    - Upload your own dataset
    - View distribution of cancer levels
    - Explore relationships between features
    - Generate correlation heatmaps
    """)

else:
    st.warning("⚠️ Please upload a CSV file to begin.")
