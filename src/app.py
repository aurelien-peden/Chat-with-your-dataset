import streamlit as st
from .data_loader import DataLoader
from .chat_handler import ChatHandler
from .pdf_exporter import PDFExporter


def run_app():
    """
    Streamlit application runner.
    """
    st.title("CSV Chat and Visualization App with PandasAI")

    # Initialize session state for chat history if not exists
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # File uploader
    uploaded_files = st.file_uploader(
        "Upload CSV file(s)", type="csv", accept_multiple_files=True)

    if uploaded_files:
        # Load DataFrames
        dataframes = DataLoader.load_csv_files(uploaded_files)

        # Initialize ChatHandler
        chat_handler = ChatHandler(dataframes)

        # User input for chat
        user_input = st.text_input("Ask a question about your CSV data:")

        if user_input:
            # Process user input
            response = chat_handler.handle_chat(user_input)

            # Update chat history
            st.session_state.chat_history.append(("User", user_input))
            st.session_state.chat_history.append(("AI", response))

            # Display response
            ChatHandler.display_response(response)

        # Display chat history
        st.subheader("Chat History")
        for role, content in st.session_state.chat_history:
            if role == "User":
                st.text(f"User: {content}")
            elif role == "AI":
                ChatHandler.display_response(content)
            elif role == "Plot":
                st.pyplot(content)

        # PDF export button
        if st.button("Export Chat as PDF"):
            pdf_data = PDFExporter.export_chat_history(
                st.session_state.chat_history)
            st.download_button(
                label="Download PDF",
                data=pdf_data,
                file_name="chat_history.pdf",
                mime="application/pdf"
            )
