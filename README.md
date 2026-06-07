# 🏥 WhatsApp Appointment Booking Bot with Automated Excel Export

[English Description Below]

## 📋 وصف المشروع (باللغة العربية)
نظام ذكي ومؤتمت بالكامل لإدارة وحجز المواعيد للعيادات والمراكز الحيوية عبر تطبيق **WhatsApp**. يقوم البوت بتتبع العميل خطوة بخطوة (Multi-stage user tracking) عبر المحادثة وتخزين البيانات في قاعدة بيانات محلية، مع ميزة ذكية لمنع تعارض المواعيد، وفي نهاية كل حجز ناجح يتم تصدير البيانات وتحديثها تلقائياً داخل ملف **Excel (CSV)** باستخدام مكتبة Pandas ليسهل على الإدارة متابعتها.

### ✨ الميزات الرئيسية:
* **إدارة المراحل (State Management):** تتبع العميل بدقة من مرحلة اختيار الخدمة، التاريخ، وحتى اختيار الوقت.
* **منع تعارض المواعيد (Conflict Prevention):** فحص قاعدة البيانات قبل تثبيت الحجز للتأكد من عدم وجود حجز مسبق في نفس الوقت والتاريخ.
* **ميزة التصفير التلقائي (Session Reset):** إمكانية خروج العميل أو تصفير جلسته في أي وقت بمجرد إرسال كلمة "خروج" أو "إلغاء".
* **التصدير الفوري للإكسل (Automated Excel Export):** تحديث تلقائي لملف `appointments.csv` بترميز يدعم اللغة العربية (`utf-8-sig`) فور نجاح أي حجز.
* **الاستعلام عن المواعيد:** يمكن للعميل كتابة "مواعيدي" لاستعراض حجوزاته السابقة المرتبطة برقم جواله.

### 🛠️ التقنيات المستخدمة (Tech Stack):
* **Python 3**
* **Flask** (لبناء السيرفر واستقبال الـ Webhooks)
* **SQLite3** (لقاعدة البيانات الدائمة وجداول المراحل)
* **Pandas** (لمعالجة البيانات وتصديرها للإكسل)
* **Twilio API** (للربط وتوجيه رسائل الواتساب)
* **Ngrok** (لإنشاء نفق سحابي آمن للسيرفر المحلي)

---

## 📋 Project Description (English)
An intelligent, fully automated **WhatsApp Bot** for managing clinic appointments. The bot tracks user sessions step-by-step (Multi-stage state management) and stores information securely in a local database. It features an automated conflict check to prevent double-booking. Upon every successful booking, the bot utilizes the **Pandas** library to export and overwrite a unified **Excel (CSV)** sheet, enabling clinic administrators to seamlessly track schedules in real-time.

### ✨ Key Features:
* **Multi-Stage State Management:** Tracks user progress smoothly (Service Selection ➡️ Date Input ➡️ Time Slot Selection).
* **Booking Conflict Prevention:** Validates inputs against the database to ensure no two clients can book the exact same slot.
* **Session Reset Option:** Users can reset their current stage at any time by sending "خروج" (Exit) or "إلغاء" (Cancel).
* **Automated Excel Export:** Instant synchronization with `appointments.csv` utilizing `utf-8-sig` encoding for flawless Arabic character rendering.
* **Appointment Lookup:** Clients can view all their registered sessions instantly by texting "مواعيدي".

### 🛠️ Tech Stack:
* **Python 3**
* **Flask** (Micro-framework for handling Twilio Webhooks)
* **SQLite3** (Relational database for storing schedules and user stages)
* **Pandas** (Data analysis library used for live Excel/CSV generation)
* **Twilio API** (WhatsApp Business Gateway)
* **Ngrok** (Secure tunneling for local development)

---

## 🚀 كيفية التشغيل والاستخدام (How to Run)

### 1. تثبيت المكتبات (Installation)
```bash
pip install flask twilio pandas sqlite3