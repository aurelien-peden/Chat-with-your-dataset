import io
import base64
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from typing import List, Tuple


class PDFExporter:
    @staticmethod
    def export_chat_history(chat_history: List[Tuple[str, object]]) -> bytes:
        """
        Export chat history to a PDF file.

        Args:
            chat_history: List of chat history tuples

        Returns:
            Bytes object of the PDF
        """
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        y = height - 50
        for role, content in chat_history:
            try:
                if role == "User":
                    p.drawString(50, y, f"User: {content}")
                elif role == "AI":
                    if isinstance(content, pd.DataFrame):
                        p.drawString(50, y, "AI: [DataFrame output]")
                    elif isinstance(content, plt.Figure):
                        img_data = io.BytesIO()
                        content.savefig(img_data, format='png')
                        img_data.seek(0)
                        img = base64.b64encode(img_data.getvalue()).decode()
                        p.drawImage(
                            f"data:image/png;base64,{img}", 50, y - 200, width=400, height=200)
                        y -= 200
                    else:
                        p.drawString(50, y, f"AI: {content}")
                elif role == "Plot":
                    img_data = io.BytesIO()
                    content.savefig(img_data, format='png')
                    img_data.seek(0)
                    img = base64.b64encode(img_data.getvalue()).decode()
                    p.drawImage(
                        f"data:image/png;base64,{img}", 50, y - 200, width=400, height=200)
                    y -= 200

                y -= 20
                if y < 50:
                    p.showPage()
                    y = height - 50

            except Exception as e:
                st.error(f"Error exporting chat history item: {str(e)}")

        p.save()
        buffer.seek(0)
        return buffer.getvalue()
