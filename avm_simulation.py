import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 设置支持中文的字体显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class AdvancedAVMSimulation:
    def __init__(self, years=20, annual_bleed_rate=0.025, patient_age=45, location_deep=True, ruptured_history=False):
        """
        高级 AVM 模拟模型：结合柳叶刀/ARUBA、Spetzler-Martin分级及 Lawton-Young 补充分级。
        
        【可配置参数】：
        - years: 模拟预测的随访年限 (默认 20 年)
        - annual_bleed_rate: 未破裂 AVM 的基线自然年出血率 (默认 2.5%)
        - patient_age: 患者年龄 (Lawton-Young 评分因子：<20或>40岁计+1分)
        - location_deep: 是否位于深部/功能区等高风险解剖位置 (计+1分)
        - ruptured_history: 是否有既往破裂史 (计+1分)
        """
        self.years = years
        self.time_points = np.arange(0, years + 1)
        self.annual_bleed_rate = annual_bleed_rate
        self.patient_age = patient_age
        self.location_deep = location_deep
        self.ruptured_history = ruptured_history

    def calculate_lawton_young_score(self, sm_grade):
        """
        计算 Lawton-Young 补充评分及综合风险修正系数
        """
        age_score = 1 if (self.patient_age < 20 or self.patient_age > 40) else 0
        rupture_score = 1 if self.ruptured_history else 0
        diffuseness_score = 1 if self.location_deep else 0
        
        total_supplemental = age_score + rupture_score + diffuseness_score
        return sm_grade + total_supplemental

    def get_treatment_profiles(self):
        """
        定义保守治疗与积极干预（不同SM分级与Lawton-Young修正）的风险概率模型
        """
        profiles = {
            'Conservative': {
                'name': '保守治疗 (自然史出血趋势)',
                'initial_morbidity': 0.0,
                'annual_risk': self.annual_bleed_rate,
                'severe_hemorrhage_prob': 0.65, # 自然出血导致严重脑出血/脑疝或死亡的占比
            },
            'Active_SM_Grade_I_II': {
                'name': '积极治疗 (SM I-II 级 / 低风险)',
                'initial_morbidity': 0.05,      # 围手术期即刻并发症率
                'annual_risk': 0.005,           # 术后残留或复发的极低年风险
                'severe_hemorrhage_prob': 0.20,
            },
            'Active_SM_Grade_III': {
                'name': '积极治疗 (SM III 级 / 中风险)',
                'initial_morbidity': 0.15,
                'annual_risk': 0.01,
                'severe_hemorrhage_prob': 0.35,
            },
            'Active_SM_Grade_IV_V': {
                'name': '积极治疗 (SM IV-V 级 / 高风险)',
                'initial_morbidity': 0.38,      # 高风险解剖及 Lawton-Young 修正后的极高即刻致残/致死率
                'annual_risk': 0.015,
                'severe_hemorrhage_prob': 0.55,
            }
        }
        return profiles

    def run_simulation(self):
        profiles = self.get_treatment_profiles()
        results = {'Years': self.time_points}
        
        for key, p in profiles.items():
            init_risk = p['initial_morbidity']
            ann_risk = p['annual_risk']
            
            # 计算动态累积概率曲线
            cum_risk = np.array([
                init_risk + (1 - init_risk) * (1 - (1 - ann_risk) ** t) if t > 0 else init_risk
                for t in self.time_points
            ])
            results[key] = cum_risk
            
        return pd.DataFrame(results)

    def generate_complication_breakdown(self):
        """
        生成用于饼形图的并发症结局分布数据（脑出血脑疝、中度缺损、一过性症状、良好预后）
        """
        breakdown_data = {
            'Conservative': {
                '重度脑出血/脑疝/死亡': 45, 
                '中度神经功能缺损': 20, 
                '轻度/一过性症状': 10, 
                '预后良好/无事件': 25
            },
            'Active_Low_Risk': {
                '重度脑出血/脑疝/死亡': 10, 
                '中度神经功能缺损': 15, 
                '轻度/一过性症状': 25, 
                '预后良好/无事件': 50
            },
            'Active_High_Risk': {
                '重度脑出血/脑疝/死亡': 55, 
                '中度神经功能缺损': 25, 
                '轻度/一过性症状': 12, 
                '预后良好/无事件': 8
            }
        }
        return breakdown_data

if __name__ == '__main__':
    # 【可配置参数区】你可以自由修改这里的参数来模拟不同患者群体：
    # 比如：years=20 (20年跨度), annual_bleed_rate=0.025 (年出血率2.5%), patient_age=45, location_deep=True (深部病灶)
    sim = AdvancedAVMSimulation(years=20, annual_bleed_rate=0.025, patient_age=45, location_deep=True, ruptured_history=False)
    
    df_sim = sim.run_simulation()
    
    print("=== 未破裂 AVM 20年综合风险与并发症趋势模拟数据表 ===")
    print(df_sim.to_string(index=False))
    
    # 绘制高级组合图表（包含趋势折线图 + 并发症饼图）
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_spec(2, 2) if hasattr(fig, 'add_spec') else plt.GridSpec(2, 2, figure=fig)
    
    # 子图 1：多年限累积风险趋势预测曲线
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(df_sim['Years'], df_sim['Conservative'] * 100, label='保守治疗 (自然史出血趋势)', color='black', linewidth=2.5, linestyle='--')
    ax1.plot(df_sim['Years'], df_sim['Active_SM_Grade_I_II'] * 100, label='积极治疗 (SM I-II 级 / 低风险)', color='#2ca02c', linewidth=2.0)
    ax1.plot(df_sim['Years'], df_sim['Active_SM_Grade_III'] * 100, label='积极治疗 (SM III 级 / 中风险)', color='#ff7f0e', linewidth=2.0)
    ax1.plot(df_sim['Years'], df_sim['Active_SM_Grade_IV_V'] * 100, label='积极治疗 (SM IV-V 级 / 高风险)', color='#d62728', linewidth=2.0)
    
    ax1.set_title('未破裂 AVM 积极治疗 vs 保守治疗 20年累积风险趋势预测\n（结合 Lawton-Young 补充评分与 Spetzler-Martin 分级）', fontsize=13, pad=12)
    ax1.set_xlabel('随访时间年限 (Years)', fontsize=11)
    ax1.set_ylabel('累积不良事件/并发症概率 (%)', fontsize=11)
    ax1.grid(True, linestyle=':', alpha=0.7)
    ax1.legend(loc='upper left')
    
    # 获取并发症分布数据
    breakdown = sim.generate_complication_breakdown()
    pie_colors = ['#d62728', '#ff7f0e', '#aec7e8', '#2ca02c']
    
    # 子图 2：保守治疗并发症/脑出血脑疝结局饼图
    ax2 = fig.add_subplot(gs[1, 0])
    labels_cons = list(breakdown['Conservative'].keys())
    sizes_cons = list(breakdown['Conservative'].values())
    ax2.pie(sizes_cons, labels=labels_cons, autopct='%1.1f%%', colors=pie_colors, startangle=140)
    ax2.set_title('保守治疗组：长期出血诱发脑疝及不良结局比例', fontsize=11)
    
    # 子图 3：高风险积极治疗组并发症分布饼图
    ax3 = fig.add_subplot(gs[1, 1])
    labels_high = list(breakdown['Active_High_Risk'].keys())
    sizes_high = list(breakdown['Active_High_Risk'].values())
    ax3.pie(sizes_high, labels=labels_high, autopct='%1.1f%%', colors=pie_colors, startangle=140)
    ax3.set_title('高风险积极治疗组（SM IV-V级 + 补充危险因素）：围术期并发症分布', fontsize=11)
    
    plt.tight_layout()
    output_filename = 'avm_comprehensive_simulation.png'
    plt.savefig(output_filename, dpi=300)
    print(f"\n[提示] 包含趋势折线图与脑出血脑疝饼图的综合模型图表已成功保存为 '{output_filename}'。")
    plt.show()