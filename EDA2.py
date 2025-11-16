"""
simple_streamlit_eda_matplotlib.py
(Updated: Plot controls appear BELOW upload, not in sidebar)
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="EDA Application", layout="wide", page_icon="📈")

st.title("📈 EDA Application")
st.write("Upload Your Data File And Visualize Instantly")

# -----------------------
# 1. Upload CSV
# -----------------------
uploaded_file = st.file_uploader("📂 Upload Your CSV File", type=["csv"])

if uploaded_file is None:
    st.info("Please upload a CSV file to continue.")
    st.stop()

# -----------------------
# 2. Read DataFrame
# -----------------------
try:
    df = pd.read_csv(uploaded_file)
    bool_cols = df.select_dtypes(include=["bool"]).columns
    if len(bool_cols) > 0:
        df[bool_cols] = df[bool_cols].astype(str)
except Exception as e:
    st.error("Could not read the CSV. Please check the file format.")
    st.exception(e)
    st.stop()

cols = df.columns.tolist()
if len(cols) < 2:
    st.error("Dataset must have at least 2 columns for plotting.")
    st.stop()

# -----------------------
# 3. Show Data Preview
# -----------------------
st.subheader("📄 Data Preview")
st.dataframe(df.head())

# -----------------------
# 4. Plot Controls (NOW BELOW UPLOAD)
# -----------------------
st.subheader("📊 Plot Controls")
col1, col2 = st.columns(2)

with col1:
    x_axis = st.selectbox("X Axis : Select Column", cols, index=0)
with col2:
    y_axis = st.selectbox("Y Axis : Select Column", cols, index=1 if len(cols) > 1 else 0)

plot_buttons_col = st.columns(2)
line_btn = plot_buttons_col[0].button("Click Here For Line Graph")
bar_btn = plot_buttons_col[1].button("Click Here For Bar Chart")

# -----------------------
# 5. Prepare Plot Data
# -----------------------
plot_df = df[[x_axis, y_axis]].dropna().copy()

try:
    plot_df[x_axis] = pd.to_datetime(plot_df[x_axis])
except Exception:
    pass

# -----------------------
# 6. Plotting Functions
# -----------------------
def plot_line():
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(plot_df[x_axis], plot_df[y_axis], marker="o")
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(f"Line Graph: {y_axis} vs {x_axis}")
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)


def plot_bar():
    fig, ax = plt.subplots(figsize=(8, 4))

    if pd.api.types.is_numeric_dtype(plot_df[x_axis]):
        ax.bar(plot_df[x_axis].astype(str), plot_df[y_axis])
    else:
        agg = plot_df.groupby(x_axis)[y_axis].mean().reset_index()
        ax.bar(agg[x_axis].astype(str), agg[y_axis])

    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(f"Bar Chart: {y_axis} vs {x_axis}")
    ax.grid(True)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)

# -----------------------
# 7. Execute Plot
# -----------------------
if line_btn:
    if plot_df.empty:
        st.warning("No data to plot.")
    else:
        plot_line()

if bar_btn:
    if plot_df.empty:
        st.warning("No data to plot.")
    else:
        plot_bar()

st.caption("Matplotlib version — simple, clean, and centered controls.")