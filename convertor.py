import streamlit as st
from collections import deque
import json
import os

# --- Page Config ---
st.set_page_config(page_title="🔥 Ultimate Unit Converter", page_icon="🔄", layout="wide")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
        body {background-color: #0d1117;}
        .main {background: rgba(20, 20, 20, 0.95); padding: 30px; border-radius: 15px;}
        h1 {color: #00f2ff; text-align: center; font-weight: bold; text-shadow: 0px 0px 10px #00f2ff;}
        .result-box {background: rgba(0, 242, 255, 0.2); padding: 15px; border-radius: 10px; 
                     text-align: center; font-size: 24px; font-weight: bold; color: #00f2ff; 
                     border: 1px solid #00f2ff; box-shadow: 0px 0px 10px rgba(0, 242, 255, 0.8);}
        .sidebar .block-container {background: #1c1c1c; padding: 20px; border-radius: 10px; 
                                  box-shadow: 0px 0px 10px rgba(0, 212, 255, 0.5);}
        .sidebar .stRadio label {color: #00f2ff; font-size: 18px; font-weight: bold;}
        .category-icon {font-size: 24px; margin-right: 10px;}
        .tab-title {font-size: 20px; font-weight: bold; color: #00f2ff;}
    </style>
""", unsafe_allow_html=True)

# --- File for Storing Comments ---
COMMENTS_FILE = "comments.json"

def load_comments():
    if os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, "r") as file:
            return json.load(file)
    return []

def save_comments(comments):
    with open(COMMENTS_FILE, "w") as file:
        json.dump(comments, file)

comments = load_comments()

# --- Title ---
st.markdown("<h1>🔥 Ultimate Unit Converter</h1>", unsafe_allow_html=True)
st.markdown("<h2>Convert Anything with Style!</h2><hr>", unsafe_allow_html=True)

# --- Conversion Data ---
conversions = {
    "📏 Length": {"Meter": 1, "Kilometer": 1000, "Centimeter": 0.01, "Inch": 0.0254, "Foot": 0.3048},
    "⚖️ Weight": {"Kilogram": 1, "Gram": 0.001, "Pound": 0.453592, "Ounce": 0.0283495},
    "🚀 Speed": {"m/s": 1, "km/h": 0.277778, "mph": 0.44704, "knot": 0.514444},
    "🌡️ Temperature": {"Celsius": lambda x: x, "Fahrenheit": lambda x: (x * 9/5) + 32, "Kelvin": lambda x: x + 273.15},
    "⏳ Time": {"Second": 1, "Minute": 60, "Hour": 3600, "Day": 86400}
}

categories = list(conversions.keys())
history = deque(maxlen=5)  # Store last 5 conversions

# --- Tabs for Categories ---
tabs = st.tabs(categories)
for i, category in enumerate(categories):
    with tabs[i]:
        st.markdown(f"<div class='tab-title'>{category}</div>", unsafe_allow_html=True)
        units = list(conversions[category].keys())
        col1, col2 = st.columns(2)
        from_unit = col1.selectbox("From Unit", units, key=f"from_{category}")
        to_unit = col2.selectbox("To Unit", units, key=f"to_{category}")
        value = st.number_input(f"Enter Value in {from_unit}", min_value=0.0, format="%.2f", key=f"val_{category}")
        
        if value:
            if "Temperature" in category:
                if from_unit == "Celsius":
                    result = conversions[category][to_unit](value)
                elif from_unit == "Fahrenheit":
                    result = (value - 32) * 5/9 if to_unit == "Celsius" else ((value - 32) * 5/9) + 273.15
                elif from_unit == "Kelvin":
                    result = value - 273.15 if to_unit == "Celsius" else ((value - 273.15) * 9/5) + 32
            else:
                result = value * (conversions[category][to_unit] / conversions[category][from_unit])
            
            history.append(f"{value} {from_unit} = {result:.2f} {to_unit}")
            st.markdown(f"<div class='result-box'>{value} {from_unit} = {result:.2f} {to_unit}</div>", unsafe_allow_html=True)

# --- Sidebar Enhancements ---
st.sidebar.header("🕒 Conversion History")
st.sidebar.markdown("<br>".join(history) if history else "No history yet.", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.header("💬 User Comments")
name = st.sidebar.text_input("Your Name:")
comment = st.sidebar.text_area("Leave a comment:")
if st.sidebar.button("Submit Comment"):
    if name and comment:
        comments.append(f"**{name}:** {comment}")
        save_comments(comments)
        st.sidebar.success("Comment added!")
        st.rerun()
    else:
        st.sidebar.error("Please enter both name and comment before submitting.")

st.sidebar.markdown("### Recent Comments")
for i, comment in enumerate(comments):
    st.sidebar.markdown(comment, unsafe_allow_html=True)
    if st.sidebar.button(f"Delete {i+1}", key=f"del_{i}"):
        comments.pop(i)
        save_comments(comments)
        st.rerun()

# --- Footer ---
st.markdown("<br><hr><p style='text-align: center; color: gray;'>🚀 Created with ❤️ using Streamlit | Developed by Muzamil Ahmed</p>", unsafe_allow_html=True)
