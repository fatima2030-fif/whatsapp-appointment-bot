import csv
from datetime import datetime
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


# دالة احترافية لحفظ البيانات في CSV لمنع التكرار وسد الثغرات
def save_appointment_to_csv(phone, service):
    file_name = "appointments.csv"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # نتحقق أولاً إذا كان العميل مسجلاً مسبقاً لمنع التكرار
    rows = []
    updated = False
    try:
        with open(file_name, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)

            for row in rows:
                if row and row[0] == phone:  # إذا وجدنا نفس رقم الهاتف
                    row[1] = service  # نحدث الخدمة
                    row[2] = current_time  # نحدث الوقت
                    updated = True
                    break
    except FileNotFoundError:
        # إذا لم يكن الملف موجوداً، فسيتم إنشاؤه في خطوة الكتابة
        pass

    if updated:
        # إعادة كتابة الملف بالبيانات المحدثة
        with open(file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        print(f"🔄 تم تحديث موعد العميل {phone} بنجاح.")
    else:
        # إضافة عميل جديد تماماً
        with open(file_name, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # إذا كان الملف فارغاً تماماً نضع العناوين أولاً
            if file.tell() == 0:
                writer.writerow(["رقم الهاتف", "الخدمة المطلوبة", "وقت التسجيل"])
            writer.writerow([phone, service, current_time])
        print(f"💾 تم حفظ عميل جديد {phone} في ملف CSV.")


# نقطة النهاية (Webhook) التي سيرسل Twilio البيانات إليها
@app.route("/bot", methods=["POST"])
def whatsapp_bot():
    # استقبال النص أو خيار الزر الذي أرسله العميل
    incoming_msg = request.values.get("Body", "").strip()
    # استقبال رقم هاتف العميل
    sender_phone = request.values.get("From", "")

    print(f"📩 رسالة قادمة من {sender_phone}: {incoming_msg}")

    # ردهم باستخدام نظام TwiML الخاص بتويليو
    resp = MessagingResponse()
    msg = resp.message()

    # المنطق البرمجي لقراءة ضغطة الزر
    if incoming_msg == "حجز موعد جديد":
        save_appointment_to_csv(sender_phone, "حجز موعد جديد")
        msg.body("شكراً لك! تم تسجيل طلبك لحجز موعد جديد بنجاح. 👍")

    elif incoming_msg == "تعديل/إلغاء موعد":
        save_appointment_to_csv(sender_phone, "تعديل/إلغاء موعد")
        msg.body("تم توجيه طلبك لتعديل الموعد، سنقوم بالتواصل معك قريباً.")

    elif incoming_msg == "تحدث مع الدعم":
        msg.body("يرجى الانتظار، سيقوم أحد موظفي الدعم بالتحدث معك الآن.")

    else:
        # إذا أرسل العميل أي نص آخر، البوت يرحب به ويعرض الأزرار مجدداً
        msg.body(
            "مرحباً بك! الرجاء استخدام الأزرار التفاعلية أسفل الرسالة لاختيار الخدمة."
        )

    return str(resp)


if __name__ == "__main__":
    # تشغيل السيرفر المحلي على منفذ 5000
    app.run(port=5000)