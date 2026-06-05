import csv
import os
import streamlit as st
import pywhatkit as kit
from datetime import date
import pandas as pd

DB_FILE = "appointments.csv"

def initialize_database():
    file_exists = os.path.isfile(DB_FILE)
    if not file_exists or os.path.getsize(DB_FILE) == 0:
        with open(DB_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Customer Name", "Phone Number", "Service", "Date"])

initialize_database()

# --- إعدادات الواجهة والتصميم المطور بدعم اللغة العربية (RTL) ---
st.set_page_config(page_title="Clinic System", page_icon="🏥", layout="centered")

# --- كود الحقن القسري للتنسيق العربي (Force RTL) ---
st.markdown("""
    <style>
    /* 1. قلب اتجاه التطبيق بالكامل والحاوية الرئيسية */
    .main, .stApp, [data-testid="stAppViewContainer"], .block-container {
        direction: rtl !important;
        text-align: right !important;
    }

    /* 2. استهداف العناوين التوضيحية فوق الخانات (Labels) بدقة */
    [data-testid="stWidgetLabel"] p, label {
        direction: rtl !important;
        text-align: right !important;
        justify-content: flex-start !important;
    }

    /* 3. ضبط محاذاة النص داخل خانات الإدخال والقوائم */
    input, select, textarea, [data-testid="stSelectbox"] {
        direction: rtl !important;
        text-align: right !important;
    }

    /* 4. ضمان محاذاة الجداول (Dataframes) لتبدأ من اليمين */
    [data-testid="stTable"], .stDataFrame, [data-testid="stExpander"] {
        direction: rtl !important;
        text-align: right !important;
    }

    /* 5. تنسيق زر الإرسال ليبقى متناسقاً */
    div.stButton > button {
        width: 100% !important;
        font-weight: bold !important;
    }
    </style>""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1e3d59;'>🏥 نظام إدارة حجوزات العيادة الذكي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #17b978; font-size: 16px;'>منصة تنظيم المواعيد المحترفة وأتمتة رسائل التأكيد</p>", unsafe_allow_html=True)
st.markdown("---")

st.subheader("📝 نموذج تسجيل بيانات المريض")

with st.form("booking_form", clear_on_submit=False):
    # استخدام الأعمدة المتقابلة مع الحفاظ على الترتيب العربي
    col1, col2 = st.columns(2)
    
    with col1:
        customer_name = st.text_input("👤 اسم المريض الكامل:", placeholder="مثال: منى أحمد").strip()
        selected_service = st.selectbox("💼 نوع الخدمة المطلوبة:", ["General Consultation", "Follow-up"])
        
    with col2:
        customer_phone = st.text_input("📞 رقم الواتساب (بالصيغة الدولية):", value="+966").strip()
        booking_date = st.date_input("📅 اختر تاريخ الحجز (ميلادي):", min_value=date.today())
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # نص الزر المعتمد
    submit_button = st.form_submit_button("إرسال وحفظ الحجز الآن 🚀")

if submit_button:
    date_str = str(booking_date)

    if not customer_name or not customer_phone or customer_phone == "+966":
        st.warning("⚠️ الرجاء تعبئة اسم المريض ورقم الجوال بشكل صحيح!")
    elif len(customer_phone) < 12 or not customer_phone.startswith("+"):
        st.error("❌ صيغة رقم الهاتف غير صحيحة! تأكدي من كتابة رمز الدولة (مثال: +9665xxxxxxxx).")
    else:
        is_booked = False
        try:
            with open(DB_FILE, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row.get("Date") and row["Date"].strip() == date_str:
                        is_booked = True
                        break
        except Exception:
            initialize_database()

        if is_booked:
            st.error(f"❌ عذراً! تاريخ [{date_str}] محجوز مسبقاً لمريض آخر. يرجى اختيار تاريخ بديل.")
        else:
            with open(DB_FILE, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([customer_name, customer_phone, selected_service, date_str])

            st.success(f"💾 تم تأكيد الموعد بنجاح للمريض ({customer_name}) بتاريخ {date_str}.")

            whatsapp_message = (
                f"مرحباً بكِ {customer_name} في عيادتنا الكريمة.\n\n"
                f"تم تأكيد موعدكِ بنجاح! 🎉\n"
                f"🔹 الخدمة: {selected_service}\n"
                f"🔹 التاريخ: {date_str}\n\n"
                f"نتطلع لرؤيتكِ قريباً. دمتم بصحة وعافية! ❤️"
            )
            
            with st.spinner("📱 جاري الاتصال بالواتساب ويب لإرسال الرسالة..."):
                try:
                    kit.sendwhatmsg_instantly(phone_no=customer_phone, message=whatsapp_message, wait_time=15, tab_close=True)
                    st.info("✅ تم توجيه الرسالة وإرسالها عبر المتصفح بنجاح!")
                except Exception as e:
                    st.error(f"⚠️ تم حفظ الحجز، ولكن تعذر فتح الواتساب تلقائياً. الخطأ: {e}")

# --- عرض جدول الحجوزات المباشر المنسق عربياً ---
st.markdown("---")
st.subheader("📅 جدول المواعيد المحجوزة حالياً")

try:
    if os.path.isfile(DB_FILE) and os.path.getsize(DB_FILE) > 0:
        df = pd.read_csv(DB_FILE)
        if not df.empty:
            # 🌟 تم تصحيح المعامل البرمجي هنا ليتمدد الجدول بأمان دون أخطاء
            st.dataframe(df, use_container_width=True)
        else:
            st.info("ℹ️ لا توجد مواعيد مسجلة في الجدول حالياً.")
    else:
        st.info("ℹ️ لا توجد مواعيد مسجلة في الجدول حالياً.")
except Exception as e:
    st.error(f"حدث خطأ أثناء قراءة جدول المواعيد: {e}")