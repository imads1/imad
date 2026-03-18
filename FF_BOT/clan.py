import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json
from reqClan_pb2 import MyMessage
from xTnito import xGeT

# إعدادات المفاتيح (ثابتة بناءً على ملفاتك)
K = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
I = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

# --- ضع بياناتك هنا ---
uid = ''  # معرف البوت
pas = '' 
c_id = 'clan id' # معرف الكلان الذي تريد الانضمام إليه
# --------------------

url = "https://clientbp.ggblueshark.com/RequestJoinClan"

print(f"[*] جاري جلب التوكن لـ UID: {uid}...")
T = xGeT(uid, pas)

if not T or "Error" in T:
    print("[!] فشل في الحصول على التوكن. تأكد من الحساب.")
else:
    print("[+] تم الحصول على التوكن بنجاح.")
    
    # صياغة رسالة Protobuf
    message = MyMessage()
    message.field_1 = int(c_id)
    serialized_data = message.SerializeToString()

    # تشفير البيانات باستخدام AES-CBC
    cipher = AES.new(K, AES.MODE_CBC, I)
    dt = cipher.encrypt(pad(serialized_data, AES.block_size))

    # الترويسات مع إضافة Authorization
    hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 10; m3 note Build/QD4A.200805.003)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/octet-stream",
    'Authorization': f"Bearer {T}",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB52",
}

    print(f"[*] جاري إرسال طلب الانضمام للكلان {c_id}...")
    try:
        response = requests.post(url, data=dt, headers=hr, timeout=15)
        
        print(f"\n[Result] Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ تم إرسال الطلب بنجاح! (تحقق من الكلان في اللعبة)")
        elif response.status_code == 401:
            print("❌ خطأ: التوكن غير صالح أو انتهت صلاحيته.")
        else:
            print(f"❌ فشل الطلب. الرد من السيرفر: {response.text}")
            
    except Exception as e:
        print(f"⚠️ حدث خطأ أثناء الاتصال: {e}")
