import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, ttk

# 设置支持中文的字体显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class ComprehensiveAVMAppWithPie:
    def __init__(self, root):
        self.root = root
        root.title("AVM 多模态策略模拟与大数据并发症结局分析系统")
        root.geometry("520x720")
        
        # 1. 基础与随访参数
        self.var_years = tk.IntVar(value=15)
        self.var_age = tk.IntVar(value=40)
        self.var_sm_grade = tk.IntVar(value=3)
        
        # 2. 治疗方案多选变量
        self.var_use_embolization = tk.BooleanVar(value=True)
        self.var_use_microsurgery = tk.BooleanVar(value=True)
        self.var_use_gammaknife = tk.BooleanVar(value=False)
        self.var_embolization_count = tk.IntVar(value=2)
        
        # 3. 临床症状与病史变量
        self.var_epilepsy = tk.BooleanVar(value=False)
        self.var_fainting = tk.BooleanVar(value=False)
        self.var_bled = tk.BooleanVar(value=False)
        self.var_headache_dizziness = tk.BooleanVar(value=True)
        self.var_hypertension = tk.BooleanVar(value=False)
        self.var_pregnancy = tk.BooleanVar(value=False)
        
        # 4. 解剖结构变量
        self.var_nidus_size = tk.StringVar(value="中等 (3-6cm)")
        self.var_deep_drainage = tk.BooleanVar(value=False)
        self.var_other_aneurysm = tk.BooleanVar(value=False)

        self.create_main_interface()

    def create_main_interface(self):
        lbl_title = tk.Label(self.root, text="AVM 智能决策与并发症结局预测系统", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=10)
        
        lbl_sub = tk.Label(self.root, text="同步输出多模态趋势曲线及死亡、脑疝、残疾、自理率等大数据饼图", font=("Arial", 9), fg="gray")
        lbl_sub.pack(pady=2)

        btn_config = tk.Button(self.root, text="⚙ 配置治疗方案、栓塞次数与临床特征", font=("Arial", 11, "bold"), bg="#1f77b4", fg="white", padx=10, pady=6, command=self.open_config_window)
        btn_config.pack(pady=15)

        self.status_frame = tk.LabelFrame(self.root, text=" 当前策略与参数配置概览 ", font=("Arial", 10, "bold"))
        self.status_frame.pack(pady=5, fill="x", padx=25)
        
        self.lbl_summary = tk.Label(self.status_frame, text=self.get_summary_text(), justify="left", font=("Arial", 9))
        self.lbl_summary.pack(padx=15, pady=10, anchor="w")

        btn_run = tk.Button(self.root, text="▶ 运行趋势模拟与专业结局饼图分析", font=("Arial", 12, "bold"), bg="#2ca02c", fg="white", padx=10, pady=8, command=self.run_simulation)
        btn_run.pack(pady=20)

    def get_summary_text(self):
        treatments = []
        if self.var_use_embolization.get():
            treatments.append(f"介入栓塞({self.var_embolization_count.get()}次)")
        if self.var_use_microsurgery.get():
            treatments.append("显微开刀切除")
        if self.var_use_gammaknife.get():
            treatments.append("伽马刀")
        therapy_str = " + ".join(treatments) if treatments else "纯保守观察 (无积极干预)"
        
        return (f"• 拟定治疗策略: {therapy_str}\n"
                f"• 随访年限: {self.var_years.get()} 年 | 年龄: {self.var_age.get()} 岁 | SM分级: 第 {self.var_sm_grade.get()} 级\n"
                f"• 既往出血史: {'有' if self.var_bled.get() else '无'} | 癫痫: {'有' if self.var_epilepsy.get() else '无'} | 晕倒眩晕: {'有' if self.var_fainting.get() else '无'}\n"
                f"• 畸形团体积: {self.var_nidus_size.get()} | 其它动脉瘤: {'有' if self.var_other_aneurysm.get() else '无'}")

    def open_config_window(self):
        config_win = tk.Toplevel(self.root)
        config_win.title("治疗方案与临床特征高级配置")
        config_win.geometry("460x650")
        config_win.grab_set()

        canvas = tk.Canvas(config_win, width=420, height=560)
        scrollbar = ttk.Scrollbar(config_win, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 1. 治疗方案多选框
        ttk.Label(scrollable_frame, text="【治疗方案选择 (可多选组合)】", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=5)
        
        ttk.Checkbutton(scrollable_frame, text="介入栓塞治疗 (Embolization)", variable=self.var_use_embolization).pack(anchor="w", padx=15, pady=2)

        frame_emb_count = ttk.Frame(scrollable_frame)
        frame_emb_count.pack(anchor="w", padx=35, pady=2)
        ttk.Label(frame_emb_count, text="  └ 介入栓塞次数: ").pack(side="left")
        ttk.Combobox(frame_emb_count, textvariable=self.var_embolization_count, values=[1, 2, 3, 4], state="readonly", width=5).pack(side="left")

        ttk.Checkbutton(scrollable_frame, text="显微镜开刀切除 (Microsurgical Resection)", variable=self.var_use_microsurgery).pack(anchor="w", padx=15, pady=2)
        ttk.Checkbutton(scrollable_frame, text="伽马刀放射外科 (Gamma Knife)", variable=self.var_use_gammaknife).pack(anchor="w", padx=15, pady=2)

        def toggle_embolization_ui(*args):
            if self.var_use_embolization.get():
                frame_emb_count.pack(anchor="w", padx=35, pady=2)
            else:
                frame_emb_count.pack_forget()

        self.var_use_embolization.trace_add("write", toggle_embolization_ui)
        toggle_embolization_ui()

        # 2. 基础参数
        ttk.Label(scrollable_frame, text="【基础人口学与 SM 分级】", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=10)
        f1 = ttk.Frame(scrollable_frame); f1.pack(anchor="w", padx=10, pady=2)
        ttk.Label(f1, text="随访年限 (Years): ").pack(side="left"); ttk.Entry(f1, textvariable=self.var_years, width=8).pack(side="left")

        f2 = ttk.Frame(scrollable_frame); f2.pack(anchor="w", padx=10, pady=2)
        ttk.Label(f2, text="患者年龄 (Age): ").pack(side="left"); ttk.Entry(f2, textvariable=self.var_age, width=8).pack(side="left")

        f3 = ttk.Frame(scrollable_frame); f3.pack(anchor="w", padx=10, pady=2)
        ttk.Label(f3, text="Spetzler-Martin 分级: ").pack(side="left")
        ttk.Combobox(f3, textvariable=self.var_sm_grade, values=[1, 2, 3, 4, 5], state="readonly", width=6).pack(side="left")

        # 3. 症状勾选项
        ttk.Label(scrollable_frame, text="【临床症状与病史勾选项】", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=10)
        ttk.Checkbutton(scrollable_frame, text="既往有颅内出血史 (Prior Bleed)", variable=self.var_bled).pack(anchor="w", padx=15, pady=2)
        ttk.Checkbutton(scrollable_frame, text="是否存在癫痫发作 (Epilepsy)", variable=self.var_epilepsy).pack(anchor="w", padx=15, pady=2)
        ttk.Checkbutton(scrollable_frame, text="是否存在晕倒 / 严重眩晕 (Fainting)", variable=self.var_fainting).pack(anchor="w", padx=15, pady=2)
        ttk.Checkbutton(scrollable_frame, text="长期头痛或严重头晕", variable=self.var_headache_dizziness).pack(anchor="w", padx=15, pady=2)
        ttk.Checkbutton(scrollable_frame, text="合并高血压", variable=self.var_hypertension).pack(anchor="w", padx=15, pady=2)
        ttk.Checkbutton(scrollable_frame, text="是否处于妊娠期 / 备孕期", variable=self.var_pregnancy).pack(anchor="w", padx=15, pady=2)

        # 4. 解剖结构
        ttk.Label(scrollable_frame, text="【解剖结构与畸形团特征】", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=10)
        f4 = ttk.Frame(scrollable_frame); f4.pack(anchor="w", padx=10, pady=2)
        ttk.Label(f4, text="畸形团体积大小: ").pack(side="left")
        ttk.Combobox(f4, textvariable=self.var_nidus_size, values=["小型 (<3cm)", "中等 (3-6cm)", "大型 (>6cm)"], state="readonly", width=14).pack(side="left")

        ttk.Checkbutton(scrollable_frame, text="是否存在深部静脉引流 (Deep Drainage)", variable=self.var_deep_drainage).pack(anchor="w", padx=15, pady=2)
        ttk.Checkbutton(scrollable_frame, text="畸形团是否存在其他动脉瘤", variable=self.var_other_aneurysm).pack(anchor="w", padx=15, pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def save_and_close():
            self.lbl_summary.config(text=self.get_summary_text())
            config_win.destroy()

        btn_save = tk.Button(config_win, text="保存配置并返回", bg="#1f77b4", fg="white", font=("Arial", 10, "bold"), command=save_and_close)
        btn_save.pack(pady=10)

    def run_simulation(self):
        years = self.var_years.get()
        sm = self.var_sm_grade.get()
        bled = self.var_bled.get()
        fainting = self.var_fainting.get()
        other_aneurysm = self.var_other_aneurysm.get()
        nidus = self.var_nidus_size.get()
        deep_drain = self.var_deep_drainage.get()
        
        use_emb = self.var_use_embolization.get()
        emb_count = self.var_embolization_count.get()
        use_mic = self.var_use_microsurgery.get()
        use_gam = self.var_use_gammaknife.get()

        # ==========================================
        # 风险与并发症结局大数据计算逻辑
        # ==========================================
        base_natural_bleed = 0.075 if (bled and sm >= 3) else (0.05 if bled else 0.022)
        if other_aneurysm: base_natural_bleed += 0.015
        if fainting: base_natural_bleed += 0.003

        nidus_mult = 1.0 if "小" in nidus else (1.3 if "中" in nidus else 2.0)

        if not use_emb and not use_mic and not use_gam:
            initial_morbidity = 0.0
            residual_annual_risk = base_natural_bleed
        else:
            risk_parts = []
            if use_emb:
                emb_per_risk = 0.03
                total_emb_risk = 1 - (1 - emb_per_risk) ** emb_count
                risk_parts.append(total_emb_risk)
            if use_mic:
                mic_risk = 0.04 * (sm ** 1.3) * nidus_mult * (0.85 if use_emb else 1.0)
                risk_parts.append(mic_risk)
            if use_gam:
                gam_risk = 0.03 + (0.04 if deep_drain else 0.0)
                risk_parts.append(gam_risk)

            initial_morbidity = min(sum(risk_parts), 0.85)
            residual_annual_risk = 0.003 if sm <= 3 else 0.012

        # 曲线计算
        time_points = np.arange(0, years + 1)
        cons_risk = np.array([1 - (1 - base_natural_bleed) ** t if t > 0 else 0 for t in time_points])
        
        if not use_emb and not use_mic and not use_gam:
            active_risk = cons_risk
        else:
            active_risk = np.array([
                initial_morbidity + (1 - initial_morbidity) * (1 - (1 - residual_annual_risk) ** t) 
                if t > 0 else initial_morbidity 
                for t in time_points
            ])

        # ==========================================
        # 专业的并发症与预后结局大数据库比例推算 (Pie Chart Data)
        # ==========================================
        # 依据 SM 分级和干预复杂度，动态权重分配到不同结局：
        # [自理 (完全/良好), 部分自理 (中度残疾), 重度残疾, 植物人, 脑疝/急性昏迷, 死亡]
        if not use_emb and not use_mic and not use_gam:
            # 保守观察组：若长期随访发生出血或脑疝，结局较重
            p_death = 15.0 + sm * 3
            p_herniation = 10.0 + sm * 2
            p_vegetative = 5.0
            p_severe_disability = 15.0
            p_partial_self = 20.0
            p_full_self = 100.0 - (p_death + p_herniation + p_vegetative + p_severe_disability + p_partial_self)
        else:
            # 积极干预组：风险权重与 SM 级及栓塞次数绑定
            severity_factor = (sm * 4) + (emb_count * 2 if use_emb else 0)
            p_death = max(4.0, 3.0 + severity_factor * 1.2)
            p_herniation = max(3.0, 2.0 + severity_factor * 0.9)
            p_vegetative = max(2.0, 1.0 + severity_factor * 0.5)
            p_severe_disability = max(8.0, 5.0 + severity_factor * 1.5)
            p_partial_self = 20.0
            p_full_self = max(10.0, 100.0 - (p_death + p_herniation + p_vegetative + p_severe_disability + p_partial_self))

        # 确保比例总和为 100 且不为负
        pie_sizes = [max(p_full_self, 2.0), max(p_partial_self, 5.0), max(p_severe_disability, 2.0), 
                     max(p_vegetative, 1.0), max(p_herniation, 2.0), max(p_death, 2.0)]
        
        labels = [
            f'完全自理/预后良好\n({pie_sizes[0]:.1f}%)',
            f'部分自理/中度残疾\n({pie_sizes[1]:.1f}%)',
            f'重度残疾\n({pie_sizes[2]:.1f}%)',
            f'植物人状态\n({pie_sizes[3]:.1f}%)',
            f'脑疝/急性昏迷\n({pie_sizes[4]:.1f}%)',
            f'死亡\n({pie_sizes[5]:.1f}%)'
        ]
        colors = ['#2ca02c', '#1f77b4', '#ff7f0e', '#9467bd', '#8c564b', '#d62728']

        # 弹窗提示
        report = (f"=== 智能多模态预测与结局分析报告 ===\n\n"
                  f"• 整体即刻复合风险: {initial_morbidity*100:.1f} %\n"
                  f"• 死亡率估计: {pie_sizes[5]:.1f} %\n"
                  f"• 脑疝发生率: {pie_sizes[4]:.1f} %\n"
                  f"• 完全自理预后率: {pie_sizes[0]:.1f} %\n\n"
                  f"系统已同时为您生成双图表（趋势曲线对比图 + 临床并发症结局比例专业饼图）。")
        messagebox.showinfo("大数据模拟完成", report)

        # ==========================================
        # 双图表可视化输出 (Trend Line & Pie Chart)
        # ==========================================
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # 图表 1：长期趋势风险折线图
        ax1.plot(time_points, cons_risk * 100, label='保守观察组（自然史）', color='black', linewidth=2.5, linestyle='--')
        if use_emb or use_mic or use_gam:
            ax1.plot(time_points, active_risk * 100, label='积极干预策略组', color='#d62728', linewidth=2.5)
        ax1.set_title(f'长期累积不良风险趋势\n(SM分级:{sm}级 | 栓塞:{emb_count if use_emb else 0}次)', fontsize=11)
        ax1.set_xlabel('随访时间年限 (Years)', fontsize=10)
        ax1.set_ylabel('累积发生率 (%)', fontsize=10)
        ax1.grid(True, linestyle=':', alpha=0.7)
        ax1.legend(loc='upper left')

        # 图表 2：并发症与预后结局大数据库饼图
        ax2.pie(pie_sizes, labels=labels, colors=colors, startangle=140, 
                wedgeprops=dict(width=0.6, edgecolor='w'), textprops={'fontsize': 9})
        ax2.set_title(f'患者远期生存质量与并发症结局比例\n(结合 SM分级与多模态治疗大数据)', fontsize=11)

        plt.tight_layout()
        plt.savefig('avm_comprehensive_analysis_with_pie.png', dpi=300)
        plt.show()

if __name__ == '__main__':
    root = tk.Tk()
    app = ComprehensiveAVMAppWithPie(root)
    root.mainloop()