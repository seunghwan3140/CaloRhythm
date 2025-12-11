import os
import streamlit as st
import pandas as pd
import altair as alt
from scipy.optimize import minimize
import math

# 1. Page Configuration
st.set_page_config(
    page_title="CaloRhythm",
    page_icon="🥗",
    layout="wide"
)

# 2. Smart Data Loader Function
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data.xlsx') 
    
    # Define mapping: English Key -> Actual Excel Headers (Must match raw data)
    required_keywords = {
        'Food Name': ['식품명', '식품이름'],
        'Energy': ['에너지', '열량'],
        'Carbohydrate': ['탄수화물'],
        'Protein': ['단백질'],
        'Fat': ['지방'],
        'Sodium': ['나트륨'],
        'Sugar': ['당류', '총당류']
    }
    
    try:
        # Read Excel loosely to find the header row
        df_raw = pd.read_excel(file_path, engine='openpyxl', header=None, nrows=10)
        
        # 🟢 [Updated] Logic translated to English
        # Find the row index using the keywords defined above (avoiding hardcoded Korean strings)
        target_identifiers = required_keywords['Food Name']
        header_row_idx = -1
        
        for i, row in df_raw.iterrows():
            row_str = row.astype(str).values
            # Check if any identifier exists in the current row
            if any(keyword in s for keyword in target_identifiers for s in row_str):
                header_row_idx = i
                break
        
        if header_row_idx == -1:
            st.error("⚠️ Could not find the header row in the Excel file.")
            return pd.DataFrame(), {}

        # Reload with correct header
        df = pd.read_excel(file_path, engine='openpyxl', header=header_row_idx)
        df.columns = df.columns.str.strip()
        
        # Map Columns: English Key -> Actual Excel Column Name
        cols_map = {}
        for key, keywords in required_keywords.items():
            found = False
            for col in df.columns:
                if any(k in col for k in keywords):
                    cols_map[key] = col
                    found = True
                    break
            # Handle missing Sugar column
            if not found and key == 'Sugar':
                df['Sugar(g)'] = 0
                cols_map['Sugar'] = 'Sugar(g)'
        
        final_cols = list(cols_map.values())
        df = df[final_cols]
        
        # Convert numeric columns
        target_keys = ['Energy', 'Carbohydrate', 'Protein', 'Fat', 'Sugar', 'Sodium']
        
        for key in target_keys:
            col_name = cols_map[key]
            # Replace '-' with 0, 'Tr' with 0.01
            df[col_name] = df[col_name].astype(str).replace({'-': '0', 'Tr': '0.01'})
            df[col_name] = pd.to_numeric(df[col_name], errors='coerce').fillna(0)
            
        return df, cols_map
        
    except FileNotFoundError:
        st.error("⚠️ 'data.xlsx' file not found.")
        return pd.DataFrame(), {}
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), {}

# Execute Data Loading
df, cols_map = load_data()


# 3. UI Configuration
st.title("CaloRhythm 🥗")
st.subheader("An Intelligent Nutrition Calculator for Korea")

# Sidebar Menu
st.sidebar.title("Menu")
menu = st.sidebar.radio(
    "Go to:",
    ["Home", "1. Nutrition Calculator", "2. Quantity Optimizer", "3. Food Discovery"]
)

# --- Home Screen ---
if menu == "Home":
    st.write("### Welcome to CaloRhythm!")
    st.info("👈 Select a feature from the left sidebar.")
    
    if not df.empty:
        st.success(f"✅ Data loaded successfully! ({len(df)} food items)")
        with st.expander("📊 Dataset Preview (Top 5)"):
            st.dataframe(df.head())
    else:
        st.error("⚠️ Failed to load data.")

# --- Menu 1: Nutrition Calculator ---
elif menu == "1. Nutrition Calculator":
    st.header("🍽️ Nutrition Calculator (Absolute Amount)")
    st.markdown("""
    Select food items and input quantities to compare your intake with **Korean Daily Nutritional Standards (g)**.
    """)
    
    if df.empty:
        st.warning("Data is missing.")
    else:
        # 1. Search Food
        selected_foods = st.multiselect(
            "🥗 Search and select food items:",
            options=df[cols_map['Food Name']].unique(),
            placeholder="e.g., Rice, Kimchi..."
        )

        if selected_foods:
            st.divider()
            st.subheader("📝 Input Quantity (g)")
            
            food_amounts = {}
            cols = st.columns(2)
            for i, food in enumerate(selected_foods):
                with cols[i % 2]:
                    amount = st.number_input(
                        f"🔹 {food} (g)", 
                        min_value=0, 
                        value=100, 
                        step=10, 
                        key=f"food_{i}"
                    )
                    food_amounts[food] = amount
            
            st.write("") 
            
            # 2. Calculate Button
            if st.button("Start Analysis 🧮", type="primary"):
                total_cal = 0
                total_carb = 0
                total_prot = 0
                total_fat = 0
                
                # Calculation Logic using English Keys
                for food, amount in food_amounts.items():
                    row = df[df[cols_map['Food Name']] == food].iloc[0]
                    ratio = amount / 100.0
                    
                    total_cal += row[cols_map['Energy']] * ratio
                    total_carb += row[cols_map['Carbohydrate']] * ratio
                    total_prot += row[cols_map['Protein']] * ratio
                    total_fat += row[cols_map['Fat']] * ratio

                st.divider()
                st.subheader("📊 Analysis Results")
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total Energy", f"{total_cal:.0f} kcal")
                c2.metric("Carbohydrates", f"{total_carb:.1f} g")
                c3.metric("Protein", f"{total_prot:.1f} g")
                c4.metric("Fat", f"{total_fat:.1f} g")
                
                # Standards
                std_carb = 324.0
                std_prot = 55.0
                std_fat = 54.0
                
                st.write("### ⚖️ Intake vs. Daily Standard (g)")
                
                # Prepare Data
                chart_df = pd.DataFrame({
                    'My Intake (g)': [total_carb, total_prot, total_fat],
                    'Daily Standard (g)': [std_carb, std_prot, std_fat]
                }, index=['Carbohydrate', 'Protein', 'Fat'])
                
                # Altair Chart
                chart_df_melted = chart_df.reset_index().melt('index', var_name='Category', value_name='Amount(g)')
                
                chart = alt.Chart(chart_df_melted).mark_bar().encode(
                    x=alt.X('index', title=None, axis=alt.Axis(labelAngle=0)), 
                    y=alt.Y('Amount(g)'),
                    color='Category',
                    xOffset='Category'
                ).properties(height=350)
                
                st.altair_chart(chart, use_container_width=True)
                
                # Feedback
                st.info(f"""
                **ℹ️ Reference Standards (Adult Daily)** - **Carbs:** {std_carb}g 
                - **Protein:** {std_prot}g 
                - **Fat:** {std_fat}g 
                *(Source: MFDS)*
                """)

                if total_carb > std_carb:
                    st.warning(f"⚠️ Carbs exceed standard by **{total_carb - std_carb:.1f}g**.")
                else:
                    st.warning(f"⚠️ Carbs are **{-total_carb + std_carb:.1f}g** below standard.")
                if total_prot > std_prot:
                    st.warning(f"⚠️ Protein exceeds standard by **{-std_prot + total_prot:.1f}g**.")
                else:
                    st.warning(f"⚠️ Protein is **{std_prot - total_prot:.1f}g** below standard.")
                if total_fat > std_fat:
                    st.warning(f"⚠️ Fat exceeds standard by **{total_fat - std_fat:.1f}g**.")
                else:
                    st.warning(f"⚠️ Fat is **{- total_fat + std_fat:.1f}g** below standard.")

        else:
            st.info("👆 Please select food items first.")

                        
# --- Menu 2: Ingredient Quantity Optimizer ---
elif menu == "2. Quantity Optimizer":
    st.header("⚖️ AI Diet Optimizer")
    st.markdown("""
    Calculates optimal ingredient ratios based on **Limits**, **Minimum Intake**, and **Priorities**.
    """)
    
    try:
        from scipy.optimize import minimize
    except ImportError:
        st.error("scipy library required.")
        st.stop()

    if df.empty:
        st.warning("Data not loaded.")
    else:
        st.divider()

        # 1. Constraints
        st.subheader("🎯 Nutritional Limits (per meal)")
        col1, col2, col3, col4 = st.columns(4)
        with col1: limit_cal = st.number_input("Calories (kcal)", value=500.0, step=50.0)
        with col2: limit_carb = st.number_input("Carbohydrates (g)", value=60.0, step=10.0)
        with col3: limit_prot = st.number_input("Protein (g)", value=30.0, step=5.0)
        with col4: limit_fat = st.number_input("Fat (g)", value=15.0, step=5.0)

        # 2. Select Ingredients
        st.divider()
        selected_foods_opt = st.multiselect(
            "🥗 Select Ingredients:",
            options=df[cols_map['Food Name']].unique(),
            placeholder="e.g., Chicken Breast, Sweet Potato...",
            key="opt_multiselect"
        )

        if selected_foods_opt:
            st.markdown("##### 🔽 Minimum Intake (g)")
            min_amounts = {}
            min_cols = st.columns(3)
            for i, food in enumerate(selected_foods_opt):
                with min_cols[i % 3]:
                    min_val = st.number_input(f"{food} Min", min_value=0.0, step=10.0, key=f"min_{food}")
                    min_amounts[food] = min_val
            
            st.divider()
            
            st.subheader("⭐ Priority Settings")
            priority_mode = st.radio(
                "Select Priority:",
                ["Balanced", "Prioritize Protein 🔥", "Prioritize Carbs 🍚", "Prioritize Fat 🥑", "Fill Calories ⚡"],
                horizontal=True
            )
            
            # Weights
            weights = {'cal': 1, 'carb': 1, 'prot': 1, 'fat': 1}
            
            if "Protein" in priority_mode: weights['prot'] = 100
            elif "Carbs" in priority_mode: weights['carb'] = 100
            elif "Fat" in priority_mode: weights['fat'] = 100
            elif "Calories" in priority_mode: weights['cal'] = 100

            if st.button("Calculate Optimal Ratios 🧩", type="primary"):
                target_data = []
                user_min_bounds = []
                
                # Prepare Data using English Keys
                for food in selected_foods_opt:
                    row = df[df[cols_map['Food Name']] == food].iloc[0]
                    target_data.append({
                        'name': food,
                        'cal': row[cols_map['Energy']] / 100.0,
                        'carb': row[cols_map['Carbohydrate']] / 100.0,
                        'prot': row[cols_map['Protein']] / 100.0,
                        'fat': row[cols_map['Fat']] / 100.0
                    })
                    user_min_bounds.append(min_amounts[food])
                
                n_items = len(target_data)
                
                # Objective Function
                def objective(x):
                    total_cal = sum(x[i] * target_data[i]['cal'] for i in range(n_items))
                    total_carb = sum(x[i] * target_data[i]['carb'] for i in range(n_items))
                    total_prot = sum(x[i] * target_data[i]['prot'] for i in range(n_items))
                    total_fat = sum(x[i] * target_data[i]['fat'] for i in range(n_items))
                    
                    loss = 0
                    loss += weights['cal'] * ((limit_cal - total_cal) / (limit_cal + 1e-6)) ** 2
                    loss += weights['carb'] * ((limit_carb - total_carb) / (limit_carb + 1e-6)) ** 2
                    loss += weights['prot'] * ((limit_prot - total_prot) / (limit_prot + 1e-6)) ** 2
                    loss += weights['fat'] * ((limit_fat - total_fat) / (limit_fat + 1e-6)) ** 2
                    return loss

                # Constraints
                constraints = (
                    {'type': 'ineq', 'fun': lambda x: limit_cal - sum(x[i] * target_data[i]['cal'] for i in range(n_items))},
                    {'type': 'ineq', 'fun': lambda x: limit_carb - sum(x[i] * target_data[i]['carb'] for i in range(n_items))},
                    {'type': 'ineq', 'fun': lambda x: limit_prot - sum(x[i] * target_data[i]['prot'] for i in range(n_items))},
                    {'type': 'ineq', 'fun': lambda x: limit_fat - sum(x[i] * target_data[i]['fat'] for i in range(n_items))}
                )
                
                bounds = [(user_min_bounds[i], 2000) for i in range(n_items)]
                initial_weights = [m + 10.0 for m in user_min_bounds]
                
                try:
                    result = minimize(objective, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
                    
                    final_weights = result.x
                    if any(math.isnan(w) for w in final_weights):
                        st.error("⚠️ Error: Conflicting constraints.")
                    
                    elif result.success:
                        st.success(f"✅ Optimization Successful! ({priority_mode})")
                        
                        cols = st.columns(n_items)
                        total_res = {'cal':0, 'carb':0, 'prot':0, 'fat':0}
                        
                        for idx, (weight, item) in enumerate(zip(final_weights, target_data)):
                            with cols[idx % n_items]:
                                st.info(f"**{item['name']}**")
                                st.markdown(f"## {weight:.0f} g")
                                total_res['cal'] += weight * item['cal']
                                total_res['carb'] += weight * item['carb']
                                total_res['prot'] += weight * item['prot']
                                total_res['fat'] += weight * item['fat']
                        
                        st.divider()
                        
                        # Safe Percentage
                        def safe_percentage(val, limit):
                            if limit == 0: return 0.0
                            return min((val / limit) * 100, 100.0)

                        percentages = [
                            safe_percentage(total_res['cal'], limit_cal),
                            safe_percentage(total_res['carb'], limit_carb),
                            safe_percentage(total_res['prot'], limit_prot),
                            safe_percentage(total_res['fat'], limit_fat)
                        ]
                        
                        chart_df = pd.DataFrame({
                            'Nutrient': ['Calories', 'Carbohydrate', 'Protein', 'Fat'],
                            'Fulfillment(%)': percentages
                        })
                        
                        # Highlighting
                        if "Protein" in priority_mode: 
                            chart_df.loc[chart_df['Nutrient']=='Protein', 'Color'] = '#FF4B4B'
                        elif "Carbs" in priority_mode:
                            chart_df.loc[chart_df['Nutrient']=='Carbohydrate', 'Color'] = '#FF4B4B'
                        else:
                            chart_df['Color'] = '#4CAF50'

                        # Altair Chart
                        chart_opt = alt.Chart(chart_df).mark_bar().encode(
                            x=alt.X('Nutrient', title=None, axis=alt.Axis(labelAngle=0)),
                            y=alt.Y('Fulfillment(%)', scale=alt.Scale(domain=[0, 100])),
                            color=alt.Color('Nutrient', legend=None) if 'Color' not in chart_df else alt.value('#4CAF50'),
                            tooltip=['Nutrient', alt.Tooltip('Fulfillment(%)', format='.1f')]
                        ).properties(height=350)
                        
                        st.altair_chart(chart_opt, use_container_width=True)
                        
                        display_df = pd.DataFrame({
                            'Current Intake': [total_res['cal'], total_res['carb'], total_res['prot'], total_res['fat']],
                            'Set Limit': [limit_cal, limit_carb, limit_prot, limit_fat],
                            'Fulfillment(%)': percentages
                        }, index=['Calories', 'Carbohydrate', 'Protein', 'Fat'])
                        
                        st.table(display_df.style.format("{:.1f}"))
                        
                    else:
                        st.warning("⚠️ Could not find optimal solution.")
                        
                except Exception as e:
                    st.error(f"Error: {e}")

        else:
            st.info("👆 Please select food items.")

# --- Menu 3: Food Discovery ---
elif menu == "3. Food Discovery":
    st.header("🔍 Food Discovery by Nutrient")
    st.markdown("Find foods with the **highest** and **lowest** nutrient content (Per 100g).")
    
    if df.empty:
        st.warning("Data not loaded.")
    else:
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            nutrient_select = st.radio(
                "⚖️ Select Nutrient:", 
                ["Carbohydrate", "Protein", "Fat"], 
                horizontal=True
            )
            # Use English keys directly
            target_key = nutrient_select 

        with col2:
            rank_count = st.slider("📊 Ranking Count:", 3, 100, 10)

        target_col = cols_map[target_key]
        display_cols = [cols_map['Food Name'], target_col, cols_map['Energy']]

        df_high = df.nlargest(rank_count, target_col)[display_cols].reset_index(drop=True)
        df_high.index = df_high.index + 1
        df_low = df.nsmallest(rank_count, target_col)[display_cols].reset_index(drop=True)
        df_low.index = df_low.index + 1

        st.divider()
        col_high, col_low = st.columns(2)
        
        with col_high:
            st.subheader(f"⬆️ Top {rank_count} High in {nutrient_select}")
            st.dataframe(df_high.style.background_gradient(subset=[target_col], cmap="Reds"), use_container_width=True)

        with col_low:
            st.subheader(f"⬇️ Top {rank_count} Low in {nutrient_select}")
            st.dataframe(df_low.style.background_gradient(subset=[target_col], cmap="Blues"), use_container_width=True)
            
        st.info(f"💡 **Tip**: Useful for finding {nutrient_select}-rich or {nutrient_select}-low foods.")
