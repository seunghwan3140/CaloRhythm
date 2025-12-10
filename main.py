import os
import streamlit as st
import pandas as pd
from scipy.optimize import minimize
import altair as alt # 🟢 [추가] 그래프 글자 방향 제어를 위해 필요

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="CaloRhythm",
    page_icon="🥗",
    layout="wide"
)

# 2. 스마트 데이터 로드 함수
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data.xlsx') # 파일명 data.xlsx 확인
    
    # 필수 컬럼 키워드 정의
    required_keywords = {
        '식품명': ['식품명', '식품이름'],
        '에너지': ['에너지', '열량'],
        '탄수화물': ['탄수화물'],
        '단백질': ['단백질'],
        '지방': ['지방'],
        '나트륨': ['나트륨'],
        '당류': ['당류', '총당류']
    }
    
    try:
        # 엑셀 파일 읽기 (헤더 위치를 모르니 일단 넉넉히 읽음)
        df_raw = pd.read_excel(file_path, engine='openpyxl', header=None, nrows=10)
        
        # '식품명'이라는 단어가 있는 행 번호 찾기
        header_row_idx = -1
        for i, row in df_raw.iterrows():
            row_str = row.astype(str).values
            if any('식품명' in s for s in row_str):
                header_row_idx = i
                break
        
        if header_row_idx == -1:
            st.error("⚠️ 엑셀 파일에서 '식품명' 컬럼을 찾을 수 없습니다.")
            return pd.DataFrame(), {}

        # 찾은 행을 헤더로 하여 다시 읽기
        df = pd.read_excel(file_path, engine='openpyxl', header=header_row_idx)
        
        # 컬럼명 앞뒤 공백 제거
        df.columns = df.columns.str.strip()
        
        # 필요한 컬럼만 쏙 골라내기
        cols_map = {}
        for key, keywords in required_keywords.items():
            found = False
            for col in df.columns:
                if any(k in col for k in keywords):
                    cols_map[key] = col
                    found = True
                    break
            if not found and key == '당류':
                df['당류(g)'] = 0
                cols_map['당류'] = '당류(g)'
        
        final_cols = list(cols_map.values())
        df = df[final_cols]
        
        target_cols = [
            cols_map['에너지'], cols_map['탄수화물'], cols_map['단백질'], 
            cols_map['지방'], cols_map['당류'], cols_map['나트륨']
        ]
        
        for col in target_cols:
            df[col] = df[col].astype(str).replace({'-': '0', 'Tr': '0.01'})
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
        return df, cols_map
        
    except FileNotFoundError:
        st.error("⚠️ 'data.xlsx' 파일을 찾을 수 없습니다. 파일명을 확인해주세요.")
        return pd.DataFrame(), {}
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame(), {}

# 데이터 로딩 실행
df, cols_map = load_data()


# 3. UI 구성
st.title("CaloRhythm 🥗")
st.subheader("An Intelligent Nutrition Calculator for Korea")

# 사이드바
st.sidebar.title("Menu")
menu = st.sidebar.radio(
    "Go to:",
    ["Home", "1. Nutrition Calculator", "2. Quantity Optimizer", "3. Food Discovery"]
)

# --- 홈 화면 ---
if menu == "Home":
    st.write("### Welcome to CaloRhythm!")
    st.info("👈 왼쪽 사이드바에서 기능을 선택하세요.")
    
    if not df.empty:
        st.success(f"✅ 데이터 로드 성공! (총 {len(df)}개 식품)")
        with st.expander("📊 데이터셋 미리보기 (상위 5개)"):
            st.dataframe(df.head())
    else:
        st.error("⚠️ 데이터를 불러오지 못했습니다.")

# --- 메뉴 1: 영양분 계산기 ---
elif menu == "1. Nutrition Calculator":
    st.header("🍽️ 영양분 계산기 (절대량 기준)")
    st.markdown("""
    음식을 선택하고 양을 입력하면, **한국인 1일 영양성분 기준치(절대량 g)**와 
    비교하여 부족하거나 과한 정도를 알려드립니다.
    """)
    
    if df.empty:
        st.warning("데이터가 없어서 계산기를 실행할 수 없습니다.")
    else:
        # 1. 멀티 셀렉트 (검색)
        selected_foods = st.multiselect(
            "🥗 섭취한 음식을 검색해서 선택하세요:",
            options=df[cols_map['식품명']].unique(),
            placeholder="예: 쌀밥, 김치찌개, 계란후라이..."
        )

        if selected_foods:
            st.divider()
            st.subheader("📝 섭취량 입력 (g)")
            
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
            
            # 3. 계산 버튼
            if st.button("영양분 분석 시작 🧮", type="primary"):
                total_cal = 0
                total_carb = 0
                total_prot = 0
                total_fat = 0
                
                # 합산 로직
                for food, amount in food_amounts.items():
                    row = df[df[cols_map['식품명']] == food].iloc[0]
                    ratio = amount / 100.0
                    
                    total_cal += row[cols_map['에너지']] * ratio
                    total_carb += row[cols_map['탄수화물']] * ratio
                    total_prot += row[cols_map['단백질']] * ratio
                    total_fat += row[cols_map['지방']] * ratio

                st.divider()
                st.subheader("📊 영양 성분 분석 결과")
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("총 에너지", f"{total_cal:.0f} kcal")
                c2.metric("탄수화물 (g)", f"{total_carb:.1f} g")
                c3.metric("단백질 (g)", f"{total_prot:.1f} g")
                c4.metric("지방 (g)", f"{total_fat:.1f} g")
                
                # 기준치 설정
                std_carb = 324.0
                std_prot = 55.0
                std_fat = 54.0
                
                st.write("### ⚖️ 1일 권장량 대비 섭취량 비교 (g)")
                
                # 데이터 준비
                chart_df = pd.DataFrame({
                    '내 섭취량 (g)': [total_carb, total_prot, total_fat],
                    '1일 기준치 (g)': [std_carb, std_prot, std_fat]
                }, index=['탄수화물', '단백질', '지방'])
                
                # 🟢 [수정] Altair 차트로 변경하여 가로 글씨 적용
                # 데이터 변환 (Wide -> Long)
                chart_df_melted = chart_df.reset_index().melt('index', var_name='구분', value_name='양(g)')
                
                # 차트 생성
                chart = alt.Chart(chart_df_melted).mark_bar().encode(
                    # labelAngle=0이 글자를 가로로 만드는 핵심 옵션입니다
                    x=alt.X('index', title=None, axis=alt.Axis(labelAngle=0)), 
                    y=alt.Y('양(g)'),
                    color='구분',
                    xOffset='구분' # 그룹화된 막대
                ).properties(height=350)
                
                st.altair_chart(chart, use_container_width=True)
                
                # 하단 명시 및 피드백
                st.info(f"""
                **ℹ️ 참고 기준 (성인 1일 영양성분 기준치)** - **탄수화물:** {std_carb}g 
                - **단백질:** {std_prot}g 
                - **지방:** {std_fat}g 
                *(출처: 식약처 고시 식품등의 표시기준)*
                """)

                if total_carb > std_carb:
                    st.warning(f"⚠️ 탄수화물이 기준치보다 **{total_carb - std_carb:.1f}g** 초과되었습니다.")
                else:
                    st.warning(f"⚠️ 탄수화물이 기준치까지 **{-total_carb + std_carb:.1f}g** 부족합니다.")
                if total_prot > std_prot:
                    st.warning(f"⚠️ 단백질이 기준치보다 **{-std_prot + total_prot:.1f}g** 초과되었습니다.")
                else:
                    st.warning(f"⚠️ 단백질이 기준치까지 **{std_prot - total_prot:.1f}g** 부족합니다.")
                if total_fat > std_fat:
                    st.warning(f"⚠️ 지방 섭취가 기준치보다 **{total_fat - std_fat:.1f}g** 초과되었습니다.")
                else:
                    st.warning(f"⚠️ 지방 섭취가 기준치까지 **{- total_fat + std_fat:.1f}g** 부족합니다.")

        else:
            st.info("👆 위 검색창에서 음식을 먼저 선택해주세요.")

                        
# --- 메뉴 2: 재료 양 최적화 ---
elif menu == "2. Quantity Optimizer":
    st.header("⚖️ AI 식단 최적화기 (Diet Optimizer)")
    st.markdown("""
    설정한 한도 내에서 **최소 섭취량**과 **우선순위**를 고려하여 
    가장 최적화된 재료 비율을 계산해 드립니다.
    """)
    
    try:
        from scipy.optimize import minimize
        import math
    except ImportError:
        st.error("scipy 라이브러리가 필요합니다.")
        st.stop()

    if df.empty:
        st.warning("데이터가 로드되지 않아 기능을 사용할 수 없습니다.")
    else:
        st.divider()

        # 1. 제한 조건 입력
        st.subheader("🎯 1끼 영양소 제한 설정")
        col1, col2, col3, col4 = st.columns(4)
        with col1: limit_cal = st.number_input("칼로리 (kcal)", value=500.0, step=50.0)
        with col2: limit_carb = st.number_input("탄수화물 (g)", value=60.0, step=10.0)
        with col3: limit_prot = st.number_input("단백질 (g)", value=30.0, step=5.0)
        with col4: limit_fat = st.number_input("지방 (g)", value=15.0, step=5.0)

        # 2. 재료 선택
        st.divider()
        selected_foods_opt = st.multiselect(
            "🥗 재료 선택:",
            options=df[cols_map['식품명']].unique(),
            placeholder="예: 닭가슴살, 고구마, 아몬드...",
            key="opt_multiselect"
        )

        if selected_foods_opt:
            # 2-1. 최소 섭취량 입력
            st.markdown("##### 🔽 재료별 최소 섭취량 (g)")
            min_amounts = {}
            min_cols = st.columns(3)
            for i, food in enumerate(selected_foods_opt):
                with min_cols[i % 3]:
                    min_val = st.number_input(f"{food} 최소", min_value=0.0, step=10.0, key=f"min_{food}")
                    min_amounts[food] = min_val
            
            st.divider()
            
            # 🟢 [추가 기능] 우선순위 설정
            st.subheader("⭐ 우선순위 설정")
            st.caption("어떤 요소를 최우선으로 꽉 채우시겠습니까?")
            
            priority_mode = st.radio(
                "우선순위 선택:",
                ["골고루 (기본)", "단백질 우선 🔥", "탄수화물 우선 🍚", "지방 우선 🥑", "칼로리 채우기 ⚡"],
                horizontal=True
            )
            
            # 우선순위에 따른 가중치 설정
            # 기본 가중치는 1, 선택된 요소는 100을 부여하여 강력하게 최적화 유도
            weights = {'cal': 1, 'carb': 1, 'prot': 1, 'fat': 1}
            
            if "단백질" in priority_mode: weights['prot'] = 100
            elif "탄수화물" in priority_mode: weights['carb'] = 100
            elif "지방" in priority_mode: weights['fat'] = 100
            elif "칼로리" in priority_mode: weights['cal'] = 100

            if st.button("최적 비율 계산하기 🧩", type="primary"):
                # 데이터 준비
                target_data = []
                user_min_bounds = []
                for food in selected_foods_opt:
                    row = df[df[cols_map['식품명']] == food].iloc[0]
                    target_data.append({
                        'name': food,
                        'cal': row[cols_map['에너지']] / 100.0,
                        'carb': row[cols_map['탄수화물']] / 100.0,
                        'prot': row[cols_map['단백질']] / 100.0,
                        'fat': row[cols_map['지방']] / 100.0
                    })
                    user_min_bounds.append(min_amounts[food])
                
                n_items = len(target_data)
                
                # 목적 함수 (가중치 적용)
                def objective(x):
                    total_cal = sum(x[i] * target_data[i]['cal'] for i in range(n_items))
                    total_carb = sum(x[i] * target_data[i]['carb'] for i in range(n_items))
                    total_prot = sum(x[i] * target_data[i]['prot'] for i in range(n_items))
                    total_fat = sum(x[i] * target_data[i]['fat'] for i in range(n_items))
                    
                    loss = 0
                    # 가중치를 곱해서 오차 계산 (우선순위 항목의 오차가 크면 페널티 폭증)
                    loss += weights['cal'] * ((limit_cal - total_cal) / (limit_cal + 1e-6)) ** 2
                    loss += weights['carb'] * ((limit_carb - total_carb) / (limit_carb + 1e-6)) ** 2
                    loss += weights['prot'] * ((limit_prot - total_prot) / (limit_prot + 1e-6)) ** 2
                    loss += weights['fat'] * ((limit_fat - total_fat) / (limit_fat + 1e-6)) ** 2
                    return loss

                # 제약 조건 (한도 초과 금지)
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
                        st.error("⚠️ 계산 오류: 조건이 상충됩니다.")
                    
                    elif result.success:
                        st.success(f"✅ 최적 조합 발견! ({priority_mode})")
                        
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
                        
                        # 안전한 비율 계산 함수
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
                            '영양소': ['칼로리', '탄수화물', '단백질', '지방'],
                            '충족률(%)': percentages
                        })
                        
                        # 우선순위 항목 강조 색상
                        bar_color = '#4CAF50' # 기본 초록
                        if "단백질" in priority_mode: 
                            chart_df.loc[chart_df['영양소']=='단백질', 'Color'] = '#FF4B4B' # 빨강 강조
                        elif "탄수화물" in priority_mode:
                            chart_df.loc[chart_df['영양소']=='탄수화물', 'Color'] = '#FF4B4B'
                        else:
                            chart_df['Color'] = '#4CAF50'

                        # Altair 차트
                        chart_opt = alt.Chart(chart_df).mark_bar().encode(
                            x=alt.X('영양소', title=None, axis=alt.Axis(labelAngle=0)),
                            y=alt.Y('충족률(%)', scale=alt.Scale(domain=[0, 100])),
                            color=alt.Color('영양소', legend=None) if 'Color' not in chart_df else alt.value('#4CAF50'),
                            tooltip=['영양소', alt.Tooltip('충족률(%)', format='.1f')]
                        ).properties(height=350)
                        
                        st.altair_chart(chart_opt, use_container_width=True)
                        
                        display_df = pd.DataFrame({
                            '현재 섭취량': [total_res['cal'], total_res['carb'], total_res['prot'], total_res['fat']],
                            '설정 한도': [limit_cal, limit_carb, limit_prot, limit_fat],
                            '충족률(%)': percentages
                        }, index=['칼로리', '탄수화물', '단백질', '지방'])
                        
                        st.table(display_df.style.format("{:.1f}"))
                        
                    else:
                        st.warning("⚠️ 최적 해를 찾지 못했습니다. (최소 섭취량이 한도를 넘었을 수 있습니다)")
                        
                except Exception as e:
                    st.error(f"오류: {e}")

        else:
            st.info("👆 재료를 먼저 선택해주세요.")

# --- 메뉴 3: 영양 성분 검색/추천 ---
elif menu == "3. Food Discovery":
    st.header("🔍 영양 성분별 랭킹 검색 (Food Discovery)")
    st.markdown("특정 영양소를 기준으로 **함유량이 가장 높은 음식**과 **가장 낮은 음식**을 찾아보세요. (100g 기준)")
    
    if df.empty:
        st.warning("데이터가 로드되지 않아 기능을 사용할 수 없습니다.")
    else:
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            nutrient_type = st.radio("⚖️ 기준이 될 영양소를 선택하세요:", ["탄수화물", "단백질", "지방"], horizontal=True)
        with col2:
            rank_count = st.slider("📊 보여줄 순위 개수 조절:", 3, 100, 10)

        target_col = cols_map[nutrient_type]
        display_cols = [cols_map['식품명'], target_col, cols_map['에너지']]

        df_high = df.nlargest(rank_count, target_col)[display_cols].reset_index(drop=True)
        df_high.index = df_high.index + 1
        df_low = df.nsmallest(rank_count, target_col)[display_cols].reset_index(drop=True)
        df_low.index = df_low.index + 1

        st.divider()
        col_high, col_low = st.columns(2)
        
        with col_high:
            st.subheader(f"⬆️ {nutrient_type} 많은 음식 Top {rank_count}")
            st.dataframe(df_high.style.background_gradient(subset=[target_col], cmap="Reds"), use_container_width=True)

        with col_low:
            st.subheader(f"⬇️ {nutrient_type} 적은 음식 Top {rank_count}")
            st.dataframe(df_low.style.background_gradient(subset=[target_col], cmap="Blues"), use_container_width=True)
            
        st.info(f"💡 **Tip**: {nutrient_type} 섭취 조절 시 참고하세요.")