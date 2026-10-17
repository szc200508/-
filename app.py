import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 解决中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 网页标题
st.title("☕ 校园咖啡馆投资决策与敏感性模拟器")
st.markdown("欢迎来到课堂互动环节！请在下方调整参数，观察 **NPV（净现值）** 的实时变化：")

# ==========================================
# 1. 侧边栏：让同学在手机/电脑上自由拖动滑块调整参数
# ==========================================
st.sidebar.header("🎛️ 调整项目参数")

inv = st.sidebar.slider("初始投资额 (万元)", 50.0, 200.0, 100.0, 5.0)
vol = st.sidebar.slider("销售量 (万杯/年)", 10.0, 50.0, 25.0, 1.0)
pri = st.sidebar.slider("产品单价 (元/杯)", 5.0, 20.0, 10.0, 0.5)
var_c = st.sidebar.slider("单位变动成本 (元/杯)", 1.0, 10.0, 5.0, 0.5)
fix_c = st.sidebar.slider("每年固定成本/房租 (万元)", 1.0, 20.0, 4.0, 1.0)
rate = st.sidebar.slider("折现率 (%)", 1.0, 25.0, 10.0, 0.5) / 100.0

# ==========================================
# 2. 核心计算
# ==========================================
ocf = (vol * pri - vol * var_c) - fix_c
npv = -inv + ocf / (1 + rate)

# 主页面展示大指标
col1, col2 = st.columns(2)
col1.metric("计算出的营业现金流 (OCF)", f"{ocf:.2f} 万元")
if npv > 0:
    col2.metric("净现值 (NPV)", f"{npv:.2f} 万元", delta="盈利（可投资）", delta_color="normal")
else:
    col2.metric("净现值 (NPV)", f"{npv:.2f} 万元", delta="亏损（请拒绝）", delta_color="inverse")

st.markdown("---")

# ==========================================
# 3. 动态绘制图表
# ==========================================
st.subheader("📊 实时敏感性分析驾驶舱")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 左图：单变量模拟
test_labels = ['单价降9%', '固定成本涨150%', '销量降20%']
test_npvs = [
    -inv + ((vol * (pri*0.91) - vol * var_c) - fix_c) / (1 + rate),
    -inv + ((vol * pri - vol * var_c) - fix_c*2.5) / (1 + rate),
    -inv + (((vol*0.8) * pri - (vol*0.8) * var_c) - fix_c) / (1 + rate)
]
colors = ['red' if x < 0 else 'green' for x in test_npvs]
axes[0].barh(test_labels, test_npvs, color=colors, alpha=0.8)
axes[0].axvline(0, color='black', linestyle='--', linewidth=1)
axes[0].set_title('单变量冲击后的 NPV')
axes[0].grid(axis='x', linestyle=':', alpha=0.5)

# 右图：热力图
prices = np.round(np.linspace(pri * 0.8, pri * 1.2, 5), 1)
volumes = np.round(np.linspace(vol * 0.6, vol * 1.4, 5), 1)
matrix_data = np.zeros((len(volumes), len(prices)))
for i, v_val in enumerate(volumes):
    for j, p_val in enumerate(prices):
        c_val = (v_val * p_val - v_val * var_c) - fix_c
        matrix_data[i, j] = -inv + c_val / (1 + rate)

sns.heatmap(matrix_data, annot=True, fmt=".1f", cmap="RdYlGn",
            xticklabels=prices, yticklabels=volumes, ax=axes[1], cbar=False)
axes[1].set_title('单价 vs 销量 热力图矩阵')
axes[1].set_xlabel('单价 (元)')
axes[1].set_ylabel('销量 (万杯)')

plt.tight_layout()
st.pyplot(fig)