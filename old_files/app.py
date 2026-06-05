import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# إعدادات الصفحة
st.set_page_config(page_title="نظام العيادة والواتساب الذكي", page_icon="🏥", layout="wide")

CSV_FILE = "appointments.csv"

def get_next_weekday(weekday_index):
    """حساب تاريخ الأيام القادمة ميلادياً"""
    today = datetime.now()
    days_ahead = weekday_index - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return (today + timedelta(days_ahead)).strftime('%Y-%m-%d')

# تجهيز المواعيد المتاحة آلياً
time_slots = {
    "1": f"الأحد ({get_next_weekday(6)}) - 10:00 ص",
    "2": f"الاثنين ({get_next_weekday(0)}) - 01:00 ظ",
    "3": f"الثلاثاء ({get_next_weekday(1)}) - 04:00 ع"
}

def save_to_csv(name, phone, service, appointment_time):
    new_data = pd.DataFrame([[name, phone, service, appointment_time]], 
                            columns=["الاسم", "رقم الهاتف", "الخدمة المطلوبة", "الموعد"])
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data
    df.to_csv(CSV_FILE, index=False)

def check_time_conflict(chosen_time):
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        if "الموعد" in df.columns:
            return chosen_time in df["الموعد"].values
    return False

# العنوان الرئيسي
st.markdown("<h1 style='text-align: center; color: #075e54;'>🏥 نظام إدارة وحجز العيادة الآلي</h1>", unsafe_allow_html=True)
st.write("---")

# تقسيم الشاشة إلى عمودين (لوحة الموظف على اليمين والمحاكاة على اليسار)
col1, col2 = st.columns([1.2, 1])

# 📊 العمود الأول: لوحة تحكم الإدارة والموظف
with col1:
    st.markdown("### 📊 جدول مواعيد العيادة الحالي")
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("لا توجد حجوزات مسجلة بعد.")
    else:
        st.info("لا توجد حجوزات مسجلة بعد.")

# 📱 العمود الثاني: محاكاة محادثة الواتساب التفاعلية للعميل
with col2:
    st.markdown("### 📱 محاكاة بوت الواتساب التفاعلي")
    st.caption("أرسل كلمة 'حجز' لبدء تجربة المحادثة الآلية")
    
    # استخدام نظام الـ Session State في Streamlit لحفظ ذاكرة البوت
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "مرحباً بك في نظام عيادتنا الرقمي. لبدء حجز موعد جديد أرسل كلمة (حجز)."}]
    if "step" not in st.session_state:
        st.session_state.step = "welcome"
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}

    # عرض فقاعات المحادثة بشكل يشبه الواتساب الحقيقي
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # صندوق إدخال نص المحادثة (Chat Input)
    if user_input := st.chat_input("اكتب رسالتك هنا..."):
        # عرض رسالة المستخدم فوراً
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # محرك منطق البوت (الـ Logic) داخل بايثون
        reply = ""
        user_msg = user_input.strip()
        
        if st.session_state.step == "welcome":
            if any(word in user_msg.lower() for word in ["حجز", "احجز", "سلام", "مرحبا"]):
                st.session_state.step = "ask_name"
                reply = "أهلاً بك في عيادتنا! 🏥\n\nلطفاً، اكتب اسمك الكريم الكامل الثنائي لمتابعة الحجز:"
            else:
                reply = "مرحباً بك. لبدء عملية حجز موعد، يرجى كتابة كلمة (حجز)."
                
        elif st.session_state.step == "ask_name":
            st.session_state.user_data["name"] = user_msg
            st.session_state.step = "ask_service"
            reply = f"تشرفنا بك يا {user_msg}. ✨\n\nيرجى كتابة اسم الخدمة المطلوبة (مثال: استشارة عامة، متابعة):"
            
        elif st.session_state.step == "ask_service":
            st.session_state.user_data["service"] = user_msg
            st.session_state.step = "ask_time"
            reply = f"تم تسجيل الخدمة: ({user_msg}). 🗓️\n\nالرجاء اختيار الوقت المناسب لك بإرسال رقم الخيار فقط:\n\n"
            reply += f"1️⃣ {time_slots['1']}\n"
            reply += f"2️⃣ {time_slots['2']}\n"
            reply += f"3️⃣ {time_slots['3']}"
            
        elif st.session_state.step == "ask_time":
            if user_msg not in time_slots:
                reply = "⚠️ خيار غير صحيح. يرجى إرسال رقم الوقت المطلوب فقط (1 أو 2 أو 3):"
            else:
                chosen_time = time_slots[user_msg]
                
                # فحص تضارب المواعيد
                if check_time_conflict(chosen_time):
                    reply = f"❌ نعتذر منك! الموعد ({chosen_time}) حُجز للتو من قِبل مريض آخر.\n\nالرجاء اختيار رقم موعد آخر متاح:"
                else:
                    name = st.session_state.user_data["name"]
                    service = st.session_state.user_data["service"]
                    
                    # حفظ البيانات في ملف الـ CSV المشترك
                    save_to_csv(name, "966500000000", service, chosen_time)
                    
                    # إعادة تصفير المحادثة
                    st.session_state.step = "welcome"
                    st.session_state.user_data = {}
                    
                    reply = f"🎉 تم تأكيد حجزك بنجاح يا {name}!\n\n🔹 الخدمة: {service}\n🔹 الموعد: {chosen_time}\n\nبياناتك أصبحت في لوحة التحكم الآن! 🏥✨"
        
        # إضافة رد البوت للذاكرة وإعادة تحميل الصفحة ليعمل الجدول تلقائياً
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()