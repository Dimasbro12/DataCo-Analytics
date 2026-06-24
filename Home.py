import streamlit as st
from Utils import load_transaction_data
import base64

# ======================
# Sidebar Background
# ======================
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

sidebar_bg = get_base64("static/resized_200x900.png")

st.markdown(
    f"""
    <style>
    [data-testid="stSidebar"] {{
        background-image: url("data:image/jpg;base64,{sidebar_bg}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.snow()
st.set_page_config(page_title="Home", layout="wide", page_icon="static/SUPERSTORE.png")
col1, col2 = st.columns([1, 5])

with col1:
    st.image("static/SUPERSTORE.png", width=100)

with col2:
    st.title("DataCo Analytics Dashboard")
    st.write("Selamat datang — pilih halaman di sidebar atau dari menu Pages.")
st.markdown("""
- Customer Analytics 
- Customer Segmentation
- ETL Monitoring
- Executive Dashboard
- Geographic Analytics
- Logistic Analytics
- Product Analytics  
- Product Clustering
- Product Search
- Revenue Forecasting
""")
df = load_transaction_data()
st.dataframe(df)
