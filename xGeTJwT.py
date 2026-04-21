import requests , time , binascii , json , urllib3 , random
from datetime import datetime
from Black import *
from multiprocessing.dummy import Pool as ThreadPool

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def Ua():
    TmP = "GarenaMSDK/4.0.13 ({}; {}; {};)"
    return TmP.format(random.choice(["iPhone 13 Pro", "iPhone 14", "iPhone XR", "Galaxy S22", "Note 20", "OnePlus 9", "Mi 11"]) , 
                     random.choice(["iOS 17", "iOS 18", "Android 13", "Android 14"]) , 
                     random.choice(["en-SG", "en-US", "fr-FR", "id-ID", "th-TH", "vi-VN"]))

def xGeT(u, p):
    """الدالة المعدلة لاستخدام UID و PW مباشرة من السكريبت الرئيسي"""
    print(f"جاري توليد التوكن لـ UID: {u}")
    try:
        r = requests.Session().post(
            "https://100067.connect.garena.com/oauth/guest/token/grant",
            headers={
                "Host": "100067.connect.garena.com",
                "User-Agent": Ua(),
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "close"
            },
            data={
                "uid": u,
                "password": p,
                "response_type": "token",
                "client_type": "2",
                "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
                "client_id": "100067"
            },
            verify=False
        )
        
        if r.status_code == 200:
            T = r.json()
            print("تم الحصول على التوكن بنجاح من Garena")
            a, o = T["access_token"], T["open_id"]
            jwt_token = xJwT(a, o)
            if jwt_token:
                print("تم توليد JWT بنجاح")
                return jwt_token
            else:
                print("فشل في توليد JWT")
                return None
        else:
            print(f"خطأ في الاستجابة من Garena: {r.status_code}")
            return None
    except Exception as e:
        print(f"حدث خطأ في xGeT: {str(e)}")
        return None

def xJwT(a, o):
    """دالة توليد JWT باستخدام التوكن المباشر"""
    try:
        dT = bytes.fromhex('1a13323032362d30342d30382031393a32333a3233220966726565206669726528013a07312e3132332e324232416e64726f6964204f532039202f204150492d3238202850492f72656c2e636a772e32303232303531382e313134313333294a0848616e6468656c6452074469676963656c5a045749464960b60a68ee0572033330307a287838362d3634205353453320535345342e3120535345342e3220415658207c2032343030207c20348001b5178a010f416472656e6f2028544d292036343092010d4f70656e474c20455320332e329a012b476f6f676c657c37313961636639652d303962662d343864332d383366662d303237613938616463356338a2010e3130322e3135382e3136372e3837aa01026172b201203766306433306234633063393636336538333934356636663631346432393835ba010134c2010848616e6468656c64ca01104173757320415355535f493030354441d201024d45ea014066376235336637323738353034396265363937383630346465323831356333636337633031373233356635346561623431643861333439633138666234333263f00101ca02074469676963656cd2020457494649ca03203734323862323533646566633136343031386336303461316562626665626466e003b4b502e803a0ff01f003af13f80384078004968c028804b4b5029004968c029804b4b502c80402d2043f2f646174612f6170702f636f6d2e6474732e667265656669726574682d77727a6f5850706d5875326f306d53455870684b75673d3d2f6c69622f61726d3634e00401ea045f31376536613434373830336131376534663539653366643733346566633561657c2f646174612f6170702f636f6d2e6474732e667265656669726574682d77727a6f5850706d5875326f306d53455870684b75673d3d2f626173652e61706bf00403f804028a050236349a050a32303139313230323730a80503b205094f70656e474c455332b805ff01c00504e005c451ea0507616e64726f6964f2055c4b717348542f5233354a456369536e314f32426a5a57794c38683838713555707a5a6862544d4b614e4f64697a36717775354d494b416b384657764e452b54532b7a62314962356d46597448665468335a576b423863794b7968383df805e7e4068206267b226375725f72617465223a6e756c6c2c22737570706f72745f65746332223a66616c73657d8806019006019a060134a2060134b206224506154054540d574d065d4759054459423c5b515a000c6b08030b3d55596e010631')
        
        # تحديث البيانات الديناميكية
        dT = dT.replace(b'2026-04-08 19:23:23', str(datetime.now())[:-7].encode())
        dT = dT.replace('f7b53f72785049be6978604de2815c3cc7c017235f54eab41d8a349c18fb432c', a.encode())
        dT = dT.replace(b'7f0d30b4c0c9663e83945f6f614d2985', o.encode())
        
        PyL = bytes.fromhex(EnC_AEs(dT.hex()))
        r = requests.Session().post(
            "https://loginbp.ggwhitehawk.com/MajorLogin",
            headers={
                "Expect": "100-continue",
                "X-Unity-Version": "2018.4.11f1",
                "X-GA": "v1 1",
                "ReleaseVersion": "OB53",
                "Authorization": "Bearer ",
                "Host": "loginbp.ggwhitehawk.com"
            },
            data=PyL,
            verify=False
        )
        
        if r.status_code == 200:
            response_data = json.loads(DeCode_PackEt(binascii.hexlify(r.content).decode('utf-8')))
            return response_data['8']['data']
        else:
            print(f"خطأ في MajorLogin: {r.status_code}")
            return None
    except Exception as e:
        print(f"حدث خطأ في xJwT: {str(e)}")
        return None