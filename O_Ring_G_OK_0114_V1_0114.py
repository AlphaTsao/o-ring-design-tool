import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import matplotlib.font_manager as fm
import base64
from io import BytesIO
from PIL import Image, ImageFile

# ReportLab imports
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from streamlit_paste_button import paste_image_button

# --- 0. PDF 生成引擎設定 (ReportLab) ---
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Sercomm logo Base64
SERCOMM_LOGO_BASE64 = """
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CCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCExhQZACCEx5f8BIqD/uHbR2s8AAAAASUVORK5CYII=
""".strip()

def ascii_only(s: str) -> str:
    """只保留 ASCII 字元"""
    return "".join(ch for ch in str(s) if ord(ch) < 128)

def build_oring_pdf_report(
    project_name,
    engineer_name,
    title,
    input_data,       # list of dicts
    result_data,      # list of dicts
    verdict_data,     # dict
    diagram_img_bytes, 
    hist_comp_bytes,   
    hist_fill_bytes,   
    sercomm_logo_bytes,
) -> BytesIO:
    """
    建立 O-Ring PDF 報告（Landscape A4）
    """
    buffer = BytesIO()
    page_size = landscape(A4)
    c = canvas.Canvas(buffer, pagesize=page_size)
    width, height = page_size

    # --- 浮水印 Helper ---
    logo_reader = None
    if sercomm_logo_bytes:
        try:
            img_logo = Image.open(BytesIO(sercomm_logo_bytes)).convert("RGBA")
            img_rgb = img_logo.convert("RGB")
            img_hsv = img_rgb.convert("HSV")
            h, s, v = img_hsv.split()
            h_arr = np.array(h, dtype=np.uint8)
            s_arr = np.array(s, dtype=np.uint8)
            v_arr = np.array(v, dtype=np.uint8)
            mask = ((s_arr > 60) & (v_arr > 50) & (h_arr >= 120) & (h_arr <= 210))
            alpha_arr = np.where(mask, 100, 0).astype("uint8")
            alpha = Image.fromarray(alpha_arr, mode="L")
            white = Image.new("RGB", img_rgb.size, (255, 255, 255))
            light_rgb = Image.blend(white, img_rgb, 0.18)
            img_final = Image.merge("RGBA", (*light_rgb.split(), alpha))
            buf_logo = BytesIO()
            img_final.save(buf_logo, format="PNG")
            buf_logo.seek(0)
            logo_reader = ImageReader(buf_logo)
        except Exception:
            logo_reader = None

    def draw_watermark():
        if not logo_reader: return
        c.saveState()
        img_w, img_h = logo_reader.getSize()
        target_w = width * 0.55
        scale = target_w / float(img_w)
        draw_w = img_w * scale
        draw_h = img_h * scale
        c.translate(width / 2.0, height / 2.0)
        c.rotate(45)
        # 繪製浮水印 (因為是最後繪製，所以會在最上層)
        c.drawImage(logo_reader, -draw_w/2.0, -draw_h/2.0, width=draw_w, height=draw_h, mask="auto")
        c.restoreState()

    # =================== Page 1: Header + Input + Schematic ===================
    y = height - 15 * mm

    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(20 * mm, y, "O-Ring Design Analysis Report (V1.0)")
    y -= 12 * mm

    c.setFont("Helvetica", 10)
    c.drawString(20 * mm, y, f"Project : {ascii_only(project_name)}")
    y -= 5 * mm
    c.drawString(20 * mm, y, f"Engineer: {engineer_name}")
    y -= 5 * mm
    c.drawString(20 * mm, y, f"Title   : {ascii_only(title)}")
    y -= 10 * mm

    # 1. Input Parameters
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20 * mm, y, "1. Input Parameters (Dimension & Tolerance)")
    y -= 10 * mm

    c.setFont("Helvetica-Bold", 9)
    c.drawString(20 * mm, y, "Item Name")
    c.drawString(80 * mm, y, "Nominal (mm)")
    c.drawString(110 * mm, y, "Tol (+/-)")
    c.drawString(140 * mm, y, "Cpk")
    y -= 6 * mm
    c.setFont("Helvetica", 9)

    for item in input_data:
        name = item["name"]
        nom = item.get("nom", 0.0)
        tol = item.get("tol", 0.0)
        cpk = item.get("cpk", 0.0)
        c.drawString(20 * mm, y, ascii_only(name))
        c.drawString(80 * mm, y, f"{nom:.3f}")
        c.drawString(110 * mm, y, f"{tol:.3f}")
        c.drawString(140 * mm, y, f"{cpk:.2f}")
        y -= 6 * mm
    
    y -= 10 * mm

    # Cad Schematic
    if diagram_img_bytes:
        try:
            img = ImageReader(BytesIO(diagram_img_bytes))
            img_w, img_h = img.getSize()
            remaining_h = y - 15 * mm
            max_w = width - 40 * mm
            target_h = min(remaining_h, 90 * mm)
            scale = min(max_w / img_w, target_h / img_h)
            draw_w = img_w * scale
            draw_h = img_h * scale

            c.setFont("Helvetica-Bold", 12)
            c.drawString(20 * mm, y, "Cad Schematic")
            y -= 6 * mm
            c.drawImage(img, 20*mm, y - draw_h, width=draw_w, height=draw_h, mask="auto")
        except:
            pass

    # Page 1 結束前繪製浮水印 (確保在最上層)
    draw_watermark()
    c.showPage()

    # =================== Page 2: Results -> Charts -> Verdict ===================
    y = height - 15 * mm

    # 2. Simulation Results (Table)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20 * mm, y, "2. Simulation Results (Monte Carlo)")
    y -= 10 * mm

    c.setFont("Helvetica-Bold", 9)
    c.drawString(20 * mm, y, "Metric")
    c.drawString(70 * mm, y, "Mean (%)")
    c.drawString(100 * mm, y, "Yield (%)")
    c.drawString(130 * mm, y, "Defect (PPM)")
    c.drawString(160 * mm, y, "Target (%)")
    y -= 6 * mm
    c.setFont("Helvetica", 9)

    for res in result_data:
        c.drawString(20 * mm, y, ascii_only(res["item"]))
        
        mean_val = res['mean']
        if isinstance(mean_val, (int, float)):
             c.drawString(70 * mm, y, f"{mean_val:.3f}")
        else:
             c.drawString(70 * mm, y, str(mean_val))
             
        c.drawString(100 * mm, y, f"{res['yield']:.2f}")
        c.drawString(130 * mm, y, f"{int(res['ppm'])}")
        c.drawString(160 * mm, y, ascii_only(res['target']))
        y -= 6 * mm
    
    y -= 8 * mm # 減少間距

    # --- Charts (Histograms) ---
    chart_height = 42 * mm 
    
    # Chart 1: Compression
    if hist_comp_bytes:
        try:
            img = ImageReader(BytesIO(hist_comp_bytes))
            img_w, img_h = img.getSize()
            scale = chart_height / img_h
            draw_w = img_w * scale
            draw_h = chart_height
            
            c.setFont("Helvetica-Bold", 10)
            c.drawString(20 * mm, y, "Compression Rate Distribution")
            y -= 5 * mm
            c.drawImage(img, 20*mm, y - draw_h, width=draw_w, height=draw_h, mask="auto")
            y -= (draw_h + 8 * mm) # 減少間距
        except:
            pass

    # Chart 2: Fill Rate
    if hist_fill_bytes:
        try:
            img = ImageReader(BytesIO(hist_fill_bytes))
            img_w, img_h = img.getSize()
            scale = chart_height / img_h
            draw_w = img_w * scale
            draw_h = chart_height
            
            c.setFont("Helvetica-Bold", 10)
            c.drawString(20 * mm, y, "Fill Rate Distribution")
            y -= 5 * mm
            c.drawImage(img, 20*mm, y - draw_h, width=draw_w, height=draw_h, mask="auto")
            y -= (draw_h + 8 * mm) # 減少間距
        except:
            pass

    # --- 3. Final Verdict (嘗試擠在 Page 2) ---
    if y < 35 * mm:
        # Page 2 結束前繪製浮水印 (確保在最上層)
        draw_watermark()
        c.showPage()
        y = height - 15 * mm

    c.setFont("Helvetica-Bold", 14)
    c.drawString(20 * mm, y, "3. Final Verdict (Combined)")
    y -= 8 * mm
    
    # 畫框與文字
    c.setFillColorRGB(0.95, 0.95, 0.95) # 淺灰底
    c.rect(20*mm, y - 15*mm, width - 40*mm, 15*mm, fill=1, stroke=0)
    c.setFillColorRGB(0, 0, 0) # 黑字
    
    v_yield = verdict_data.get("yield", 0.0)
    v_ppm = verdict_data.get("ppm", 0.0)
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(25 * mm, y - 10*mm, f"Combined Yield:  {v_yield:.2f} %")
    c.setFillColorRGB(0.8, 0, 0) # 紅字 PPM
    c.drawString(100 * mm, y - 10*mm, f"Defect Rate:  {int(v_ppm)} PPM")
    c.setFillColorRGB(0, 0, 0)

    # 最後一頁結束前繪製浮水印
    draw_watermark()

    c.save()
    buffer.seek(0)
    return buffer

# --- 以下為 Streamlit 主程式 ---

st.set_page_config(page_title="O-Ring Design Tool (V1.0)", layout="wide")

# CSS Style
st.markdown("""
<style>
    .metric-label { font-size: 16px; font-weight: bold; color: #555; }
    .metric-value-large { font-size: 28px; font-weight: bold; }
    .good-text { color: #4CAF50; }
    .bad-text { color: #F44336; }
    .info-text { font-size: 14px; color: #1565C0; font-weight: bold;}
    .summary-box {
        background-color: #e3f2fd;
        padding: 20px;
        border-radius: 10px;
        border-left: 8px solid #2196F3;
        margin-top: 20px;
        text-align: center;
    }
    div[data-testid="stNumberInput"] label { font-size: 14px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🔧 O-Ring Design Tool (V1.0)")
st.caption("產能驅動模擬 (Monte Carlo) | 介面文字優化 | ReportLab PDF 匯出")

def get_chinese_font():
    font_names = [f.name for f in fm.fontManager.ttflist]
    preferred_fonts = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'PingFang SC', 'Heiti TC']
    for font in preferred_fonts:
        if font in font_names:
            return font
    return None
chinese_font = get_chinese_font()

def generate_dim(nominal, tol, cpk, size):
    if cpk == 0 or tol == 0:
        return np.full(size, nominal)
    sigma = tol / (3 * cpk)
    return np.random.normal(nominal, sigma, size)

def draw_cad_schematic_v11(groove_type, w_top, w_btm, depth, oring_w, oring_h, mode, font_name):
    fig, ax = plt.subplots(figsize=(3, 1.8), dpi=250)
    ax.set_aspect('equal')
    ax.axis('off')
    
    title_size = 9
    label_size = 6
    title_font = fm.FontProperties(fname=fm.findfont(font_name), size=title_size) if font_name else None
    label_font = fm.FontProperties(fname=fm.findfont(font_name), size=label_size) if font_name else None
    lbl_top = "上底" if font_name else "Top"
    lbl_btm = "下底" if font_name else "Bottom"
    lbl_h = "高" if font_name else "Height"
    dim_lw = 0.5
    main_lw = 1.0

    if mode == "正壓 (Axial)":
        margin = max(w_top, w_btm) * 0.5
        verts = [
            (-w_top/2 - margin, depth), (-w_top/2, depth), 
            (-w_btm/2, 0), (w_btm/2, 0), 
            (w_top/2, depth), (w_top/2 + margin, depth),
            (w_top/2 + margin, -depth*0.2), (-w_top/2 - margin, -depth*0.2)
        ]
        poly = patches.Polygon(verts, facecolor='#e0e0e0', edgecolor='black', hatch='///', lw=dim_lw)
        ax.add_patch(poly)
        oring = patches.Ellipse((0, oring_h/2), width=oring_w, height=oring_h, 
                                facecolor='#ffab91', edgecolor='red', alpha=0.8, lw=main_lw)
        ax.add_patch(oring)
        ax.annotate("", xy=(w_top/2+margin*0.2, depth), xytext=(w_top/2+margin*0.2, 0), arrowprops=dict(arrowstyle='<->', lw=dim_lw))
        ax.text(w_top/2+margin*0.4, depth/2, lbl_h, va='center', fontproperties=label_font)
        ax.set_xlim(-w_top/2 - margin - 1, w_top/2 + margin + 1)
        ax.set_ylim(-depth*0.5, depth*1.5)
        ax.set_title("Axial", fontproperties=title_font)
    else:
        h_half = depth / 2
        x_left = 0
        x_right_top = w_top
        x_right_btm = w_btm
        ax.plot([x_left, x_left], [h_half, -h_half], color='#004d40', lw=main_lw)
        ax.plot([x_right_top, x_right_btm], [h_half, -h_half], color='#004d40', lw=main_lw)
        ax.plot([x_left, x_right_top], [h_half, h_half], color='#004d40', lw=main_lw)
        ax.plot([x_left, x_right_btm], [-h_half, -h_half], color='#004d40', lw=main_lw)
        oring_x_center = oring_w / 2
        oring = patches.Ellipse((oring_x_center, 0), width=oring_w, height=oring_h, 
                                facecolor='#90a4ae', edgecolor='#004d40', lw=main_lw, alpha=0.7)
        ax.add_patch(oring)
        ax.text(x_right_top/2, h_half + depth*0.1, lbl_top, ha='center', va='bottom', fontproperties=label_font)
        ax.text(x_right_btm/2, -h_half - depth*0.1, lbl_btm, ha='center', va='top', fontproperties=label_font)
        ax.annotate("", xy=(x_left - depth*0.1, h_half), xytext=(x_left - depth*0.1, -h_half), arrowprops=dict(arrowstyle='<->', lw=dim_lw, color='#004d40'))
        ax.text(x_left - depth*0.2, 0, lbl_h, ha='right', va='center', fontproperties=label_font, color='#004d40')
        max_w = max(w_top, w_btm, oring_w)
        margin_x = max_w * 0.5
        margin_y = depth * 0.5
        ax.set_xlim(x_left - margin_x*0.5, max_w + margin_x)
        ax.set_ylim(-h_half - margin_y, h_half + margin_y)
        ax.set_title("Radial", fontproperties=title_font)
    return fig

# --- 全域設定 ---
with st.expander("⚙️ 全域設定與目標 (Global Settings & Yield Targets)", expanded=True):
    row0_1, row0_2, row0_3 = st.columns([1, 1, 2])
    with row0_1:
        comp_mode = st.radio("壓縮模式", ["正壓 (Axial)", "側壓 (Radial)"])
    with row0_2:
        monthly_forecast = st.number_input("月產能預估 (Monthly Forecast)", value=500000, step=10000)
        sim_count = int(monthly_forecast)
    with row0_3:
        st.info(f"💡 系統將執行 **{sim_count:,}** 次蒙地卡羅模擬，以評估該批生產的良率。")
    st.markdown("---")
    st.write("🎯 **良率判定標準**")
    row1_1, row1_2, row1_3, row1_4 = st.columns(4)
    with row1_1:
        target_comp_min = st.number_input("壓縮 Min (%)", value=15.0, step=0.5)
    with row1_2:
        target_comp_max = st.number_input("壓縮 Max (%)", value=25.0, step=0.5)
    with row1_3:
        target_fill_min = st.number_input("填充 Min (%)", value=75.0, step=0.5)
    with row1_4:
        target_fill_max = st.number_input("填充 Max (%)", value=85.0, step=0.5)

# --- O-Ring 設定 ---
st.subheader("1. O-Ring 設定")
oring_type = st.radio("類型", ["正規圓形 (Standard)", "不規則形 (Irregular)"], horizontal=True, label_visibility="collapsed")
sim_oring_h_raw = None; sim_oring_w_raw = None; sim_oring_area_raw = None
oring_display_w_nom = 0; oring_display_h_nom = 0
oring_pdf_params = [] 

if oring_type == "正規圓形 (Standard)":
    c_o1, c_o2, c_o3 = st.columns([1, 1, 1])
    with c_o1:
        cs_nom = st.number_input("線徑 (CS) mm", value=2.00, format="%.3f")
    with c_o2:
        cs_tol = st.number_input("CS 公差 (±) mm", value=0.08, format="%.3f")
    with c_o3:
        cs_cpk = st.number_input("CS Cpk", value=1.33, step=0.1) 
    if cs_nom > 0:
        raw_cs_sim = generate_dim(cs_nom, cs_tol, cs_cpk, sim_count)
        sim_oring_h_raw = sim_oring_w_raw = raw_cs_sim
        sim_oring_area_raw = np.pi * (raw_cs_sim / 2)**2
        oring_display_w_nom = oring_display_h_nom = cs_nom
        oring_pdf_params.append({"name": "O-Ring CS", "nom": cs_nom, "tol": cs_tol, "cpk": cs_cpk})
else:
    c_ir1, c_ir2, c_ir3, c_ir4 = st.columns(4)
    with c_ir1:
        irr_area = st.number_input("截面積 (Area) mm²", value=3.14, format="%.3f")
    with c_ir2:
        irr_h = st.number_input("高度 (Height) mm", value=2.00, format="%.3f")
    with c_ir3:
        irr_h_tol = st.number_input("高度公差 (±)", value=0.08, format="%.3f")
        irr_area_tol = irr_h_tol ** 2 if irr_h_tol > 0 else 0
    with c_ir4:
        irr_h_cpk = st.number_input("高度 Cpk", value=1.33, step=0.1)
        irr_area_cpk = irr_h_cpk
    if irr_h > 0 and irr_area > 0:
        sim_oring_h_raw = generate_dim(irr_h, irr_h_tol, irr_h_cpk, sim_count)
        sim_oring_area_raw = generate_dim(irr_area, irr_area_tol, irr_area_cpk, sim_count)
        sim_oring_w_raw = sim_oring_area_raw / sim_oring_h_raw
        oring_display_h_nom = irr_h
        oring_display_w_nom = irr_area / irr_h
        oring_pdf_params.append({"name": "O-Ring Height", "nom": irr_h, "tol": irr_h_tol, "cpk": irr_h_cpk})
        oring_pdf_params.append({"name": "O-Ring Area", "nom": irr_area, "tol": irr_area_tol, "cpk": irr_area_cpk})
st.markdown("---")

# --- 拉伸設定 ---
st.subheader("2. 拉伸設定 (Stretch)")
is_stretched = st.checkbox("啟用拉伸計算", value=False)
stretch_factor = 1.0
if is_stretched:
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        stretch_pct = st.number_input("拉伸率 (%)", value=2.50, step=0.1)
    with col_s2:
        install_len = st.number_input("安裝後長度 (mm)", value=100.00, step=1.0)
    stretch_factor = 1 + (stretch_pct / 100.0)
    orig_len_calc = install_len / stretch_factor
    area_new_display = (np.pi * (oring_display_h_nom/2)**2) / stretch_factor if oring_type == "正規圓形 (Standard)" else (oring_display_w_nom * oring_display_h_nom) / stretch_factor
    with col_s3:
        st.markdown(f"<div class='info-text'>安裝前原始長度</div><div style='font-size:20px; font-weight:bold;'>{orig_len_calc:.2f} mm</div>", unsafe_allow_html=True)
    with col_s4:
        st.markdown(f"<div class='info-text'>拉伸後平均截面積</div><div style='font-size:20px; font-weight:bold;'>{area_new_display:.3f} mm²</div>", unsafe_allow_html=True)

if sim_oring_h_raw is not None:
    sim_oring_area_final = sim_oring_area_raw / stretch_factor
    shrink_ratio = np.sqrt(1 / stretch_factor)
    sim_oring_h_final = sim_oring_h_raw * shrink_ratio
    sim_oring_w_final = sim_oring_w_raw * shrink_ratio
    oring_display_h_final = oring_display_h_nom * shrink_ratio
    oring_display_w_final = oring_display_w_nom * shrink_ratio
else:
    sim_oring_h_final = sim_oring_w_final = sim_oring_area_final = None
    oring_display_h_final = oring_display_w_final = 0
st.markdown("---")

# --- 溝槽參數 ---
st.subheader("3. 溝槽參數 (Groove)")
groove_type = st.radio("形狀", ["矩形 (Rectangular)", "梯形 (Trapezoidal)"], horizontal=True, label_visibility="collapsed")
sim_groove_depth = None; sim_groove_area = None; sim_groove_width_eff = None
plot_w_top = 0; plot_w_btm = 0; plot_depth = 0
groove_pdf_params = []

if groove_type == "矩形 (Rectangular)":
    rg1, rg2 = st.columns(2)
    with rg1:
        g_depth_nom = st.number_input("溝槽高度 (Height) mm", value=1.55, format="%.3f")
        g_depth_tol = st.number_input("H 公差 (±) mm", value=0.05, format="%.3f")
        g_depth_cpk = st.number_input("H Cpk", value=1.33, step=0.1)
    with rg2:
        g_width_nom = st.number_input("溝槽寬度 (Width) mm", value=2.40, format="%.3f")
        g_width_tol = st.number_input("W 公差 (±) mm", value=0.05, format="%.3f")
        g_width_cpk = st.number_input("W Cpk", value=1.33, step=0.1)
    sim_groove_depth = generate_dim(g_depth_nom, g_depth_tol, g_depth_cpk, sim_count)
    sim_g_width = generate_dim(g_width_nom, g_width_tol, g_width_cpk, sim_count)
    sim_groove_area = sim_g_width * sim_groove_depth
    sim_groove_width_eff = sim_g_width
    plot_depth = g_depth_nom; plot_w_top = plot_w_btm = g_width_nom
    
    groove_pdf_params.append({"name": "Groove Height", "nom": g_depth_nom, "tol": g_depth_tol, "cpk": g_depth_cpk})
    groove_pdf_params.append({"name": "Groove Width", "nom": g_width_nom, "tol": g_width_tol, "cpk": g_width_cpk})
else:
    tg1, tg2, tg3 = st.columns(3)
    with tg1:
        st.markdown("**溝槽高度 (Height)**")
        g_depth_nom = st.number_input("高度 (H) mm", value=1.55, format="%.3f")
        g_depth_tol = st.number_input("H 公差 (±) mm", value=0.05, format="%.3f")
        g_depth_cpk = st.number_input("H Cpk", value=1.33, step=0.1)
    with tg2:
        st.markdown("**上底寬度 (Top Width)**")
        g_wtop_nom = st.number_input("上底寬 (W_top) mm", value=2.00, format="%.3f")
        g_wtop_tol = st.number_input("上底公差 (±) mm", value=0.05, format="%.3f")
        g_wtop_cpk = st.number_input("上底 Cpk", value=1.33, step=0.1)
    with tg3:
        st.markdown("**下底寬度 (Bottom Width)**")
        g_wbtm_nom = st.number_input("下底寬 (W_btm) mm", value=1.50, format="%.3f")
        g_wbtm_tol = st.number_input("下底公差 (±) mm", value=0.05, format="%.3f")
        g_wbtm_cpk = st.number_input("下底 Cpk", value=1.33, step=0.1)
    sim_groove_depth = generate_dim(g_depth_nom, g_depth_tol, g_depth_cpk, sim_count)
    sim_wtop = generate_dim(g_wtop_nom, g_wtop_tol, g_wtop_cpk, sim_count)
    sim_wbtm = generate_dim(g_wbtm_nom, g_wbtm_tol, g_wbtm_cpk, sim_count)
    sim_groove_area = (sim_wtop + sim_wbtm) * sim_groove_depth / 2
    sim_groove_width_eff = (sim_wtop + sim_wbtm) / 2
    plot_depth = g_depth_nom; plot_w_top = g_wtop_nom; plot_w_btm = g_wbtm_nom
    
    groove_pdf_params.append({"name": "Groove Height", "nom": g_depth_nom, "tol": g_depth_tol, "cpk": g_depth_cpk})
    groove_pdf_params.append({"name": "Groove Width (Top)", "nom": g_wtop_nom, "tol": g_wtop_tol, "cpk": g_wtop_cpk})
    groove_pdf_params.append({"name": "Groove Width (Btm)", "nom": g_wbtm_nom, "tol": g_wbtm_tol, "cpk": g_wbtm_cpk})

# --- 4. 示意圖 (Picture) ---
st.markdown("---")
st.subheader("4. 示意圖 (Picture)")

schematic_source = st.radio(
    "選擇示意圖來源", 
    ["程式自動繪製 (Auto Generated)", "自行貼上Screanshot (Screanshot Paste)"], 
    horizontal=True
)

final_diagram_bytes = None

if schematic_source == "程式自動繪製 (Auto Generated)":
    if plot_depth > 0:
        fig_cad = draw_cad_schematic_v11(groove_type, plot_w_top, plot_w_btm, plot_depth, 
                                        oring_display_w_final, oring_display_h_final, comp_mode, chinese_font)
        c_fig1, c_fig2, c_fig3 = st.columns([3, 2, 3]) 
        with c_fig2:
            st.pyplot(fig_cad, use_container_width=True)
            
        buf_cad = BytesIO()
        fig_cad.savefig(buf_cad, format="png", dpi=200, bbox_inches='tight', transparent=True)
        buf_cad.seek(0)
        final_diagram_bytes = buf_cad.getvalue()

else: # 自行貼上Screanshot
    st.info("👇 Screanshot後請點擊下方Paste按鈕")
    
    # [FIX] 這個 paste 元件在 Streamlit 多次 rerun 後，偶發「變成 Paste Button / 點了沒反應」
    # 你的手動 workaround（切到 Auto Generated 再切回來）其實是在「重新掛載 component」。
    # 這裡用「輸入參數簽章」變更時，自動刷新 key，效果等同於自動重新掛載，但不改外觀/流程。
    if "_paste_btn_nonce" not in st.session_state:
        st.session_state["_paste_btn_nonce"] = 0
        st.session_state["_paste_btn_sig"] = None

    _paste_sig = (
        schematic_source,
        comp_mode, sim_count,
        target_comp_min, target_comp_max,
        target_fill_min, target_fill_max,
        oring_type,
        locals().get("cs_nom"), locals().get("cs_tol"), locals().get("cs_cpk"),
        locals().get("irr_area"), locals().get("irr_area_tol"), locals().get("irr_area_cpk"),
        locals().get("irr_h"), locals().get("irr_h_tol"), locals().get("irr_h_cpk"),
        is_stretched, locals().get("stretch_pct"), locals().get("install_len"),
        groove_type,
        locals().get("g_depth_nom"), locals().get("g_depth_tol"), locals().get("g_depth_cpk"),
        locals().get("g_width_nom"), locals().get("g_width_tol"), locals().get("g_width_cpk"),
        locals().get("g_wtop_nom"), locals().get("g_wtop_tol"), locals().get("g_wtop_cpk"),
        locals().get("g_wbtm_nom"), locals().get("g_wbtm_tol"), locals().get("g_wbtm_cpk"),
    )
    if st.session_state["_paste_btn_sig"] != _paste_sig:
        st.session_state["_paste_btn_sig"] = _paste_sig
        st.session_state["_paste_btn_nonce"] += 1

    paste_result = paste_image_button(
        label="📋 Paste",
        background_color="#3B82F6",
        hover_background_color="#2563EB",
        errors="ignore",
        key=f"clipboard_paste_btn_{st.session_state['_paste_btn_nonce']}"
    )

    if paste_result.image_data is not None:
        st.image(paste_result.image_data, caption="已貼上的圖片", width=400)
        buf_paste = BytesIO()
        paste_result.image_data.save(buf_paste, format="PNG")
        buf_paste.seek(0)
        final_diagram_bytes = buf_paste.getvalue()
    else:
        st.warning("尚未貼上圖片")

# --- 計算與報告 ---
if sim_oring_h_final is not None and sim_groove_depth is not None and sim_groove_width_eff is not None:
    if comp_mode == "正壓 (Axial)":
        dim_oring_comp = sim_oring_h_final; dim_groove_comp = sim_groove_depth
        comp_title = "軸向壓縮率 (Axial Compression)"; hist_color = '#4CAF50'
    else:
        dim_oring_comp = sim_oring_w_final; dim_groove_comp = sim_groove_width_eff
        comp_title = "徑向壓縮率 (Radial Compression)"; hist_color = '#2196F3'

    with np.errstate(divide='ignore', invalid='ignore'):
        compression_sim = (dim_oring_comp - dim_groove_comp) / dim_oring_comp * 100
        fill_sim = (sim_oring_area_final / sim_groove_area) * 100
        compression_sim = np.nan_to_num(compression_sim, nan=0.0)
        fill_sim = np.nan_to_num(fill_sim, nan=0.0)

    mean_comp = np.mean(compression_sim); mean_fill = np.mean(fill_sim)
    pass_comp_mask = (compression_sim >= target_comp_min) & (compression_sim <= target_comp_max)
    yield_comp = (np.sum(pass_comp_mask) / sim_count) * 100
    ppm_comp = (100 - yield_comp) * 10000
    pass_fill_mask = (fill_sim >= target_fill_min) & (fill_sim <= target_fill_max)
    yield_fill = (np.sum(pass_fill_mask) / sim_count) * 100
    ppm_fill = (100 - yield_fill) * 10000
    pass_combined_mask = pass_comp_mask & pass_fill_mask
    yield_combined = (np.sum(pass_combined_mask) / sim_count) * 100
    ppm_combined = (100 - yield_combined) * 10000

    st.markdown("---")
    st.header("📊 分析報告")
    def get_yield_html(yield_val, ppm_val):
        return f"""<div style="margin-bottom: 5px;"><span class="metric-label">良率:</span> <span class="metric-value-large good-text">{yield_val:.2f} %</span>&nbsp;&nbsp;|&nbsp;&nbsp;<span class="metric-label">不良:</span> <span class="metric-value-large bad-text">{int(ppm_val)} ppm</span></div>"""

    st.subheader(comp_title)
    if mean_comp < 0: st.error(f"⚠️ 警告: 平均值為負 ({mean_comp:.2f}%)，存在間隙 (Gap)！")
    cr1, cr2 = st.columns([1, 2])
    with cr1:
        st.metric("平均壓縮率", f"{mean_comp:.3f} %")
        st.markdown(get_yield_html(yield_comp, ppm_comp), unsafe_allow_html=True)
    with cr2:
        fig_c, ax_c = plt.subplots(figsize=(6, 2.5))
        ax_c.hist(compression_sim, bins=50, color=hist_color, alpha=0.7, density=True)
        ax_c.axvline(target_comp_min, color='r', ls='--'); ax_c.axvline(target_comp_max, color='r', ls='--')
        ax_c.set_title("Compression Distribution", fontsize=10) 
        st.pyplot(fig_c, use_container_width=True)
    with st.expander("查看壓縮率 6-Sigma 詳細數據"):
        std_c = np.std(compression_sim)
        sigma_data = [{"Level": ("Mean" if i==0 else f"{i:+}σ"), "Value (%)": mean_comp + i * std_c} for i in range(-6, 7)]
        st.dataframe(pd.DataFrame(sigma_data).set_index("Level").T.style.format("{:.3f}"), use_container_width=True)

    st.markdown("---")
    st.subheader("填充率 (Fill Rate)")
    fr1, fr2 = st.columns([1, 2])
    with fr1:
        st.metric("平均填充率", f"{mean_fill:.3f} %")
        st.markdown(get_yield_html(yield_fill, ppm_fill), unsafe_allow_html=True)
    with fr2:
        fig_f, ax_f = plt.subplots(figsize=(6, 2.5))
        ax_f.hist(fill_sim, bins=50, color='#FF9800', alpha=0.7, density=True)
        ax_f.axvline(target_fill_min, color='r', ls='--'); ax_f.axvline(target_fill_max, color='r', ls='--')
        ax_f.set_title("Fill Rate Distribution", fontsize=10)
        st.pyplot(fig_f, use_container_width=True)
    with st.expander("查看填充率 6-Sigma 詳細數據"):
        std_f = np.std(fill_sim)
        sigma_data_f = [{"Level": ("Mean" if i==0 else f"{i:+}σ"), "Value (%)": mean_fill + i * std_f} for i in range(-6, 7)]
        st.dataframe(pd.DataFrame(sigma_data_f).set_index("Level").T.style.format("{:.3f}"), use_container_width=True)

    st.markdown(f"""<div class="summary-box"><h2 style="margin-top:0;">🌟 綜合評估結果 (Final Verdict)</h2><p style="font-size:16px;">同時滿足 <b>壓縮率 ({target_comp_min}-{target_comp_max}%)</b> 與 <b>填充率 ({target_fill_min}-{target_fill_max}%)</b> 之統計結果</p><div style="display: flex; justify-content: center; align-items: center; gap: 40px; margin-top: 10px;"><div><div style="color:#555; font-size:14px;">綜合良率 (Combined Yield)</div><div class="metric-value-large good-text" style="font-size:36px;">{yield_combined:.2f} %</div></div><div style="height: 50px; border-left: 2px solid #ccc;"></div><div><div style="color:#555; font-size:14px;">綜合不良率 (Defect Rate)</div><div class="metric-value-large bad-text" style="font-size:36px;">{int(ppm_combined)} ppm</div></div></div></div>""", unsafe_allow_html=True)

    # --- PDF 下載區 ---
    st.markdown("---")
    st.subheader("6. 匯出報告 (Export Report)")

    p_col1, p_col2 = st.columns(2)
    pdf_proj = p_col1.text_input("Project Name", "Sercomm_Gateway")
    pdf_eng = p_col2.text_input("Engineer", "ME Team")
    pdf_title = st.text_input("Report Title", f"O-Ring Analysis - {comp_mode}")

    try:
        sercomm_logo_bytes = base64.b64decode(SERCOMM_LOGO_BASE64)
    except:
        sercomm_logo_bytes = None

    # 自動備妥圖片
    buf_hist_c = BytesIO()
    fig_c.savefig(buf_hist_c, format="png", dpi=150, bbox_inches='tight', transparent=True)
    buf_hist_c.seek(0)

    buf_hist_f = BytesIO()
    fig_f.savefig(buf_hist_f, format="png", dpi=150, bbox_inches='tight', transparent=True)
    buf_hist_f.seek(0)

    # 資料
    all_inputs = oring_pdf_params + groove_pdf_params
    all_results = [
        {"item": "Compression Rate", "mean": mean_comp, "yield": yield_comp, "ppm": ppm_comp, "target": f"{target_comp_min}-{target_comp_max}%"},
        {"item": "Fill Rate", "mean": mean_fill, "yield": yield_fill, "ppm": ppm_fill, "target": f"{target_fill_min}-{target_fill_max}%"},
        {"item": "Combined (Total)", "mean": "-", "yield": yield_combined, "ppm": ppm_combined, "target": "-"}
    ]
    verdict_dict = {"yield": yield_combined, "ppm": ppm_combined}

    # 自動計算
    pdf_data = build_oring_pdf_report(
        project_name=pdf_proj,
        engineer_name=pdf_eng,
        title=pdf_title,
        input_data=all_inputs,
        result_data=all_results,
        verdict_data=verdict_dict,
        diagram_img_bytes=final_diagram_bytes,
        hist_comp_bytes=buf_hist_c.getvalue(),
        hist_fill_bytes=buf_hist_f.getvalue(),
        sercomm_logo_bytes=sercomm_logo_bytes
    )

    st.download_button(
        label="📥 下載完整 PDF 報告 (Download Report)",
        data=pdf_data,
        file_name=f"O_Ring_Report_{comp_mode[:2]}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
