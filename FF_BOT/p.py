import requests, urllib3, os, json, re, time, threading
from datetime import datetime
from protobuf_decoder.protobuf_decoder import Parser
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from google.protobuf import json_format
import Fo_pb2
import sys

# تعطيل تحذيرات urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class FriendManager:
    def __init__(self, uid=None, password=None):
        self.uid = uid or os.environ.get('BOT_UID', '')
        self.password = password or os.environ.get('BOT_PASSWORD', '')
        
        if not self.uid or not self.password:
            raise ValueError(f"UID and Password are required")
        
        self.key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        self.iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        
        self.AUTH_TOKEN = None
        self.get_jwt_token()
        
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.UIDS_FILE = os.path.join(self.BASE_DIR, 'uids.json')
        self.load_uids_data()
    
    def get_jwt_token(self):
        try:
            from xTnito import xGeT
            self.AUTH_TOKEN = xGeT(self.uid, self.password)
            return self.AUTH_TOKEN
        except Exception as e:
            print(f"Error getting JWT: {e}")
            return None
    
    def load_uids_data(self):
        try:
            with open(self.UIDS_FILE, 'r', encoding='utf-8') as f:
                self.uids_data = json.load(f)
        except:
            self.uids_data = {}
    
    def save_uids_data(self):
        with open(self.UIDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.uids_data, f, indent=4, ensure_ascii=False)
    
    def EnC_AEs(self, HeX):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher.encrypt(pad(bytes.fromhex(HeX), AES.block_size)).hex()
    
    def EnC_Uid(self, n):
        e = []
        while n:
            e.append((n & 0x7F) | (0x80 if n > 0x7F else 0))
            n >>= 7
        return bytes(e).hex()
    
    def CrEaTe_VarianT(self, field_number, value):
        field_header = (field_number << 3) | 0
        return self.EnC_Vr(field_header) + self.EnC_Vr(value)
    
    def CrEaTe_LenGTh(self, field_number, value):
        field_header = (field_number << 3) | 2
        encoded_value = value.encode() if isinstance(value, str) else value
        return self.EnC_Vr(field_header) + self.EnC_Vr(len(encoded_value)) + encoded_value
    
    def CrEaTe_ProTo(self, fields):
        packet = bytearray()    
        for field, value in fields.items():
            if isinstance(value, dict):
                nested_packet = self.CrEaTe_ProTo(value)
                packet.extend(self.CrEaTe_LenGTh(field, nested_packet))
            elif isinstance(value, int):
                packet.extend(self.CrEaTe_VarianT(field, value))           
            elif isinstance(value, str) or isinstance(value, bytes):
                packet.extend(self.CrEaTe_LenGTh(field, value))           
        return packet.hex()
    
    def EnC_Vr(self, n):
        e = []
        while n:
            e.append((n & 0x7F) | (0x80 if n > 0x7F else 0))
            n >>= 7
        return bytes(e)
    
    def SEnd(self, UrL, PyL):
        if not self.AUTH_TOKEN:
            self.get_jwt_token()
            if not self.AUTH_TOKEN:
                return None, None, None
        
        try:
            H = requests.session().post(UrL, headers={
                "Expect": "100-continue",
                "X-Unity-Version": "2018.4.11f1",
                "X-GA": "v1 1",
                "ReleaseVersion": "OB52",
                "Authorization": "Bearer " + self.AUTH_TOKEN,
                "Host": "clientbp.ggblueshark.com"
            }, data=PyL, verify=False)
            
            if H.status_code == 401:
                self.AUTH_TOKEN = None
                return self.SEnd(UrL, PyL)
            
            return H.status_code, H.content, H.text
            
        except Exception as e:
            print(f"API Error: {e}")
            return None, None, None
    
    def Add_FrEind(self, Uid, days=None):
        try:
            UrL = 'https://clientbp.ggblueshark.com/RequestAddingFriend'
            PyL = f'08f795f0b53210{self.EnC_Uid(int(Uid))}1816'
            
            PyL = bytes.fromhex(self.EnC_AEs(PyL))
            status, _, _ = self.SEnd(UrL, PyL)
            
            if status == 200 and days:
                expire_time = self.add_uid_with_expiry(Uid, days)
                return {
                    'success': True,
                    'uid': Uid,
                    'expire_time': expire_time,
                    'expire_date': datetime.fromtimestamp(expire_time).strftime('%Y-%m-%d %H:%M:%S')
                }
            
            return {'success': status == 200, 'uid': Uid, 'status': status}
        except Exception as e:
            print(f"Error adding friend: {e}")
            return {'success': False, 'error': str(e)}
    
    def DeLetE_FrEind(self, Uid):
        try:
            UrL = 'https://clientbp.ggblueshark.com/RemoveFriend'
            PyL = f'08a7c4839f1e10{self.EnC_Uid(int(Uid))}'
            PyL = bytes.fromhex(self.EnC_AEs(PyL))
            status, _, _ = self.SEnd(UrL, PyL)
            
            if str(Uid) in self.uids_data:
                self.uids_data[str(Uid)]['status'] = 'removed'
                self.save_uids_data()
            
            return {'success': status == 200, 'uid': Uid}
        except Exception as e:
            print(f"Error removing friend: {e}")
            return {'success': False, 'error': str(e)}
    
    def Show_FrEinds(self):
        UrL = 'https://clientbp.ggblueshark.com/GetFriend'
        PyL = {1: 1, 2: 1, 7: 1}
        PyL = bytes.fromhex(self.EnC_AEs(self.CrEaTe_ProTo(PyL)))
        S, H, A = self.SEnd(UrL, PyL)
        
        if H is None:
            return []
        
        try:
            f = Fo_pb2.Friends()
            f.ParseFromString(H)
            P = json.loads(json_format.MessageToJson(f).encode('utf-8').decode('unicode_escape'))
            
            friends_list = []
            for entry in P.get("field1", []):
                friend_id = entry.get("ID", "غير معروف")
                friend_name = "غير معروف"
                for key, value in entry.items():
                    if isinstance(value, str) and key != "ID":
                        friend_name = value
                        break
                friends_list.append({
                    'id': str(friend_id),
                    'name': friend_name
                })
            
            return friends_list
        except Exception as e:
            print(f"Parse Error: {e}")
            return []
    
    def add_uid_with_expiry(self, uid, days):
        expire_time = int(time.time()) + (days * 24 * 60 * 60)
        self.uids_data[uid] = {
            "status": "active",
            "expire": expire_time,
            "added_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.save_uids_data()
        return expire_time


def parse_args():
    """قراءة الـ arguments يدوياً من sys.argv"""
    args = {
        'action': None,
        'uid': None,
        'days': None,
        'bot_uid': None,
        'bot_password': None
    }
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg in ['add', 'remove', 'show']:
            args['action'] = arg
        elif arg == '--bot-uid' and i + 1 < len(sys.argv):
            args['bot_uid'] = sys.argv[i + 1]
            i += 1
        elif arg == '--bot-password' and i + 1 < len(sys.argv):
            args['bot_password'] = sys.argv[i + 1]
            i += 1
        elif args['action'] and not args['uid'] and not arg.startswith('-'):
            args['uid'] = arg
        elif args['action'] and args['uid'] and not args['days'] and not arg.startswith('-'):
            try:
                args['days'] = int(arg)
            except:
                pass
        
        i += 1
    
    return args


def main():
    args = parse_args()
    
    uid = args['bot_uid'] or os.environ.get('BOT_UID', '')
    password = args['bot_password'] or os.environ.get('BOT_PASSWORD', '')
    
    if not uid or not password:
        print(json.dumps({'success': False, 'error': f'BOT_UID and BOT_PASSWORD required'}, ensure_ascii=False))
        sys.exit(1)
    
    try:
        manager = FriendManager(uid, password)
        
        if args['action'] == 'add':
            if not args['uid'] or not args['days']:
                print(json.dumps({'success': False, 'error': 'UID and days are required'}, ensure_ascii=False))
                sys.exit(1)
            
            result = manager.Add_FrEind(args['uid'], args['days'])
            print(json.dumps(result, ensure_ascii=False))
            
        elif args['action'] == 'remove':
            if not args['uid']:
                print(json.dumps({'success': False, 'error': 'UID is required'}, ensure_ascii=False))
                sys.exit(1)
            
            result = manager.DeLetE_FrEind(args['uid'])
            print(json.dumps(result, ensure_ascii=False))
            
        elif args['action'] == 'show':
            friends = manager.Show_FrEinds()
            for friend in friends:
                print(f"ID: {friend['id']}")
                print(f"Name: {friend['name']}")
                print("-" * 30)
        else:
            print(json.dumps({'success': False, 'error': 'Unknown action'}, ensure_ascii=False))
            sys.exit(1)
                
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
