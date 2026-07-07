import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Barrier & Cost Prediction App", layout="wide")

st.title("🎬 Barrier & Cost Prediction Web App")
st.markdown("ทำนายค่า OTR, WVTR และประมาณราคาต้นทุนโครงสร้างฟิล์มลามิเนต")

# 1. ฐานข้อมูลที่เพิ่มค่า Density (g/cm3) และ Price (บาท/กก.)
DATABASE = [
    {
        "material_category": "Metalized film",
        "film_name": "mPE(XE)-MDO",
        "ref_thickness_microns": 25.0,
        "ref_otr": 0.25,
        "ref_wvtr": 0.45,
        "density": 0.972,       # ความหนาแน่นเพื่อคำนวณน้ำหนัก
        "price_per_kg": 349.0,  # ราคา (บาท/กิโลกรัม)
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day"
    },
    {
        "material_category": "Metalized film",
        "film_name": "mMDOPE",
        "ref_thickness_microns": 28.0,
        "ref_otr": 0.1,
        "ref_wvtr": 1.46,
        "density": 0.935,
        "price_per_kg": 220.5,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day"
    },
    {
        "material_category": "Non-metalized film (AlOx)",
        "film_name": "MDOPE-AlOx",
        "ref_thickness_microns": 28.0,
        "ref_otr": 0.29,
        "ref_wvtr": 1.5,
        "density": 0.935,
        "price_per_kg": 253.75,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day"
    },
       {
        "material_category": "Non-metalized film (EVOH)",
        "film_name": "LL-EVOH",
        "ref_thickness_microns": 70.0,
        "ref_otr": 0.48,
        "ref_wvtr": 1.81,
        "density": 0.94,
        "price_per_kg": 91.2,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day"
    },
    {
      "material_category": "Non-metalized film (EVOH)",
        "film_name": "EF-F",
        "ref_thickness_microns": 12.0,
        "ref_otr": 0.60,
        "ref_wvtr": 86,
      "density": 1.19,
        "price_per_kg": 349,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day"
        },
    {
        "material_category": "Base Film",
        "film_name": "LL50",
        "ref_thickness_microns": 50,
        "ref_otr": 4000,
        "ref_wvtr": 7.5,
        "density": 0.92,
        "price_per_kg": 46.5,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day"
        },
    {
        "material_category": "Base Film",
        "film_name": "LL100",
        "ref_thickness_microns": 100,
        "ref_otr": 2000,
        "ref_wvtr": 4.0,
        "density": 0.92,
        "price_per_kg": 92.5,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day"
    },
    {
        "material_category": "Base Film",
        "film_name": "MDOPE_adj",
        "ref_thickness_microns": 25.0,
        "ref_otr": 1852,
        "ref_wvtr": 4.56,
        "density": 0.92,
        "price_per_kg": 80.0,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day"
        },
    {
        "material_category": "Base Film",
        "film_name": "MDOPE",
        "ref_thickness_microns": 25.0,
        "ref_otr": 4000.0,
        "ref_wvtr": 12,
        "density": 0.92,
        "price_per_kg": 80.0,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day"
        },
    {
        "material_category": "Base Film",
        "film_name": "Alu",
        "ref_thickness_microns": 11,
        "ref_otr": 0.01,
        "ref_wvtr": 0.01,
        "density": 2.7,
        "price_per_kg": 44.5,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day"
       },
    {
        "material_category": "Custom",
        "film_name": "กำหนดเอง (Custom Material)",
        "ref_thickness_microns": 25.0,
        "ref_otr": 0.0,
        "ref_wvtr": 0.0,
        "density": 1.0,
        "price_per_kg": 100.0,
        "unit_otr": "cc/m2.day",
        "unit_wvtr": "g/m2.day"
    }
]

df_db = pd.DataFrame(DATABASE)

with st.expander("🔍 ตรวจสอบฐานข้อมูลฟิล์มและราคาอ้างอิง (Database Lookup)"):
    show_df = df_db[df_db["film_name"] != "กำหนดเอง (Custom Material)"].copy()
    show_df.columns = ["หมวดหมู่", "ชื่อฟิล์ม", "ความหนาอ้างอิง (µm)", "Ref OTR", "Ref WVTR", "Density (g/cm³)", "ราคาอ้างอิง (บาท/กก.)", "หน่วย OTR", "หน่วย WVTR"]
    st.dataframe(show_df)

st.write("---")

st.header("🛠️ ออกแบบโครงสร้างชั้นฟิล์ม (Laminate Structure Design)")
num_layers = st.number_input("ระบุจำนวนชั้นฟิล์ม (Number of Layers)", min_value=1, max_value=10, value=3, step=1)

layers_data = []
total_film_cost = 0.0

# ส่วนที่ 1: ดึงราคาฟิล์มมาคำนวณอัตโนมัติรายชั้นตามความหนาจริง
for i in range(int(num_layers)):
    st.subheader(f"🎞️ ชั้นที่ {i+1} (Layer {i+1})")
    col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
    
    with col1:
        material_options = df_db["film_name"].tolist()
        selected_material = st.selectbox(f"เลือกวัสดุชั้นที่ {i+1}", material_options, key=f"mat_{i}")
        mat_info = df_db[df_db["film_name"] == selected_material].iloc[0]
        
    with col2:
        actual_thickness = st.number_input(f"ความหนาจริง (µm)", min_value=0.1, value=float(mat_info["ref_thickness_microns"]), key=f"thick_{i}")

    with col3:
        manual_toggle = st.toggle("ปรับค่าฟิล์มเอง", value=(selected_material == "กำหนดเอง (Custom Material)"), key=f"toggle_{i}")

    with col4:
        if manual_toggle:
            ref_otr = st.number_input(f"OTR เอง", min_value=0.0, value=float(mat_info["ref_otr"]), key=f"otr_{i}")
            ref_wvtr = st.number_input(f"WVTR เอง", min_value=0.0, value=float(mat_info["ref_wvtr"]), key=f"wvtr_{i}")
            density = st.number_input(f"Density เอง (g/cm³)", min_value=0.5, value=float(mat_info["density"]), key=f"dens_{i}")
            price_per_kg = st.number_input(f"ราคาเอง (บาท/กก.)", min_value=0.0, value=float(mat_info["price_per_kg"]), key=f"price_{i}")
            ref_thick = 25.0
        else:
            ref_otr = mat_info["ref_otr"]
            ref_wvtr = mat_info["ref_wvtr"]
            ref_thick = mat_info["ref_thickness_microns"]
            density = mat_info["density"]
            price_per_kg = mat_info["price_per_kg"]
            st.write(f"📊 ระบบดึงค่า: {price_per_kg} บาท/กก. (Density: {density})")

    ref_otr = max(ref_otr, 0.00001)
    ref_wvtr = max(ref_wvtr, 0.00001)

    actual_otr_layer = ref_otr * (ref_thick / actual_thickness)
    actual_wvtr_layer = ref_wvtr * (ref_thick / actual_thickness)
    
    # คำนวณราคาฟิล์มรายชั้น (บาท/ตารางเมตร)
    weight_per_m2 = actual_thickness * density
    film_cost_m2 = (weight_per_m2 / 1000) * price_per_kg
    total_film_cost += film_cost_m2

    layers_data.append({
        "layer_order": i + 1,
        "material": selected_material,
        "thickness": actual_thickness,
        "otr_layer": actual_otr_layer,
        "wvtr_layer": actual_wvtr_layer,
        "cost_m2": film_cost_m2
    })

st.write("---")

# ส่วนที่ 2: ปรับแต่งปริมาณกาวลามิเนต (แปรผันตาม Coat Weight)
total_adhesive_cost = 0.0
if num_layers > 1:
    st.header("🧪 ปรับแต่งปริมาณกาวลามิเนต (Adhesive Layer Specification)")
    st.info("💡 ราคาคิดอัตโนมัติจากสูตร: 0.122 บาท/g × Coat Weight (g/m²)")
    
    num_adhesives = int(num_layers - 1)
    col_adh = st.columns(num_adhesives)
    
    for j in range(num_adhesives):
        with col_adh[j]:
            coat_wt = st.number_input(f"Coat Wt. กาวรอยต่อที่ {j+1} (g/m²)", min_value=0.0, value=3.0, step=0.5, key=f"coat_{j}")
            adh_cost = 0.122 * coat_wt
            total_adhesive_cost += adh_cost
            st.caption(f"💰 ค่ากาวชั้นนี้: {adh_cost:.3f} บาท/m²")

st.write("---")

# ส่วนที่ 3: คำนวณตามสูตรใหม่พ่วงด้วย Variable Cost 15%
total_material_cost = total_film_cost + total_adhesive_cost  # สรุปต้นทุนเนื้อวัสดุแท้ ๆ
variable_cost = 0.15 * total_material_cost                   # ต้นทุนผันแปร 15%
total_laminated_film_cost = total_material_cost + variable_cost  # ราคาสุทธิสุดท้ายของโครงสร้างฟิล์ม

# ส่วนที่ 4: แดชบอร์ดสรุปผลรวม (Output Dashboard)
st.header("📊 แดชบอร์ดสรุปผลคุณสมบัติและราคา (Output Dashboard)")

total_thickness = sum(layer["thickness"] for layer in layers_data)

inv_otr_total = sum(1 / layer["otr_layer"] for layer in layers_data)
inv_wvtr_total = sum(1 / layer["wvtr_layer"] for layer in layers_data)
predicted_otr = 1 / inv_otr_total
predicted_wvtr = 1 / inv_wvtr_total

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric(label="📏 ความหนารวมลามิเนต", value=f"{total_thickness:.2f} µm")
    st.metric(label="💵 ต้นทุนรวมสุทธิ (Total Laminated Cost)", value=f"{total_laminated_film_cost:.4f} บาท/m²")
with col_m2:
    st.metric(label="🌬️ ค่าทำนาย OTR (ASTM D3985)", value=f"{predicted_otr:.4f} cc/m².day")
    st.metric(label="⚙️ ต้นทุนผันแปรโรงงาน (Variable Cost 15%)", value=f"{variable_cost:.4f} บาท/m²")
with col_m3:
    st.metric(label="💧 ค่าทำนาย WVTR (ASTM F1249)", value=f"{predicted_wvtr:.4f} g/m².day")
    st.metric(label="📦 ต้นทุนเฉพาะวัสดุ (Total Material Cost)", value=f"{total_material_cost:.4f} บาท/m²")

# ตารางแจกแจงโครงสร้างภายใน (ไม่มีการแสดงราคาแยกรายชั้นในตารางสรุปเพื่อความสะอาด)
st.subheader("📋 ตารางแจกแจงคุณสมบัติรายชั้น (Layer Analysis Table)")
summary_df = pd.DataFrame(layers_data)
table_df = summary_df[["layer_order", "material", "thickness", "otr_layer", "wvtr_layer"]].copy()
table_df.columns = ["ลำดับชั้น (Layer)", "วัสดุที่เลือก (Material)", "ความหนาจริง (microns)", "OTR ชั้นนี้ (cc/m².day)", "WVTR ชั้นนี้ (g/m².day)"]
st.dataframe(table_df.style.format({
    "ความหนาจริง (microns)": "{:.2f}",
    "OTR ชั้นนี้ (cc/m².day)": "{:.4f}",
    "WVTR ชั้นนี้ (g/m².day)": "{:.4f}"
}))

st.info("💡 หมายเหตุสูตรคำนวณ: Total Material Cost = [ค่าฟิล์มรวมทุกลักษณะความหนา + ค่ากาวรวม] -> จากนั้นระบบจะแสดงราคาสุทธิที่รวม Variable Cost 15% ให้ที่กรอบด้านบน")
