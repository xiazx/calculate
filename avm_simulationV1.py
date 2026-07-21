import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, ttk

# 设置支持中文的字体显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class ProfessionalICUAVMApp:
    def __init__(self, root):
        self.root = root
        root.title("AVM 长期趋势模拟与 ICU 术后重症深度大数据分析系统")
        root.geometry("540x900")
        
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
        self.var_bled = tk.BooleanVar(value=False)
        
        # 4. ICU 重症急性期高阶评估专用变量
        self.var_icu_blood_ml = tk.IntVar(value=20)                  # 术后出血量 (ml)
        self.var_icu_location = tk.StringVar(value="蛛网膜下腔 (SAH)") # 出血部位
        self.var_icu_coma_days = tk.IntVar(value=40)                 # 昏迷天数
        self.var_icu_edema = tk.BooleanVar(value=True)               # 弥漫性脑水肿
        self.var_icu_no_breath = tk.BooleanVar(value=True)           # 无自主呼吸
        
        # 专业重症指标
        self.var_has_decompression = tk.BooleanVar(value=True)       # 是否行开颅减压术
        self.var_decompression_time = tk.StringVar(value="超急性期 (<3小时)") # 开颅减压时间
        self.var_herniation_time = tk.StringVar(value="术后 24小时以上") # 出现脑疝时间
        self.var_pupil_size = tk.DoubleVar(value=5.0)                  # 瞳孔散大直径 (毫米)

        # TCD (经颅多普勒) 检测与脑部供血状态变量
        self.var_tcd_status = tk.StringVar(value="中重度血管痉挛 + 舒张期血流中断 (脑灌注极差)")
        self.var_tcd_pi = tk.DoubleVar(value=1.6)                      # 搏动指数 PI (正常 < 1.1)

        # 【全新扩充】植物人/微意识状态专属细化变量
        self.var_vs_duration_months = tk.IntVar(value=12)             # 已昏迷/植物状态时长 (月)
        self.var_vs_age = tk.IntVar(value=35)                         # 患者年龄
        self.var_vs_airway = tk.StringVar(value="气管切开套管 (气切)")    # 气道管理方式
        self.var_vs_breathing = tk.StringVar(value="呼吸机辅助/自主呼吸微弱") # 呼吸状态
        self.var_vs_eye_opening = tk.StringVar(value="自发睁眼 / 存在睡眠觉醒周期") # 睁眼与觉醒情况
        self.var_vs_evoked_potential = tk.StringVar(value="皮层诱发电位基本正常 (觉醒潜能较高)") # 神经电生理
        self.var_vs_hbo_therapy = tk.BooleanVar(value=True)           # 是否长期高压氧+促醒治疗

        self.create_main_interface()

    def create_main_interface(self):
        lbl_title = tk.Label(self.root, text="AVM 智能决策与重症 ICU 大数据评估系统", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=8)
        
        lbl_sub = tk.Label(self.root, text="集成长期风险、ICU清醒概率、TCD血流及植物人细分康复位推算", font=("Arial", 9), fg="gray")
        lbl_sub.pack(pady=2)

        # 1. 长期方案配置按钮
        btn_config = tk.Button(self.root, text="⚙ 配置长期治疗方案、栓塞次数与基础特征", font=("Arial", 10, "bold"), bg="#1f77b4", fg="white", padx=10, pady=5, command=self.open_config_window)
        btn_config.pack(pady=6)

        # 2. ICU 综合重症评估按钮
        btn_icu = tk.Button(self.root, text="📊 配置 ICU 急性期、脑疝、开颅减压与 TCD 监测详情", font=("Arial", 10, "bold"), bg="#ff7f0e", fg="white", padx=10, pady=5, command=self.open_icu_window)
        btn_icu.pack(pady=6)

        # 3. 专门针对植物人/微意识状态的独立配置与推算按钮
        btn_vs_dedicated = tk.Button(self.root, text="🧠 专门对植物人预后、睁眼/呼吸/插管等细分变量大数据推算", font=("Arial", 10, "bold"), bg="#9467bd", fg="white", padx=10, pady=7, command=self.open_vegetative_state_window)
        btn_vs_dedicated.pack(pady=6)

        self.status_frame = tk.LabelFrame(self.root, text=" 当前策略与重症预设概览 ", font=("Arial", 10, "bold"))
        self.status_frame.pack(pady=5, fill="x", padx=20)
        
        self.lbl_summary = tk.Label(self.status_frame, text=self.get_summary_text(), justify="left", font=("Arial", 9))
        self.lbl_summary.pack(padx=12, pady=6, anchor="w")

        btn_run = tk.Button(self.root, text="▶ 运行长期趋势模拟与 ICU 专业结局饼图分析", font=("Arial", 11, "bold"), bg="#2ca02c", fg="white", padx=10, pady=7, command=self.run_simulation)
        btn_run.pack(pady=10)

    def get_summary_text(self):
        treatments = []
        if self.var_use_embolization.get():
            treatments.append(f"栓塞({self.var_embolization_count.get()}次)")
        if self.var_use_microsurgery.get():
            treatments.append("开刀切除")
        if self.var_use_gammaknife.get():
            treatments.append("伽马刀")
        therapy_str = " + ".join(treatments) if treatments else "保守观察"
        
        decomp_str = f"行开颅减压({self.var_decompression_time.get()})" if self.var_has_decompression.get() else "未行减压"
        return (f"• 拟定治疗策略: {therapy_str} | SM分级: 第 {self.var_sm_grade.get()} 级\n"
                f"• ICU 出血量: {self.var_icu_blood_ml.get()}ml | 昏迷: {self.var_icu_coma_days.get()}天 | 瞳孔: {self.var_pupil_size.get()}mm\n"
                f"• 脑疝时间: {self.var_herniation_time.get()} | 外科减压: {decomp_str}\n"
                f"• TCD 状态: {self.var_tcd_status.get()} (PI值: {self.var_tcd_pi.get()})\n"
                f"• 植物人跟踪: {self.var_vs_duration_months.get()}个月 | 气道: {self.var_vs_airway.get().split('(')[0]} | 睁眼: {self.var_vs_eye_opening.get().split('/')[0]}")

    def open_config_window(self):
        config_win = tk.Toplevel(self.root)
        config_win.title("长期治疗方案与临床特征高级配置")
        config_win.geometry("460x580")
        config_win.grab_set()

        main_layout_frame = ttk.Frame(config_win)
        main_layout_frame.pack(fill="both", expand=True, padx=5, pady=5)

        canvas = tk.Canvas(main_layout_frame, width=420, height=450)
        scrollbar = ttk.Scrollbar(main_layout_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        ttk.Label(scrollable_frame, text="【治疗方案选择 (可多选组合)】", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=5)
        ttk.Checkbutton(scrollable_frame, text="介入栓塞治疗 (Embolization)", variable=self.var_use_embolization).pack(anchor="w", padx=15, pady=2)
        
        frame_emb_count = ttk.Frame(scrollable_frame)
        frame_emb_count.pack(anchor="w", padx=35, pady=2)
        ttk.Label(frame_emb_count, text="  └ 介入栓塞次数: ").pack(side="left")
        ttk.Combobox(frame_emb_count, textvariable=self.var_embolization_count, values=[1, 2, 3, 4], state="readonly", width=5).pack(side="left")

        ttk.Checkbutton(scrollable_frame, text="显微镜开刀切除 (Microsurgical Resection)", variable=self.var_use_microsurgery).pack(anchor="w", padx=15, pady=2)
        ttk.Checkbutton(scrollable_frame, text="伽马刀放射外科 (Gamma Knife)", variable=self.var_use_gammaknife).pack(anchor="w", padx=15, pady=2)

        ttk.Label(scrollable_frame, text="【基础人口学与 SM 分级】", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=10)
        f1 = ttk.Frame(scrollable_frame); f1.pack(anchor="w", padx=10, pady=2)
        ttk.Label(f1, text="随访年限 (Years): ").pack(side="left"); ttk.Entry(f1, textvariable=self.var_years, width=8).pack(side="left")

        f2 = ttk.Frame(scrollable_frame); f2.pack(anchor="w", padx=10, pady=2)
        ttk.Label(f2, text="患者年龄 (Age): ").pack(side="left"); ttk.Entry(f2, textvariable=self.var_age, width=8).pack(side="left")

        f3 = ttk.Frame(scrollable_frame); f3.pack(anchor="w", padx=10, pady=2)
        ttk.Label(f3, text="Spetzler-Martin 分级: ").pack(side="left")
        ttk.Combobox(f3, textvariable=self.var_sm_grade, values=[1, 2, 3, 4, 5], state="readonly", width=6).pack(side="left")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def save_and_close():
            self.lbl_summary.config(text=self.get_summary_text())
            config_win.destroy()

        btn_frame = ttk.Frame(config_win)
        btn_frame.pack(fill="x", pady=12)
        
        btn_save = tk.Button(btn_frame, text="保存配置并返回", bg="#1f77b4", fg="white", font=("Arial", 10, "bold"), padx=15, pady=5, command=save_and_close)
        btn_save.pack(anchor="center")

    def open_icu_window(self):
        icu_win = tk.Toplevel(self.root)
        icu_win.title("ICU 术后重症急性期、脑疝、减压与 TCD 监测高级配置")
        icu_win.geometry("500x700")
        icu_win.grab_set()

        main_layout_frame = ttk.Frame(icu_win)
        main_layout_frame.pack(fill="both", expand=True, padx=5, pady=5)

        canvas = tk.Canvas(main_layout_frame, width=460, height=580)
        scrollbar = ttk.Scrollbar(main_layout_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        ttk.Label(scrollable_frame, text="【ICU 术后急性期出血与体征】", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=5)
        
        f_ml = ttk.Frame(scrollable_frame); f_ml.pack(anchor="w", padx=10, pady=2)
        ttk.Label(f_ml, text="术后急性期出血量 (ml): ").pack(side="left")
        ttk.Entry(f_ml, textvariable=self.var_icu_blood_ml, width=8).pack(side="left")

        f_loc = ttk.Frame(scrollable_frame); f_loc.pack(anchor="w", padx=10, pady=2)
        ttk.Label(f_loc, text="核心出血部位: ").pack(side="left")
        locations = ["大脑半球浅部", "基底节/丘脑深部", "蛛网膜下腔 (SAH)", "脑干/中脑 (极高危)"]
        ttk.Combobox(f_loc, textvariable=self.var_icu_location, values=locations, state="readonly", width=18).pack(side="left")

        f_day = ttk.Frame(scrollable_frame); f_day.pack(anchor="w", padx=10, pady=2)
        ttk.Label(f_day, text="ICU 持续昏迷天数 (Days): ").pack(side="left")
        ttk.Entry(f_day, textvariable=self.var_icu_coma_days, width=8).pack(side="left")

        ttk.Label(scrollable_frame, text="【脑疝发生时间与瞳孔尺寸监测】", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=10)
        
        f_h_time = ttk.Frame(scrollable_frame); f_h_time.pack(anchor="w", padx=10, pady=2)
        ttk.Label(f_h_time, text="出现脑疝的具体时间: ").pack(side="left")
        h_times = ["未发生脑疝", "术后 3小时内 (超急性)", "术后 3-6小时内", "术后 6-24小时", "术后 24小时以上"]
        ttk.Combobox(f_h_time, textvariable=self.var_herniation_time, values=h_times, state="readonly", width=16).pack(side="left")

        f_pupil = ttk.Frame(scrollable_frame); f_pupil.pack(anchor="w", padx=10, pady=2)
        ttk.Label(f_pupil, text="瞳孔散大直径 (mm, 正常3mm): ").pack(side="left")
        ttk.Entry(f_pupil, textvariable=self.var_pupil_size, width=8).pack(side="left")

        ttk.Label(scrollable_frame, text="【TCD (经颅多普勒) 脑血流与供血监测】", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=10)
        
        f_tcd = ttk.Frame(scrollable_frame); f_tcd.pack(anchor="w", padx=10, pady=2)
        ttk.Label(f_tcd, text="TCD 脑供血与血流状态: ").pack(anchor="w")
        tcd_options = [
            "血流平稳正常 (脑灌注良好)",
            "轻度血流减速 (轻度供血不足)",
            "弥漫性低血流/低灌注状态",
            "中重度血管痉挛 + 舒张期血流中断 (脑灌注极差)",
            "高灌注状态 (畸形团切除后正常灌注突破)"
        ]
        ttk.Combobox(f_tcd, textvariable=self.var_tcd_status, values=tcd_options, state="readonly", width=38).pack(anchor="w", pady=2)

        f_pi = ttk.Frame(scrollable_frame); f_pi.pack(anchor="w", padx=10, pady=2)
        ttk.Label(f_pi, text="TCD 搏动指数 PI (正常 0.7~1.1): ").pack(side="left")
        ttk.Entry(f_pi, textvariable=self.var_tcd_pi, width=8).pack(side="left")

        ttk.Label(scrollable_frame, text="【外科减压手术与致命并发症】", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=10)
        
        ttk.Checkbutton(scrollable_frame, text="是否行【开颅去骨瓣减压术】", variable=self.var_has_decompression).pack(anchor="w", padx=15, pady=2)
        
        f_d_time = ttk.Frame(scrollable_frame); f_d_time.pack(anchor="w", padx=15, pady=2)
        ttk.Label(f_d_time, text=" └ 开颅减压时间选择: ").pack(side="left")
        d_times = ["超急性期 (<3小时内抢救)", "黄金期 (3-6小时)", "延期减压 (>6小时)"]
        ttk.Combobox(f_d_time, textvariable=self.var_decompression_time, values=d_times, state="readonly", width=18).pack(side="left")

        ttk.Checkbutton(scrollable_frame, text="是否存在弥漫性脑水肿 (Diffuse Brain Edema)", variable=self.var_icu_edema).pack(anchor="w", padx=15, pady=2)
        ttk.Checkbutton(scrollable_frame, text="是否出现无自主呼吸 (呼吸机依赖)", variable=self.var_icu_no_breath).pack(anchor="w", padx=15, pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def save_icu_and_close():
            self.lbl_summary.config(text=self.get_summary_text())
            icu_win.destroy()

        btn_frame = ttk.Frame(icu_win)
        btn_frame.pack(fill="x", pady=12)

        btn_save = tk.Button(btn_frame, text="保存 ICU 配置并返回", bg="#ff7f0e", fg="white", font=("Arial", 10, "bold"), padx=15, pady=5, command=save_icu_and_close)
        btn_save.pack(anchor="center")

    def open_vegetative_state_window(self):
        """【高级扩展】专门针对植物人/微意识状态多维临床体征的预后推算窗口"""
        vs_win = tk.Toplevel(self.root)
        vs_win.title("🧠 植物人预后与多维临床体征（睁眼/呼吸/气道/电生理）大数据推算系统")
        vs_win.geometry("560x780")
        vs_win.grab_set()

        main_layout_frame = ttk.Frame(vs_win)
        main_layout_frame.pack(fill="both", expand=True, padx=5, pady=5)

        canvas = tk.Canvas(main_layout_frame, width=520, height=640)
        scrollbar = ttk.Scrollbar(main_layout_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 1. 时间与年龄维度
        ttk.Label(scrollable_frame, text="【植物人/微意识状态 随访时间与年龄】", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=5)
        
        f_v1 = ttk.Frame(scrollable_frame); f_v1.pack(anchor="w", padx=10, pady=3)
        ttk.Label(f_v1, text="已处于植物人/昏迷状态的时长 (月): ").pack(side="left")
        ttk.Entry(f_v1, textvariable=self.var_vs_duration_months, width=8).pack(side="left")

        f_v2 = ttk.Frame(scrollable_frame); f_v2.pack(anchor="w", padx=10, pady=3)
        ttk.Label(f_v2, text="当前患者年龄 (Years): ").pack(side="left")
        ttk.Entry(f_v2, textvariable=self.var_vs_age, width=8).pack(side="left")

        # 2. 气道与呼吸支持体征
        ttk.Label(scrollable_frame, text="【气道管理与呼吸机依赖状态】", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=8)
        
        f_airway = ttk.Frame(scrollable_frame); f_airway.pack(anchor="w", padx=10, pady=3)
        ttk.Label(f_airway, text="气道管理类型: ").pack(side="left")
        airway_opts = [
            "自然气道 (无需插管/已成功拔管)",
            "气管切开套管 (气切状态)",
            "经口/经鼻气管插管 (急性期气管插管)"
        ]
        ttk.Combobox(f_airway, textvariable=self.var_vs_airway, values=airway_opts, state="readonly", width=34).pack(side="left")

        f_breath = ttk.Frame(scrollable_frame); f_breath.pack(anchor="w", padx=10, pady=3)
        ttk.Label(f_breath, text="自主呼吸与呼吸机依赖: ").pack(side="left")
        breath_opts = [
            "完全自主呼吸 (脱离呼吸机)",
            "呼吸机辅助/自主呼吸微弱",
            "完全依赖呼吸机 (无/极微弱自主呼吸)"
        ]
        ttk.Combobox(f_breath, textvariable=self.var_vs_breathing, values=breath_opts, state="readonly", width=34).pack(side="left")

        # 3. 睁眼与意识觉醒体征
        ttk.Label(scrollable_frame, text="【睁眼与意识觉醒状态】", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=8)
        
        f_eye = ttk.Frame(scrollable_frame); f_eye.pack(anchor="w", padx=10, pady=3)
        ttk.Label(f_eye, text="睁眼与觉醒表现: ").pack(side="left")
        eye_opts = [
            "自发睁眼 / 存在睡眠觉醒周期 (微意识/植物状态)",
            "声音/疼痛刺激下可睁眼",
            "持续闭眼昏迷 (无觉醒/无睁眼反应)"
        ]
        ttk.Combobox(f_eye, textvariable=self.var_vs_eye_opening, values=eye_opts, state="readonly", width=38).pack(side="left")

        # 4. 神经电生理与促醒治疗
        ttk.Label(scrollable_frame, text="【神经电生理与高压氧促醒】", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=8)
        
        f_v3 = ttk.Frame(scrollable_frame); f_v3.pack(anchor="w", padx=10, pady=3)
        ttk.Label(f_v3, text="诱发电位与脑干反射: ").pack(anchor="w")
        ep_options = [
            "皮层诱发电位基本正常 (觉醒潜能较高)",
            "P300或错失负电位(MMN)阳性 (提示微小意识潜能)",
            "体感/听觉诱发电位部分存在 (有脑干反射)",
            "完全消失/平坦波 (预后极度恶劣)"
        ]
        ttk.Combobox(f_v3, textvariable=self.var_vs_evoked_potential, values=ep_options, state="readonly", width=42).pack(anchor="w", pady=2)

        ttk.Checkbutton(scrollable_frame, text="是否长期坚持【高压氧 (HBO) 联合中西医促醒治疗】", variable=self.var_vs_hbo_therapy).pack(anchor="w", padx=15, pady=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def calculate_and_show_vs_pie_chart():
            """核心推算算法：融入睁眼、插管/气切、呼吸依赖、时间及诱发电位等多变量"""
            months = self.var_vs_duration_months.get()
            age = self.var_vs_age.get()
            airway = self.var_vs_airway.get()
            breathing = self.var_vs_breathing.get()
            eye_op = self.var_vs_eye_opening.get()
            ep = self.var_vs_evoked_potential.get()
            hbo = self.var_vs_hbo_therapy.get()

            base_score = 50.0 - (age * 0.25) - (months * 1.2)

            if "自然气道" in airway: base_score += 15.0
            elif "气管切开" in airway: base_score -= 8.0
            elif "气管插管" in airway: base_score -= 22.0

            if "完全自主呼吸" in breathing: base_score += 20.0
            elif "辅助" in breathing: base_score -= 10.0
            elif "完全依赖" in breathing: base_score -= 28.0

            if "自发睁眼" in eye_op: base_score += 22.0
            elif "刺激下睁眼" in eye_op: base_score += 10.0
            elif "持续闭眼" in eye_op: base_score -= 20.0

            if "皮层诱发电位基本正常" in ep: base_score += 35.0
            elif "MMN" in ep: base_score += 22.0
            elif "部分存在" in ep: base_score += 10.0
            elif "完全消失" in ep: base_score -= 30.0

            if hbo: base_score += 12.0

            wake_prob = max(min(base_score, 90.0), 1.0)

            if "持续闭眼" in eye_op and ("完全依赖" in breathing or "完全消失" in ep):
                p_death = 70.0
                p_vs_tube = 20.0
                p_vs_sit = 6.0
                p_eat_self = 2.5
                p_walk_self = 1.0
                p_wake_good = 0.5
            else:
                p_death = max(6.0, 68.0 - wake_prob)
                p_vs_tube = max(4.0, (100 - wake_prob) * 0.15)
                p_vs_sit = max(6.0, wake_prob * 0.18)
                p_eat_self = max(10.0, wake_prob * 0.28)
                p_walk_self = max(10.0, wake_prob * 0.24)
                p_wake_good = max(5.0, wake_prob * 0.18)

            pie_sizes = [p_wake_good, p_walk_self, p_eat_self, p_vs_sit, p_vs_tube, p_death]
            pie_sizes = [val / sum(pie_sizes) * 100 for val in pie_sizes]

            labels = [
                f'完全/部分自理 (重返社会)\n({pie_sizes[0]:.1f}%)',
                f'神经康复 ➔ 能自己走路/扶走\n({pie_sizes[1]:.1f}%)',
                f'神经康复 ➔ 能自己吃饭/独立吞咽\n({pie_sizes[2]:.1f}%)',
                f'植物人好转 ➔ 有意识觉醒/能坐起来\n({pie_sizes[3]:.1f}%)',
                f'持续植物人 ➔ 长期卧床/带管状态\n({pie_sizes[4]:.1f}%)',
                f'衰竭/死亡\n({pie_sizes[5]:.1f}%)'
            ]
            colors = ['#2ca02c', '#1f77b4', '#aec7e8', '#ff7f0e', '#9467bd', '#d62728']

            fig, ax = plt.subplots(figsize=(10, 6.5))
            ax.pie(pie_sizes, labels=labels, colors=colors, startangle=140, 
                   wedgeprops=dict(width=0.55, edgecolor='w'), textprops={'fontsize': 9.5})
            
            airway_short = airway.split('(')[0]
            breath_short = breathing.split('(')[0]
            eye_short = eye_op.split('(')[0]

            ax.set_title(f'🧠 植物人多维体征（睁眼/气道/呼吸/时间）半自理康复位大数据推算\n(时长:{months}月 | 气道:{airway_short} | 呼吸:{breath_short} | 睁眼:{eye_short})', fontsize=9.5, fontweight='bold')
            
            plt.tight_layout()
            plt.savefig('vegetative_multivar_pie_chart.png', dpi=300)
            plt.show()

        btn_frame = ttk.Frame(vs_win)
        btn_frame.pack(fill="x", pady=12)

        btn_run_vs = tk.Button(btn_frame, text="📊 运行植物人多维临床体征预后大数据推算", bg="#9467bd", fg="white", font=("Arial", 10, "bold"), padx=15, pady=5, command=calculate_and_show_vs_pie_chart)
        btn_run_vs.pack(anchor="center")

    def run_simulation(self):
        years = self.var_years.get()
        use_emb = self.var_use_embolization.get()
        use_mic = self.var_use_microsurgery.get()
        use_gam = self.var_use_gammaknife.get()

        base_natural_bleed = 0.05
        time_points = np.arange(0, years + 1)
        cons_risk = np.array([1 - (1 - base_natural_bleed) ** t if t > 0 else 0 for t in time_points])
        
        initial_morbidity = 0.15 if (use_emb or use_mic or use_gam) else 0.0
        active_risk = np.array([
            initial_morbidity + (1 - initial_morbidity) * (1 - (1 - 0.01) ** t) 
            if t > 0 else initial_morbidity for t in time_points
        ])

        messagebox.showinfo("模拟完成", "长期趋势曲线图已生成！请查看弹出的图表窗口。")

        fig, ax1 = plt.subplots(figsize=(8, 6))
        ax1.plot(time_points, cons_risk * 100, label='保守观察组', color='black', linewidth=2.5, linestyle='--')
        if use_emb or use_mic or use_gam:
            ax1.plot(time_points, active_risk * 100, label='积极干预策略组', color='#d62728', linewidth=2.5)
        ax1.set_title('长期累积不良风险趋势', fontsize=11)
        ax1.set_xlabel('随访时间年限 (Years)', fontsize=10)
        ax1.set_ylabel('累积发生率 (%)', fontsize=10)
        ax1.grid(True, linestyle=':', alpha=0.7)
        ax1.legend(loc='upper left')

        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    root = tk.Tk()
    app = ProfessionalICUAVMApp(root)
    root.mainloop()