from flask import Flask, request
import pandas as pd
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CSV_FILE = "appointments.csv"

# قاموس بسيط لحفظ خطوات المريض (الاسم -> الخدمة -> الوقت)
user_sessions = {}

def get_next_weekday(weekday_index):
    """حساب التاريخ الميلادي آلياً للأيام القادمة"""
    today = datetime.now()
    days_ahead = weekday_index - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return (today + timedelta(days_ahead)).strftime('%Y-%m-%d')

@app.route("/webhook", methods=["POST"])
def whatsapp_bot():
    # استقبال الرقم ونص الرسالة القادمة من الواتساب الحقيقي
    incoming_msg = request.values.get('Body', '').strip()
    user_phone = request.values.get('From', '')
    
    # قائمة المواعيد المحدثة ميلادياً
    time_slots = {
        "1": f"الأحد ({get_next_weekday(6)}) - 10:00 ص",
        "2": f"الاثنين ({get_next_weekday(0)}) - 01:00 ظ",
        "3": f"الثلاثاء ({get_next_weekday(1)}) - 04:00 ع"
    }

    # 1️⃣ الخطوة الأولى: إذا كانت الرسالة جديدة
    if user_phone not in user_sessions:
        if any(word in incoming_msg.lower() for word in ["حجز", "احجز", "سلام", "مرحبا"]):
            user_sessions[user_phone] = {"step": "ask_name"}
            return "مرحباً بك في عيادتنا الرقمية! 🏥\nلطفاً، اكتب اسمك الكريم الكامل الثنائي لمتابعة الحجز:"
        else:
            return "مرحباً بك. لبدء حجز موعد جديد أرسل كلمة (حجز)."

    session = user_sessions[user_phone]

    # 2️⃣ الخطوة الثانية: استقبال الاسم وطلب الخدمة
    if session["step"] == "ask_name":
        session["name"] = incoming_msg
        session["step"] = "ask_service"
        return f"تشرفنا بك يا {incoming_msg}. ✨\nيرجى كتابة الخدمة المطلوبة (مثال: استشارة عامة، متابعة):"

    # 3️⃣ الخطوة الثالثة: استقبال الخدمة وعرض الأوقات
    elif session["step"] == "ask_service":
        session["service"] = incoming_msg
        session["step"] = "ask_time"
        
        reply = f"تم تسجيل الخدمة: ({incoming_msg}). 🗓️\nالرجاء اختيار الوقت المناسب بإرسال رقم الخيار فقط:\n\n"
        reply += f"1️⃣ {time_slots['1']}\n"
        reply += f"2️⃣ {time_slots['2']}\n"
        reply += f"3️⃣ {time_slots['3']}"
        return reply

    # 4️⃣ الخطوة الرابعة: استقبال الوقت وحفظ الحجز النهائي
    elif session["step"] == "ask_time":
        if incoming_msg not in time_slots:
            return "⚠️ خيار غير صحيح. الرجاء إرسال رقم الوقت المطلوب فقط (1 أو 2 أو 3):"
            
        chosen_time = time_slots[incoming_msg]
        name = session["name"]
        service = session["service"]
        
        # حفظ البيانات في ملف الـ CSV المشترك مع لوحة تحكم الموظف
        new_data = pd.DataFrame([[name, user_phone, service, chosen_time]], 
                                columns=["الاسم", "رقم الهاتف", "الخدمة المطلوبة", "الموعد"])
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            df = pd.concat([df, new_data], ignore_index=True)
        else:
            df = new_data
        df.to_csv(CSV_FILE, index=False)
        
        # إنهاء الجلسة بنجاح
        del user_sessions[user_phone]
        
        return f"🎉 تم تأكيد حجزك بنجاح يا {name}!\n\n🔹 الخدمة: {service}\n🔹 الموعد: {chosen_time}\n\nشكراً لثقتك بنا، وتم إرسال بياناتك للعيادة فوراً! 🏥✨"

if __name__ == "__main__":
    app.run(port=5000)