import streamlit as st
import time
import plotly.graph_objects as go
import pandas as pd

# إعدادات واجهة التطبيق
st.set_page_config(page_title="نظام إسناد للدرونات", page_icon="🛸", layout="wide")

# --- إضافة تنسيق CSS للحقوق في أسفل الصفحة ---
footer_style = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: #888;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }
    </style>
    <div class="footer">
        جميع الحقوق محفوظة لصالح فريق (عنان السماء) المشارك في #تحدي_ديفنسثون@
    </div>
"""

# --- نظام التنقل الجانبي ---
st.sidebar.title("🎛️ لوحة التحكم")
page = st.sidebar.radio("انتقل إلى:", ["اختبار الدرون", "سجل العمليات"])

# ---------------------------------------------------------
# الصفحة الأولى: اختبار الدرون
# ---------------------------------------------------------
if page == "اختبار الدرون":
    st.title("✈️ (Esnad) نظام التحقق من سلامة اقلاع الطائرة")
    st.markdown("---")

    st.sidebar.header("⚙️ إعدادات الاختبار")
    
    cargo_type = st.sidebar.selectbox("نوع الحمولة:", ["إعاشة", "ذخيرة", "سلاح", "أخرى"])
    weight = st.sidebar.number_input("وزن الشحنة (كجم):", min_value=0, max_value=200, value=20)
    weather = st.sidebar.selectbox("حالة الطقس:", ["صافي", "غائم", "ممطر", "عاصف"])
    wind_speed = st.sidebar.slider("سرعة الرياح (كم/ساعة):", 0, 50, 15)

    MAX_WEIGHT = 100
    MAX_WIND = 25

    st.subheader(f"📋 تحليل بيانات المهمة - ({cargo_type})")
    col1, col2, col3 = st.columns(3)
    col1.metric("الوزن الإجمالي", f"{weight} كجم")
    col2.metric("حالة الجو", weather)
    col3.metric("سرعة الرياح", f"{wind_speed} كم/س")

    has_error = False
    if weight > MAX_WEIGHT:
        st.error(f"❌ خطأ في الحمولة: وزن زائد بمقدار ({weight - MAX_WEIGHT} كجم)")
        has_error = True
    if weather in ["ممطر", "عاصف"]:
        st.error(f"❌ خطأ في البيئة: حالة الطقس غير آمنة ({weather})")
        has_error = True
    if wind_speed > MAX_WIND:
        if wind_speed > 35:
            st.error(f"❌ خطأ في الملاحة: سرعة الرياح خطيرة جداً")
            has_error = True
        else:
            st.warning(f"⚠️ تحذير ملاحة: سرعة الرياح عالية")

    if not has_error:
        st.success(f"✅ تم تأمين ( {cargo_type} ) .. جاهزة للإقلاع")

    # الرسم البياني
    st.markdown("#### 📊 مؤشرات الجاهزية الرقمية")
    weight_health = max(0, (1 - (weight / MAX_WEIGHT)) * 100)
    wind_health = max(0, (1 - (wind_speed / MAX_WIND)) * 100)
    weather_impact = 100 if weather == "صافي" else (80 if weather == "غائم" else 15)

    fig = go.Figure(data=[go.Bar(
        x=['سلامة الوزن', 'استقرار الرياح', 'تأثير الطقس'], 
        y=[weight_health, wind_health, weather_impact],
        marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'],
        text=[f"{v:.1f}%" for v in [weight_health, wind_health, weather_impact]],
        textposition='auto',
    )])
    fig.update_layout(yaxis_range=[0, 100], height=350)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# الصفحة الثانية: سجل العمليات
# ---------------------------------------------------------
elif page == "سجل العمليات":
    st.title("📜 سجل عمليات الدرون")
    st.markdown("تحليل أداء الرحلات السابقة وإحصائيات التسليم")
    st.markdown("---")

    # إحصائيات علوية
    stat1, stat2, stat3 = st.columns(3)
    stat1.metric("إجمالي الجولات", "12 جولة")
    stat2.metric("نسبة النجاح", "92%", delta="2% عن الشهر الماضي")
    stat3.metric("متوسط وزن الحمولة", "45 كجم")

    # بيانات الجدول
    data = {
        "التوقيت": ["2026-05-02 14:30", "2026-05-02 16:15", "2026-05-02 18:00"],
        "المنطقة": ["القطاع الشمالي", "نقطة إسناد 5", "منطقة العمليات أ"],
        "الحمولة": ["إعاشة", "ذخيرة", "إعاشة"],
        "الإحداثيات": ["24.7136, 46.6753", "24.7200, 46.6800", "24.7500, 46.7000"],
        "الحالة": ["✅ ناجحة", "⚠️ خلل في التوازن", "❌ إلغاء (رياح)"]
    }
    
    df = pd.DataFrame(data)
    st.table(df)

    st.markdown("### 🗺️ مواقع العمليات الأخيرة")
    map_data = pd.DataFrame({
        'lat': [24.7136, 24.7200, 24.7500],
        'lon': [46.6753, 46.6800, 46.7000]
    })
    st.map(map_data)

# --- عرض الحقوق في نهاية الكود لضمان ظهورها في كل الصفحات ---
st.markdown(footer_style, unsafe_allow_html=True)