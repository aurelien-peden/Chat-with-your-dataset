import streamlit as st
import pandas as pd
from typing import Dict, Optional


class DataLoader:
    @staticmethod
    def load_csv_files(uploaded_files) -> Dict[str, pd.DataFrame]:
        """
        Load multiple CSV files into a dictionary of DataFrames.

        Args:
            uploaded_files: Streamlit uploaded files

        Returns:
            Dictionary of DataFrames with filenames as keys
        """
        dataframes = {}
        if uploaded_files:
            for file in uploaded_files:
                try:
                    df = pd.read_csv(file)
                    dataframes[file.name] = df

                    # Display preview of each uploaded DataFrame
                    st.subheader(f"Preview of {file.name}")
                    st.write(df.head())
                    st.write(f"Shape: {df.shape}")
                    st.write(f"Columns: {', '.join(df.columns)}")
                    st.write("---")

                except Exception as e:
                    st.error(f"Error loading {file.name}: {str(e)}")

        return dataframes
