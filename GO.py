import subprocess
import time
import sys
import os

# اسم الملف الذي تريد تشغيله وإعادة تشغيله
script_to_run = "app.py"

# المدة بالثواني بين كل إعادة تشغيل (5 دقائق * 60 ثانية)
restart_interval_seconds = 20 * 60

# متغير لتخزين العملية الجارية
process = None

def start_script():
    """
    دالة لبدء تشغيل السكربت والتحقق من وجود الملف.
    """
    global process
    if not os.path.exists(script_to_run):
        print(f"خطأ: الملف '{script_to_run}' غير موجود في نفس المجلد.")
        print("الرجاء التأكد من وضع هذا السكربت في نفس مجلد ملف البوت.")
        sys.exit(1) # إيقاف البرنامج مع رمز خطأ

    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] بدء تشغيل {script_to_run}...")
    # نستخدم sys.executable لضمان تشغيل السكربت بنفس إصدار بايثون
    process = subprocess.Popen([sys.executable, script_to_run])
    print(f"تم تشغيل العملية بنجاح. معرف العملية (PID): {process.pid}")

def stop_script():
    """
    دالة لإيقاف السكربت الحالي.
    """
    global process
    if process:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] إيقاف العملية {process.pid}...")
        process.kill() # .kill() لإغلاق فوري وقوي
        process = None
        print("تم إيقاف العملية بنجاح.")

if __name__ == "__main__":
    try:
        while True:
            start_script()
            
            print(f"العملية ستعمل لمدة {restart_interval_seconds / 60} دقائق.")
            print(f"سيتم إعادة التشغيل التالية في: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + restart_interval_seconds))}")
            
            time.sleep(restart_interval_seconds)
            
            stop_script()
            
            print("--- دورة جديدة ---")

    except KeyboardInterrupt:
        print("\nتم استلام طلب إيقاف (Ctrl+C).")
        stop_script()
        print("تم إغلاق المشغّل.")
        sys.exit(0)
    except Exception as e:
        print(f"حدث خطأ غير متوقع: {e}")
        stop_script() # محاولة إيقاف العملية الحالية قبل الخروج
        sys.exit(1)
