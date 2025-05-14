
import streamlit as st
from utils import get_top_gainers, screen_stocks
from sheets import export_to_google_sheet

st.title("Warrior Trading-Style Stock Screener")

df = screen_stocks()

if not df.empty:
    st.dataframe(df)

    if st.button("Export to Google Sheet"):
        export_to_google_sheet(df)
        st.success("Exported to Google Sheet!")
else:
    st.write("No qualifying stocks found.")
