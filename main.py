import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="CaloRhythm",
    page_icon="🥗",
    layout="wide"
)

# 제목 및 소개
st.title("CaloRhythm 🥗")
st.subheader("An Intelligent Nutrition Calculator for Korea")

# 사이드바 메뉴 (기능 선택)
st.sidebar.title("Menu")
menu = st.sidebar.radio(
    "Go to:",
    ["Home", "1. Nutrition Calculator", "2. Quantity Optimizer", "3. Food Discovery"]
)

# --- 메인 화면 (Home) ---
if menu == "Home":
    st.write("### Welcome to CaloRhythm!")
    st.write("This application helps you manage your dietary health effectively.")
    st.info("👈 Select a feature from the sidebar to get started.")

# --- 기능 1: 영양분 계산기 ---
elif menu == "1. Nutrition Calculator":
    st.header("🍽️ Standard Nutrition Calculation")
    st.write("**Feature:** Calculate nutritional breakdown based on ingredients and quantities.")
    st.warning("Development in progress...")

# --- 기능 2: 재료 양 최적화 ---
elif menu == "2. Quantity Optimizer":
    st.header("⚖️ Ingredient Quantity Optimization")
    st.write("**Feature:** Recommend optimal portion sizes to match your nutritional goals.")
    st.warning("Development in progress...")

# --- 기능 3: 영양 성분 검색/추천 ---
elif menu == "3. Food Discovery":
    st.header("🔍 Food Discovery by Nutrient")
    st.write("**Feature:** Filter foods by nutrient density or get random recommendations.")
    st.warning("Development in progress...")

# 저작권/라이선스 푸터
st.sidebar.markdown("---")
st.sidebar.text("Apache License 2.0")