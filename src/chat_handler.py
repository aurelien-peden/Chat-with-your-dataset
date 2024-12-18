import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pandasai import SmartDataframe
from langchain_community.llms import Ollama
from typing import Union, List, Tuple


class ChatHandler:
    def __init__(self, dataframes: dict):
        """
        Initialize ChatHandler with loaded DataFrames.

        Args:
            dataframes: Dictionary of DataFrames
        """
        self.llm = Ollama(model="llama3.1")

        # Create SmartDataframe based on number of uploaded files
        if len(dataframes) == 1:
            self.smart_df = SmartDataframe(
                list(dataframes.values())[0],
                config={
                    "llm": self.llm,
                    "custom_whitelisted_dependencies": ["PIL"]
                }
            )
        else:
            self.smart_df = SmartDataframe(
                dataframes,
                config={
                    "llm": self.llm,
                    "custom_whitelisted_dependencies": ["PIL"]
                }
            )

    def handle_chat(self, user_input: str) -> Union[pd.DataFrame, plt.Figure, str]:
        """
        Process user input and generate a response.

        Args:
            user_input: User's query string

        Returns:
            Response from SmartDataframe (DataFrame, Figure, or text)
        """
        try:
            response = self.smart_df.chat(user_input)
            return response

        except Exception as e:
            error_message = f"I'm sorry, I encountered an error: {str(e)}. Could you please rephrase your question or provide more context?"
            return error_message

    @staticmethod
    def display_response(response: Union[pd.DataFrame, plt.Figure, str]):
        """
        Display the response based on its type.

        Args:
            response: Response from chat handler
        """
        if isinstance(response, pd.DataFrame):
            st.dataframe(response)
        elif isinstance(response, plt.Figure):
            st.pyplot(response)
        else:
            st.write(response)
