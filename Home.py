import streamlit as st
from Utils import load_transaction_data
st.snow()
st.set_page_config(page_title="Home", layout="wide", page_icon="")
st.title("Home")
st.write("Selamat datang — pilih halaman di sidebar atau dari menu Pages.")
st.markdown("""
- Executive Dashboard: ringkasan KPI & tren  
- Customer Analytics: segmentasi & retensi  
- Product Analytics: performa produk  
- Logistics Analytics: pengiriman & SLA  
- Geographic Analytics: peta & distribusi
""")
df = load_transaction_data()
st.dataframe(df)
