import streamlit as st

from Utils import (
    load_data_quality
)

st.title("🔍 Data Quality Monitoring")

duplicate_df, missing_df, orphan_df = (
    load_data_quality()
)

duplicate_count = (
    duplicate_df.iloc[0]["duplicate_order"]
)

missing_count = (
    missing_df.iloc[0]
    .sum()
)

orphan_count = (
    orphan_df.iloc[0]["orphan_product"]
)

# ======================
# KPI
# ======================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Duplicate Record",
        int(duplicate_count)
    )

with col2:
    st.metric(
        "Missing Value",
        int(missing_count)
    )

with col3:
    st.metric(
        "Orphan Record",
        int(orphan_count)
    )

# ======================
# DETAIL
# ======================

st.subheader(
    "Missing Value Detail"
)

st.dataframe(
    missing_df,
    use_container_width=True
)

# ======================
# STATUS
# ======================

if (
    duplicate_count == 0
    and missing_count == 0
    and orphan_count == 0
):

    st.success(
        "Data Quality Status: GOOD"
    )

else:

    st.warning(
        "Data Quality Status: NEED ATTENTION"
    )