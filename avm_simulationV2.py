import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("AVM 智能决策与重症 ICU 大数据评估系统")

# 1. 用 Streamlit 侧边栏替代原本的 tkinter 配置弹窗
st.sidebar.header("⚙ 长期治疗方案与临床特征配置")
var_years = st.sidebar.slider("随访年限 (Years)", 1, 30, 15)
var_age = st.sidebar.slider("患者年龄 (Age)", 10, 90, 40)
var_sm_grade = st.sidebar.selectbox("Spetzler-Martin 分级", [1, 2, 3, 4, 5], index=2)

var_use_embolization = st.sidebar.checkbox("介入栓塞治疗", value=True)
var_use_microsurgery = st.sidebar.checkbox("显微镜开刀切除", value=True)
var_use_gammaknife = st.sidebar.checkbox("伽马刀放射外科", value=False)

# 2. 运行模拟按钮
if st.button("▶ 运行长期趋势模拟与分析"):
    # 计算逻辑
    time_points = np.arange(0, var_years + 1)
    cons_risk = np.array([1 - (1 - 0.05) ** t if t > 0 else 0 for t in time_points])
    
    # 3. 直接在网页中展示 Matplotlib 图表，而不是用 plt.show()
    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.plot(time_points, cons_risk * 100, label='保守观察组', color='black', linewidth=2.5, linestyle='--')
    ax1.set_title('长期累积不良风险趋势')
    ax1.set_xlabel('随访时间年限 (Years)')
    ax1.set_ylabel('累积发生率 (%)')
    ax1.grid(True, linestyle=':', alpha=0.7)
    ax1.legend(loc='upper left')

    st.pyplot(fig)