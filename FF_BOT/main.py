import requests , os , psutil , sys , jwt , pickle , json , binascii , time , urllib3 , xKEys , base64 , datetime , re , socket , threading
from protobuf_decoder.protobuf_decoder import Parser
from xTnito import * 
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

BOT_NAME = "DEFAULT_BOT"
DEVELOPER_NAME = "DEFAULT_DEV"
CHANNEL_NAME = ""

def AuTo_ResTartinG():
    time.sleep(6 * 60 * 60)
    print('\n - AuTo ResTartinG The BoT ... ! ')
    p = psutil.Process(os.getpid())
    for handler in p.open_files():
        try:
            os.close(handler.fd)
        except Exception as e:
            print(f" - Error CLose Files : {e}")
    for conn in p.net_connections():
        try:
            if hasattr(conn, 'fd'):
                os.close(conn.fd)
        except Exception as e:
            print(f" - Error CLose Connection : {e}")
    sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))
    python = sys.executable
    os.execl(python, python, *sys.argv)
       
def ResTarT_BoT():
    print('\n - ResTartinG The BoT ... ! ')
    p = psutil.Process(os.getpid())
    open_files = p.open_files()
    connections = p.net_connections()
    for handler in open_files:
        try:
            os.close(handler.fd)
        except Exception:
            pass           
    for conn in connections:
        try:
            conn.close()
        except Exception:
            pass
    sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))
    python = sys.executable
    os.execl(python, python, *sys.argv)

def GeT_Time(timestamp):
    last_login = datetime.fromtimestamp(timestamp)
    now = datetime.now()
    diff = now - last_login   
    d = diff.days
    h , rem = divmod(diff.seconds, 3600)
    m , s = divmod(rem, 60)    
    return d, h, m, s

def Time_En_Ar(t): 
    return ' '.join(t.replace("Day","يوم").replace("Hour","ساعة").replace("Min","دقيقة").replace("Sec","ثانية").split(" - "))
    
Thread(target = AuTo_ResTartinG , daemon = True).start()
            
class FF_CLient():

    def __init__(self, id, password):
        self.id = id
        self.password = password
        self.Get_FiNal_ToKen_0115()     
            
    def Connect_SerVer_OnLine(self , Token , tok , host , port , key , iv , host2 , port2):
            global CliEnts2 , DaTa2 , AutH
            try:
                self.AutH_ToKen_0115 = tok    
                self.CliEnts2 = socket.create_connection((host2 , int(port2)))
                self.CliEnts2.send(bytes.fromhex(self.AutH_ToKen_0115))                  
            except:pass        
            while True:
                try:
                    self.DaTa2 = self.CliEnts2.recv(99999)
                    if '0500' in self.DaTa2.hex()[0:4] and len(self.DaTa2.hex()) > 30:	         	    	    
                            self.packet = json.loads(DeCode_PackEt(f'08{self.DaTa2.hex().split("08", 1)[1]}'))
                            self.AutH = self.packet['5']['data']['7']['data'] 
                            self.dT = json.loads(DeCode_PackEt(self.DaTa2.hex()[10:]))
                            self.dT = self.dT["5"]["data"]["1"]["data"] 
                            
                        
                            self.CliEnts2.send(maq(self.dT, key, iv))      		   
                except:pass    	
                                                            
    def Connect_SerVer(self , Token , tok , host , port , key , iv , host2 , port2):
            global CliEnts       
            self.AutH_ToKen_0115 = tok    
            self.CliEnts = socket.create_connection((host , int(port)))
            self.CliEnts.send(bytes.fromhex(self.AutH_ToKen_0115))  
            self.DaTa = self.CliEnts.recv(1024)          	        
            threading.Thread(target=self.Connect_SerVer_OnLine, args=(Token , tok , host , port , key , iv , host2 , port2)).start()
            self.Exemple = xMsGFixinG('12345678')
            while True:      
                try:
                    
                    self.DaTa = self.CliEnts.recv(1024)
                    
                    if len(self.DaTa) == 0 or len(self.DaTa2) == 0:	            		
                        try:            		    
                            self.CliEnts.close() ; self.CliEnts2.close() ; self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)                    		                    
                        except:
                            try:
                                self.CliEnts.close() ; self.CliEnts2.close() ; self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                            except:
                                self.CliEnts.close() ; self.CliEnts2.close() ; ResTarT_BoT()	            
                                      
                    if '1200' in self.DaTa.hex()[0:4] and 900 > len(self.DaTa.hex()) > 100:
                        if b"***" in self.DaTa:self.DaTa = self.DaTa.replace(b"***",b"106")         
                        try:
                           self.BesTo_data = json.loads(DeCode_PackEt(self.DaTa.hex()[10:]))	       
                           self.input_msg = 'besto_love' if '8' in self.BesTo_data["5"]["data"] else self.BesTo_data["5"]["data"]["4"]["data"]
                        except: self.input_msg = None	   	 
                        self.DeCode_CliEnt_Uid = self.BesTo_data["5"]["data"]["1"]["data"]
                        self.CliEnt_Uid = EnC_Uid(self.DeCode_CliEnt_Uid , Tp = 'Uid')
                               
                    if 'besto_love' in self.input_msg[:10]:
                        self.CliEnts.send(xSEndMsg(f'''
[b][c][FFD3EF] > أهلاً بك في بوت {BOT_NAME} <

[ffffff] للحصول على قائمة الأوامر

 فقط أرسل /start أو /help !

 للقائمة العربية => ar

 للقائمة الإنجليزية => en

 استمتع باستخدام البوت مع الميزات الجديدة وأفضل سرعة

 لا تنسَ متابعتي 

 انستا => {CHANNEL_NAME}
 تلغرام => {CHANNEL_NAME}

[FFD3EF]المطور {DEVELOPER_NAME}
''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                       
                        time.sleep(0.3)
                        self.CliEnts.close() ; self.CliEnts2.close()
                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	                    	 	 
                                                               
                    if b'/start' in self.DaTa or b'/help' in self.DaTa or 'en' in self.input_msg[:2]:
                        self.result = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                        if self.result:
                            self.Status , self.Expire = self.result
                            self.CliEnts.send(xSEndMsg(f'''
[b][c][FFD700]  Welcome To {BOT_NAME} BOT [ffffff]
    
> CommandEs AvaibLe For U : <
     
[ffffff]  /6 => [FFD3EF]6 In Sqiud
     
[ffffff]  /5 => [FFD3EF]5 In Sqiud
     
[ffffff]  /3 => [FFD3EF]3 In Sqiud	 
     
[ffffff]  /c5/id => [FFD3EF]SEnd Squid 5
     
[ffffff]  /c6/id => [FFD3EF]SEnd Squid 6
     
[ffffff]  /c3/id => [FFD3EF]SEnd Squid 3

[ffffff]  /get/id => [FFD3EF]GeT FrEind To Sq
     
[ffffff]  /st/id => [FFD3EF]GeT PLayEr s'Status
     
[ffffff]  /sp/id => [FFD3EF]SPam Room
     
[ffffff]  /pp/id => [FFD3EF]SPam Squid
     
[ffffff]  ++ id => [FFD3EF]GeT InFo Of Uid
     
[ffffff]  /visit id => [FFD3EF]SEnd Visits To Uid\n''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CliEnts.send(xSEndMsg(f'''
[b][c][FFD700]  Another Cmds[ffffff]
    
[ffffff] /jn[tmcd] =>[FFD3EF] join sqwad    

[ffffff] /em/ [id_Emote] =>[FFD3EF] emote you
    
[ffffff] /em1/[id_friend] [id_Emote] =>[FFD3EF] emote friend's      
    
[ffffff] /code [tmcd] =>[FFD3EF]lag sq
     
[ffffff] /psps/[id] =>[FFD3EF]sq 5 + chb7
                                                       
[ffffff] /ou/[id] =>[FFD3EF]snd gst via id

[ffffff]/msg/[tmcd] [msg] =>[FFD3EF]snd msg to tmcd


    \n''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)		
                            self.CliEnts.send(xSEndMsg(f'''
[b][c][FFD700]━━━━━━━━━━━━[ffffff]
[ffffff]  ReGister InFo :
     
[ffffff]  Uid => [90EE90]{xMsGFixinG(self.DeCode_CliEnt_Uid)} 
[ffffff]  Status => [90EE90]{self.Status} - Good !
[ffffff]  Expire In => [90EE90]{self.Expire}
[ffffff]  Version => [90EE90]V2 X[ffffff]
[FFD700]━━━━━━━━━━━━[ffffff]
[FFD700]  DevLoped By : {DEVELOPER_NAME} \n''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CliEnts.close() ; self.CliEnts2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	   	       		
                        elif False == self.result:
                            DeLet_Uid(self.DeCode_CliEnt_Uid , Token)  
                            
                    elif 'ar' in self.input_msg[:2]:
                        self.result = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                        if self.result:
                            self.Status , self.Expire = self.result
                            self.CliEnts.send(xSEndMsg(f'''
[b][c][FFD700]مرحبا بك في البوت ايها المستخدم
[ffffff]لتحويل سكواد الى أوضاع مختلفة[90EE90]
/6
/5
/3
[ffffff]لإرسال السكواد الى صديقك[90EE90]
/c6/id
/c5/id
/c3/id
[ffffff]لجلب لاعب الى السكواد[90EE90]
/get/id
[ffffff]لزيادة 100 لايك يومية[90EE90]
/like id
[ffffff]لإرسال سبام طلبات الصداقة[90EE90]
/spam id
[ffffff]لإرسال سبام دخول السكواد[90EE90]
/pp/id
[ffffff]لجلب معلومات بروفايل اللاعب[90EE90]
++ id
[ffffff]لجلب حالة اللاعب و مالك السكواد[90EE90]
/st/id
[ffffff]لإرسال سبام الروم الى لاعب[90EE90]
/sp/id
[ffffff] تابعني على \\n[FFD3EF]{CHANNEL_NAME}\n''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CliEnts.send(xSEndMsg(f'''
    [b][c][FFD700]أوامر ميزة الشبح 
    
    [ffffff]لإرسال الاق بالشبح[90EE90]
    
    [ffffff]/code [تيم كود] [90EE90]
    
    [ffffff]لفتح سكواد مع الشبح[90EE90]	
    
    [ffffff]/psps/[id] [90EE90]
                                                       
    [ffffff]لإرسال الشبح عبر الايدي[90EE90]
    
    [ffffff]/ou/[id] [90EE90]
    
    [ffffff]لعمل سبام علا لاعب 24ساعة [90EE90]	
    
    [ffffff]/V[id] [90EE90]
    
    [ffffff]لايقاف السبام[90EE90]	
    
    [ffffff]/D[id] [90EE90]
    
    [ffffff]لأرسال رساله للسكواد عبر تيم كود[90EE90]
    
    [ffffff]/msg/[tmcd] [90EE90]
\n''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)		
                            self.CliEnts.send(xSEndMsg(f'''[b][c]
[ffffff]الوقت المتبقي لديك أيها المستخدم هو\n\n[FFD3EF]{Time_En_Ar(self.Expire)}\n\n[ffffff]لشراء البوت او سرفر بإسمك تواصل\n[90EE90]{CHANNEL_NAME}\n''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))	        
                            time.sleep(0.3)
                            self.CliEnts.close() ; self.CliEnts2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	   	       		
                        elif False == self.result:
                            DeLet_Uid(self.DeCode_CliEnt_Uid , Token)
                     
                    elif '/code' in self.input_msg[:5]:
                        self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                        self.id , self.nm = (self.input_msg[6:].split(" ", 1) if " " in self.input_msg[6:] else [self.input_msg[6:], f"{CHANNEL_NAME}"])  
                        self.Zx = ChEck_Commande(self.id)
                        if self.ChEck_ReGister and True == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] JoinInG With Code {self.id}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            self.CliEnts2.send(GenJoinSquadsPacket(self.id, key, iv))
                            time.sleep(0.3)
                            if '0500' in self.DaTa2.hex()[0:4] and len(self.DaTa2.hex()) > 30:
                                self.dT = json.loads(DeCode_PackEt(self.DaTa2.hex()[10:]))
                                sq = self.dT["5"]["data"]["31"]["data"]
                                idT = self.dT["5"]["data"]["1"]["data"]
                                print(idT)	            	            	            	            	            	            
                                self.CliEnts2.send(ExiT('000000' , key , iv))	            	            
                                for i in range(200):
                                   self.CliEnts2.send(GenJoinSquadsPacket(self.id, key, iv))
                                   time.sleep(0.1)
                                   self.CliEnts2.send(ExiT('000000' , key , iv))
                                   self.CliEnts2.send(ghost_pakcet(idT, self.nm , sq , key , iv))
                        elif False == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /cood <code>\n - Ex : /cood 517284\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        elif False == self.ChEck_ReGister:
                            DeLet_Uid(self.DeCode_CliEnt_Uid , Token)
                    elif any(cmd in self.input_msg for cmd in ['/msg/', '/ban/']):
                        if not ChEck_The_Uid(self.DeCode_CliEnt_Uid):
                            DeLet_Uid(self.DeCode_CliEnt_Uid, Token)
                            return
                        cmd_type = '/msg/' if '/msg/' in self.input_msg else '/ban/'
                        target_id = self.input_msg[5:].split(" ", 1)[0]
                        message_text = self.input_msg[5:].split(" ", 1)[1] if " " in self.input_msg[5:] else (
                            f'[b][c][{ArA_CoLor()}]Dont Forget to follow me  : {CHANNEL_NAME}' if cmd_type == '/msg/' else 'حصلت و تحشالك ولد عمي'
                        )
                        if not ChEck_Commande(target_id):
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - Invalid ID format\n - Ex : {cmd_type}{self.Exemple}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                            time.sleep(0.1)
                            self.CliEnts.close(); self.CliEnts2.close()
                            self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2)
                            return 
                        action_msg = "sending message" if cmd_type == '/msg/' else "tchitchi msg"
                        self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] Wait for {action_msg} : {target_id}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))                        
                        self.CliEnts2.send(GenJoinSquadsPacket(target_id, key, iv))
                        time.sleep(0.5)

                        if '0500' in self.DaTa2.hex()[0:4] and len(self.DaTa2.hex()) > 30:
                            self.dT = json.loads(DeCode_PackEt(self.DaTa2.hex()[10:]))
                            idT = self.dT["5"]["data"]["1"]["data"]
                            sq = self.dT["5"]["data"]["17"]["data"]
                            self.CliEnts.send(Auth_Chat(idT, str(sq), key, iv))
                            self.CliEnts2.send(ExiT('000000', key, iv))
                            for i in range(20):
                                self.CliEnts.send(xSendTeamMsg(f'\n[b][c][{ArA_CoLor()}] {message_text}\n', idT , key, iv))
                                time.sleep(0.2)
                                
                            success_msg = "succesfull snd message" if cmd_type == '/msg/' else "BAN msg SS"
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] {success_msg} : {target_id}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                        time.sleep(0.1)
                        self.CliEnts.close(); self.CliEnts2.close()
                        self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2)  	              
                           	    
                    elif any(cmd in self.input_msg for cmd in ['/vip/', '/list', '/-vip/']):
                        if '/vip/' in self.input_msg:
                            self.id = self.input_msg[5:]
                            self.Zx = ChEck_Commande(self.id)
                            if True == self.Zx:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] جاري إضافة ID إلى القائمة: {xMsGFixinG(self.id)}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                success, message = add_vip_to_github(self.id)
                                if success:
                                    self.CliEnts.send(xSEndMsg(f'\n[b][c][90EE90]{message}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                else:
                                    self.CliEnts.send(xSEndMsg(f'\n[b][c][FF0000]{message}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            else:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - الصيغة الصحيحة: /vip/<آيدي>\n - مثال: /vip/{self.Exemple}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        elif '/list' in self.input_msg:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] جاري جلب قائمة IDs...\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                            vip_ids = list_vip_ids()
                            if vip_ids:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][90EE90]قائمة IDs الموجودة ({len(vip_ids)}):\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                                
                                for i, vid in enumerate(vip_ids, 1):
                                    self.CliEnts.send(xSEndMsg(f'\n[b][c][ffffff]{i}. {xMsGFixinG(vid)}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                                    time.sleep(0.1)
                            else:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][FF0000]لا توجد أي IDs في القائمة\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                        elif '/-vip/' in self.input_msg:
                            del_id = self.input_msg[6:] 
                            if ChEck_Commande(del_id):
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] جاري حذف ID: {xMsGFixinG(del_id)}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                                success, message = remove_vip_from_github(del_id)
                                if success:
                                    self.CliEnts.send(xSEndMsg(f'\n[b][c][90EE90]{message}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                                else:
                                    self.CliEnts.send(xSEndMsg(f'\n[b][c][FF0000]{message}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                            else:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - الصيغة الصحيحة: /-vip/<آيدي>\n - مثال: /-vip/{self.Exemple}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                        elif False == self.result:
                            DeLet_Uid(self.DeCode_CliEnt_Uid , Token)
                        time.sleep(0.3)
                        self.CliEnts.close() ; self.CliEnts2.close()
                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)                                   
                    elif '/spam' in self.input_msg[:5]: 	
                            self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                            self.id = self.input_msg[6:]
                            self.Zx = ChEck_Commande(self.id)
                            if self.ChEck_ReGister and True == self.Zx:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] SendinG Spam To {xMsGFixinG(self.id)}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))   
                                self.Req = Requests_SPam(self.id)	     
                                if True == self.Req:
                                    self.CliEnts.send(xSEndMsg(f'\n[b][c][90EE90]SuccEssFuLLy SendinG SPam\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                    time.sleep(0.3)
                                    self.CliEnts.close() ; self.CliEnts2.close()
                                    self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	
                                             
                                elif False == self.Req:
                                    self.CliEnts.send(xSEndMsg(f'\n[b][c][FFD700]FaiLEd SendinG SPam\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                    self.CliEnts.close() ; self.CliEnts2.close()
                                    self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                                    
                            elif False == self.Zx:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /spam <id>\n - Ex : /spam {self.Exemple}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                                    
                            elif False == self.ChEck_ReGister:
                                DeLet_Uid(self.DeCode_CliEnt_Uid , Token)      
                                                               
                    elif '++' in self.input_msg[:2]:   
                            self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                            self.id = self.input_msg[3:]
                            self.Zx = ChEck_Commande(self.id)
                            if self.ChEck_ReGister and True == self.Zx:			    
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] GeTinG InFo FoR {xMsGFixinG(self.id)}\n' , 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.3)
                                self.CliEnts.send(xSEndMsg(GeT_PLayer_InFo(self.id , Token) , 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.3)
                                self.CliEnts.close() ; self.CliEnts2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                                
                            elif False == self.Zx:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use ++ <id>\n - Ex : ++ {self.Exemple}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                                                    
                            elif False == self.ChEck_ReGister:
                                DeLet_Uid(self.DeCode_CliEnt_Uid , Token)          	               	    	
                    elif any(cmd in self.input_msg for cmd in ['/5', '/6', '/3']):
                        self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                        if self.ChEck_ReGister:
                            if '/5' in self.input_msg:
                                squad_size = 5
                                msg = "GeneRaTinG 5 In Squid"
                            elif '/6' in self.input_msg:
                                squad_size = 6
                                msg = "GeneRaTinG 6 In Squid"
                            else: 
                                squad_size = 3
                                msg = "GeneRaTinG 3 In Squid"
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}]{msg}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                            self.CliEnts2.send(OpEnSq(key, iv))
                            time.sleep(0.5)
                            self.CliEnts2.send(cHSq(squad_size, self.DeCode_CliEnt_Uid, key, iv))
                            time.sleep(0.5)
                            self.CliEnts2.send(SEnd_InV(1, self.DeCode_CliEnt_Uid, key, iv))
                            time.sleep(3)
                            self.CliEnts2.send(ExiT('000000', key, iv))
                            time.sleep(0.1)
                            self.CliEnts.close(); self.CliEnts2.close()
                            self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2)
                        elif False == self.ChEck_ReGister:
                            DeLet_Uid(self.DeCode_CliEnt_Uid, Token)
                                    
                    elif any(cmd in self.input_msg for cmd in ['/c5/', '/c6/', '/c3/']):
                        self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                        target_id = self.input_msg[4:]
                        if '/c5/' in self.input_msg:
                            squad_size = 5
                            msg = f"5 In Squid To {xMsGFixinG(target_id)}"
                        elif '/c6/' in self.input_msg:
                            squad_size = 6
                            msg = f"6 In Squid To {xMsGFixinG(target_id)}"
                        elif '/c3/' in self.input_msg:  
                            squad_size = 3
                            msg = f"3 In Squid To {xMsGFixinG(target_id)}"
                        self.Zx = ChEck_Commande(target_id)
                        if self.ChEck_ReGister and True == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}]{msg}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                            self.CliEnts2.send(OpEnSq(key, iv))
                            time.sleep(0.5)
                            self.CliEnts2.send(cHSq(squad_size, self.DeCode_CliEnt_Uid, key, iv))
                            time.sleep(0.5)
                            self.CliEnts2.send(SEnd_InV(1, target_id, key, iv))
                            time.sleep(3)
                            self.CliEnts2.send(ExiT('000000', key, iv))
                            time.sleep(0.1)
                            self.CliEnts.close(); self.CliEnts2.close()
                            self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2)
                        elif False == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /c5/<id> or /c6/<id> or /c3/<id>\n - Ex : /c5/{self.Exemple}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                            time.sleep(0.1)
                            self.CliEnts.close(); self.CliEnts2.close()
                            self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2)                    
                        elif False == self.ChEck_ReGister:
                            DeLet_Uid(self.DeCode_CliEnt_Uid, Token)
                                                            
                    elif '/get/' in self.input_msg[:5]:
                            self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                            self.id = self.input_msg[5:]
                            self.Zx = ChEck_Commande(self.id)    
                            if self.ChEck_ReGister and True == self.Zx:  
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] GeTinG PLayer {xMsGFixinG(self.id)}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                self.CliEnts2.send(OpEnSq(key , iv))
                                time.sleep(0.5)
                                self.CliEnts2.send(cHSq(5 , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.5)			         
                                self.CliEnts2.send(SEnd_InV(1 , self.id , key , iv))
                                time.sleep(0.5)
                                self.CliEnts2.send(SEnd_InV(1 , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(3)
                                self.CliEnts.close() ; self.CliEnts2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2) 

                            elif False == self.Zx:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /get/<id>\n - Ex : /get/{self.Exemple}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                                     
                            elif False == self.ChEck_ReGister:
                                DeLet_Uid(self.DeCode_CliEnt_Uid , Token)    		             

                    if '/pp/' in self.input_msg[:4]:
                        self.id = self.input_msg[4:]	 
                        self.Zx = ChEck_Commande(self.id)
                        if True == self.Zx:	            		     
                            for i in range(20):
                                threading.Thread(target=lambda: self.CliEnts2.send(SPamSq(self.id , key , iv))).start()
                            time.sleep(0.1)    			         
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] SuccEss Spam To {xMsGFixinG(self.id)}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CliEnts.close() ; self.CliEnts2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	            		      	
                        elif False == self.Zx: 
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /pp/<id>\n - Ex : /pp/{self.Exemple}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))	
                            time.sleep(0.1)
                            self.CliEnts.close() ; self.CliEnts2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	            		

                    elif '/sp/' in self.input_msg[:4]:
                        self.res , self.time = ChEck_Limit(self.DeCode_CliEnt_Uid , 'Spam_Room')
                        self.id , self.nm = (self.input_msg[4:].split(" ", 1) if " " in self.input_msg[4:] else [self.input_msg[4:], "C4 - Team"])
                        self.Zx = ChEck_Commande(self.id)	
                        if self.res and True == self.Zx:
                            try:	      		    
                                self.CliEnts2.send(GeT_Status(self.id , key , iv))
                                time.sleep(0.3)
                            except:pass    	            	
                            if '0f00' in self.DaTa2.hex()[:4]:
                                try:	            		
                                    packet = self.DaTa2.hex()[10:]
                                    self.BesTo_data = json.loads(DeCode_PackEt(packet))
                                    self.room_uid = self.BesTo_data['5']['data']['1']['data']['15']['data']
                                    self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] SuccEss SpamRoom To {xMsGFixinG(self.room_uid)}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                    for i in range(999):
                                        threading.Thread(target=lambda: self.CliEnts2.send(SPam_Room(self.id , self.room_uid , self.nm , key , iv))).start()
                                    time.sleep(0.1)
                                    self.CliEnts.close() ; self.CliEnts2.close()
                                    self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	    		       
                                except:pass
                                
                        elif False == self.res and True == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][ffffff] U Reched Max Limit To SEnd SPam\n Try AfTer : {xMsGFixinG(self.time)} !\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CliEnts.close() ; self.CliEnts2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                            
                        elif False == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /sp/<id> <name>\n - Ex : /sp/{self.Exemple} C4 Team\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CliEnts.close() ; self.CliEnts2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	
                    elif '/ou/' in self.input_msg[:4]:
                        self.id_part = self.input_msg[4:]
                        parts = self.id_part.split(" ", 1)
                        self.id = parts[0] 
                        self.ghost_name = parts[1] if len(parts) > 1 else f"{CHANNEL_NAME}"
                        self.Zx = ChEck_Commande(self.id)
                        if True == self.Zx:
                            try:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] جاري إرسال طلب انضمام إلى سكواد اللاعب {xMsGFixinG(self.id)}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                                self.CliEnts2.send(SPamSq(self.id, key, iv))
                                time.sleep(2)
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] في انتظار قبول الطلب...\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                                time.sleep(2)
                                self.CliEnts2.send(AccEpT(self.id, self.AutH, key, iv))
                                time.sleep(2)
                                start_time = time.time()
                                while time.time() - start_time < 10:  
                                    if '0500' in self.DaTa2.hex()[0:4] and len(self.DaTa2.hex()) > 30:
                                        packet = self.DaTa2.hex()[10:]
                                        self.BesTo_data = json.loads(DeCode_PackEt(packet))
                                        self.sq_code = self.BesTo_data["5"]["data"]["31"]["data"]
                                        self.sq_leader = self.BesTo_data["5"]["data"]["1"]["data"]
                                        self.CliEnts2.send(ExiT('000000', key, iv))
                                        time.sleep(1)
                                        self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] جاري إرسال الشبح "{self.ghost_name}" إلى السكواد {xMsGFixinG(self.sq_code)}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                                        self.CliEnts2.send(ghost_pakcet(self.sq_leader, self.ghost_name, self.sq_code, key, iv))
                                        time.sleep(0.01)
                                        self.CliEnts2.send(ExiT('000000', key, iv))
                                        time.sleep(0.01)
                                        self.CliEnts.send(xSEndMsg(f'\n[b][c][90EE90]تم إرسال الشبح "{self.ghost_name}" بنجاح!\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                                        break
                                    time.sleep(0.1)
                                else:
                                    self.CliEnts.send(xSEndMsg(f'\n[b][c][FF0000]لم يتم قبول الطلب خلال الوقت المحدد\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))                                
                            except Exception as e:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][FF0000]حدث خطأ: {str(e)}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                            time.sleep(0.3)
                            self.CliEnts.close(); self.CliEnts2.close()
                            self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2)
                            
                        elif False == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - الصيغة الصحيحة: /ou/<آيدي>\n - مثال: /ou/{self.Exemple}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                            time.sleep(0.1)
                            self.CliEnts.close(); self.CliEnts2.close()
                            self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2)
                            
                    # --- أمر إضافة الحماية ---
                    # --- أمر الحماية +s ---
                    elif '+X' == self.input_msg[:2]:
                        target_id = self.input_msg[2:].strip()
                        if not target_id: target_id = self.DeCode_CliEnt_Uid
                        
                        res = manage_protection("add", target_id)
                        if res == True:
                            msg = f"تم إضافة الأيدي {target_id} لقائمة الحماية بنجاح"
                        elif res == "already_protected":
                            msg = "هذا الأيدي محمي بالفعل"
                        else:
                            msg = "فشل إضافة الحماية"
                            
                        self.CliEnts.send(xSEndMsg(f"\n[b][c][90EE90]{msg}\n", 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                        time.sleep(0.3)
                        self.CliEnts.close(); self.CliEnts2.close()
                        self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2)

                    # --- أمر السبام /s ---
                    elif '/V' == self.input_msg[:2]:
                        target_id = self.input_msg[2:].strip()
                        if not target_id: target_id = self.DeCode_CliEnt_Uid

                        # التحقق من الحماية أولاً
                        if manage_protection("check", target_id):
                            self.CliEnts.send(xSEndMsg(f"\n[b][c][FF0000]عذراً، هذا الأيدي محمي من السبام!\n", 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                        else:
                            try:
                                res_raw = send_spam_stop_request("spam", target_id)
                                if "success" in res_raw or "يعمل بالفعل" in res_raw:
                                    msg_to_send = "تم سبام بنجاح"
                                else:
                                    msg_to_send = "فشل سبام"
                                self.CliEnts.send(xSEndMsg(f"\n[b][c][90EE90]{msg_to_send}\n", 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                            except:
                                self.CliEnts.send(xSEndMsg(f"\n[b][c][FF0000]فشل سبام\n", 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                        
                        time.sleep(0.3)
                        self.CliEnts.close(); self.CliEnts2.close()
                        self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2)

                    # --- أمر الإيقاف /d ---
                    elif '/D' == self.input_msg[:2]:
                        target_id = self.input_msg[2:].strip()
                        if not target_id: target_id = self.DeCode_CliEnt_Uid
                        try:
                            res_raw = send_spam_stop_request("stop", target_id)
                            if "success" in res_raw or "إيقاف" in res_raw:
                                msg_to_send = "تم الإيقاف بنجاح"
                            else:
                                msg_to_send = "فشل الإيقاف"
                            self.CliEnts.send(xSEndMsg(f"\n[b][c][FFD3EF]{msg_to_send}\n", 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                        except:
                            self.CliEnts.send(xSEndMsg(f"\n[b][c][FF0000]فشل الإيقاف\n", 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                        time.sleep(0.3)
                        self.CliEnts.close(); self.CliEnts2.close()
                        self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2)
                                                                                                            
                    elif '/st/' in self.input_msg[:4]:
                        self.id = self.input_msg[4:]
                        self.Zx = ChEck_Commande(self.id)
                        if True == self.Zx:	            		     
                            try:
                                  self.CliEnts2.send(GeT_Status(self.id , key , iv))
                                  time.sleep(0.3)
                            except:pass   
                            if '0f00' in self.DaTa2.hex()[:4]:
                                packet = self.DaTa2.hex()[10:]
                                try:
                                    self.BesTo_data = json.loads(DeCode_PackEt(packet))
                                    self.target_id = self.BesTo_data["5"]["data"]["1"]["data"]["1"]["data"]
                                    self.h = self.BesTo_data["5"]["data"]["1"]["data"]["3"]["data"]
                                except:pass						
                                try:status_data = self.BesTo_data["5"]["data"]["1"]["data"]["3"]["data"]
                                except:pass
                                try:		
                                    if self.h == 1:
                                        try:
                                            self.last = self.BesTo_data["5"]["data"]["1"]["data"]["4"]["data"]	                
                                        except:
                                            self.last = 'No DaTa !'
                                        self.name = GeT_Name(self.target_id , Token)
                                        self.name = str(self.name)
                                        self.CliEnts.send(xSEndMsg(f"[b][c]\n Status InFo Of The PLayer : \n\n[{ArA_CoLor()}]PLayer Uid : {xMsGFixinG(self.target_id)}\nPLayer Status : SoLo\nPLayer s'Name : {self.name}\nLast Login : {xMsGFixinG(datetime.fromtimestamp(self.last).strftime('%I:%M %p %d/%m/%y'))}\n\n[ffffff] Dev : Saber kadri OfficieL\n", 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                        time.sleep(0.3)
                                        self.CliEnts.close() ; self.CliEnts2.close()
                                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)					
                                    elif self.h == 2:
                                        self.leader = xMsGFixinG(self.BesTo_data["5"]["data"]["1"]["data"]["8"]["data"])
                                        self.group_count = self.BesTo_data["5"]["data"]["1"]["data"]["9"]["data"]
                                        self.group_count2 = self.BesTo_data["5"]["data"]["1"]["data"]["10"]["data"]
                                        self.leader_id = self.BesTo_data["5"]["data"]["1"]["data"]["8"]["data"]
                                        self.name = GeT_Name(self.leader_id , Token)
                                        self.name = str(self.name)
                                        self.time = self.BesTo_data["5"]["data"]["1"]["data"]["4"]["data"]
                                        self.CliEnts.send(xSEndMsg(f"[b][c]\n Status InFo Of The PLayer : \n\n[{ArA_CoLor()}]PLayer Uid : {xMsGFixinG(self.target_id)}\nPLayer Status : His In Squid\nSquid s'Leader : {self.leader}\nLeader s'Name : {self.name}\nSquid Count : {self.group_count}/{self.group_count2 + 1}\nLast Login : {xMsGFixinG(datetime.fromtimestamp(self.time).strftime('%I:%M %p %d/%m/%y'))}\n\n[ffffff] Dev : Saber kadri OfficieL\n", 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                        time.sleep(0.3)
                                        self.CliEnts.close() ; self.CliEnts2.close()
                                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                                    elif self.h in [3 , 5]:
                                        self.CliEnts.send(xSEndMsg(f"[b][c]\n Status InFo Of The PLayer : \n\nPLayer Uid : {xMsGFixinG(self.target_id)}\nPLayer Status : In Game\nLast Login : {xMsGFixinG(datetime.fromtimestamp(self.time).strftime('%I:%M %p %d/%m/%y'))}\n\n[ffffff]  Dev : Saber kadri OfficieL\n", 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                        time.sleep(0.3)
                                        self.CliEnts.close() ; self.CliEnts2.close()
                                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                                    else:
                                        self.CliEnts.send(xSEndMsg(f'\n[b][c][FFD700]FaiLEd GeTinG STaTus InFo\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                        time.sleep(0.3)
                                        self.CliEnts.close() ; self.CliEnts2.close()
                                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                                except:pass
                        if False == self.Zx: self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /st/<id>\n - Ex : /st/{self.Exemple}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))	
  
                    elif '/em1/' in self.input_msg[:5]:
                        self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                        parts = self.input_msg[5:].strip().split()
                        if len(parts) < 2:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - Use: /em1/ <uid1> <uid2> <uid3> <uid4> <uid5> <emote_id>\n - Ex: /em1/ 123456789 987654321 555555555 909000012\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                            time.sleep(0.3)
                            self.CliEnts.close(); self.CliEnts2.close()
                            self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2)
                            continue
                        uid1 = uid2 = uid3 = uid4 = uid5 = None
                        s = False
                        emote_id = None
                        try:
                            if len(parts) == 6:
                                uid1 = int(parts[0])
                                uid2 = int(parts[1])
                                uid3 = int(parts[2])
                                uid4 = int(parts[3])
                                uid5 = int(parts[4])
                                emote_id = int(parts[5])
                            elif len(parts) == 5:
                                uid1 = int(parts[0])
                                uid2 = int(parts[1])
                                uid3 = int(parts[2])
                                uid4 = int(parts[3])
                                emote_id = int(parts[4])
                            elif len(parts) == 4:
                                uid1 = int(parts[0])
                                uid2 = int(parts[1])
                                uid3 = int(parts[2])
                                emote_id = int(parts[3])
                            elif len(parts) == 3:
                                uid1 = int(parts[0])
                                uid2 = int(parts[1])
                                emote_id = int(parts[2])
                            elif len(parts) == 2:
                                uid1 = int(parts[0])
                                emote_id = int(parts[1])
                        except ValueError as ve:
                            print("ValueError:", ve)
                            s = True
                        except Exception as e:
                            print("Exception:", e)
                            s = True
                            try:
                                emote_id = int(parts[-1])
                            except:
                                emote_id = None
                        if s or emote_id is None:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][FF0000]Error: Invalid format!\nUse: /em1/ <uid1> <uid2> <uid3> <emote_id>\nExample: /em1/ 123456789 987654321 909000012\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                            time.sleep(0.3)
                            self.CliEnts.close(); self.CliEnts2.close()
                            self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2)
                            continue
                        all_uids = []
                        if uid1: all_uids.append(str(uid1))
                        if uid2: all_uids.append(str(uid2))
                        if uid3: all_uids.append(str(uid3))
                        if uid4: all_uids.append(str(uid4))
                        if uid5: all_uids.append(str(uid5))
                        all_valid = all(ChEck_Commande(uid) for uid in all_uids)
                        if self.ChEck_ReGister and all_valid:
                            uid_display = ", ".join([xMsGFixinG(uid) for uid in all_uids])
                            message = f'\n[b][c][{ArA_CoLor()}] Sending emote {emote_id} to {len(all_uids)} players: {uid_display}\n'
                            self.CliEnts.send(xSEndMsg(message, 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                            success_count = 0
                            for player_uid in all_uids:
                                try:
                                    self.CliEnts2.send(EmoTe(int(player_uid), int(emote_id), key, iv))
                                    success_count += 1
                                    time.sleep(0.1)  
                                except Exception as e:
                                    error_msg = f'\n[b][c][FF0000]Error sending to {xMsGFixinG(player_uid)}\n'
                                    self.CliEnts.send(xSEndMsg(error_msg, 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                            if success_count > 0:
                                success_msg = f'\n[b][c][90EE90]Successfully sent emote {emote_id} to {success_count}/{len(all_uids)} players!\n'
                                self.CliEnts.send(xSEndMsg(success_msg, 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                            
                        elif not self.ChEck_ReGister:
                            DeLet_Uid(self.DeCode_CliEnt_Uid, Token)
                        elif not all_valid:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][FF0000]Error: One or more UIDs have invalid format!\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                        
                        time.sleep(0.3)
                        self.CliEnts.close(); self.CliEnts2.close()
                        self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2)           
                    elif '/em/' in self.input_msg[:4]:
                        self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                        self.id = self.input_msg[4:]	 
                        self.Zx = ChEck_Commande(self.id)
                        if self.ChEck_ReGister and True == self.Zx:
                            time.sleep(0.2)                           
                            self.CliEnts2.send(EmoTe(self.DeCode_CliEnt_Uid, self.id, key, iv))
                            time.sleep(0.2)
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] done  \n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.2)
                            self.CliEnts.send(xSendTeamMsg(f'\n[b][c][{ArA_CoLor()}]Done Work Emote',idT , key , iv))                                                        
                        elif False == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /cood <code>\n - Ex : /cood 517284\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        elif False == self.ChEck_ReGister:
                            DeLet_Uid(self.DeCode_CliEnt_Uid , Token)      
                    elif '/jn' in self.input_msg[:3]:
                        self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                        self.id = self.input_msg[3:]	 
                        self.Zx = ChEck_Commande(self.id)
                        if self.ChEck_ReGister and True == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] JoinInG With Code {self.id}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            self.CliEnts2.send(GenJoinSquadsPacket(self.id, key, iv))
                            time.sleep(0.3)
                            time.sleep(0.5)
                            if '0500' in self.DaTa2.hex()[0:4] and len(self.DaTa2.hex()) > 30:
                                self.dT = json.loads(DeCode_PackEt(self.DaTa2.hex()[10:]))
                                idT = self.dT["5"]["data"]["1"]["data"]
                                sq = self.dT["5"]["data"]["14"]["data"]
                                self.CliEnts.send(Auth_Chat(idT, sq, key, iv))
                                self.CliEnts.send(xSendTeamMsg(f'\n[b][c][{ArA_CoLor()}] أهلاً وسهلاً بكم في السكواد! \nتم الانضمام بواسطة بوت Beho\nتم التعرف بنجاح علي رسايل السكواد \nيمكنك الان استعمال بوت الرقصات بكل اريحيه \n',idT , key , iv))
                                time.sleep(0.3)
                                              
                        elif False == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /jn/<code>\n - Ex : /jn/517284\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        elif False == self.ChEck_ReGister:
                            DeLet_Uid(self.DeCode_CliEnt_Uid , Token)                                                           
                    
                    elif '/ex' in self.input_msg[:3]:
                        self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                        
                        self.Zx = ChEck_Commande(self.id)
                        if self.ChEck_ReGister and True == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] done\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            self.CliEnts2.send(ExiT('000000', key, iv))
                            time.sleep(0.3)                                           
                        elif False == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /ex\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        elif False == self.ChEck_ReGister:
                            DeLet_Uid(self.DeCode_CliEnt_Uid , Token)

                    elif '/psps/' in self.input_msg[:6]:
                        self.id , self.nm = (self.input_msg[6:].split(" ", 1) if " " in self.input_msg[6:] else [self.input_msg[6:], f"{CHANNEL_NAME}"])  
                        self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] Preparing ghost for {xMsGFixinG(self.id)}...\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        self.CliEnts2.send(OpEnSq(key , iv))
                        time.sleep(1)  
                        self.CliEnts2.send(cHSq(5 , self.id , key , iv))
                        time.sleep(1)  
                        start_time = time.time()
                        while time.time() - start_time < 5: 
                            if '0500' in self.DaTa2.hex()[0:4] and len(self.DaTa2.hex()) > 30:
                                self.dT = json.loads(DeCode_PackEt(self.DaTa2.hex()[10:]))
                                if "5" in self.dT and "data" in self.dT["5"] and "31" in self.dT["5"]["data"]:
                                    sq = self.dT["5"]["data"]["31"]["data"]
                                    print(f"Successfully got squad code: {sq}")
                                    self.CliEnts2.send(SEnd_InV(1 , self.id , key , iv))
                                    time.sleep(3)
                                    self.CliEnts2.send(ExiT('000000' , key , iv))
                                    time.sleep(1)
                                    for i in range(10):  
                                        self.CliEnts2.send(ghost_pakcet(self.id , self.nm , sq , key , iv))
                                        time.sleep(0.5)
                                    self.CliEnts.send(xSEndMsg(f'\n[b][c][90EE90]Ghost sent successfully!\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                    break
                            time.sleep(0.1)
                        else:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][FF0000]Failed to get squad info!\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        
                        self.CliEnts.close(); self.CliEnts2.close()
                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)

                    if '0500' in self.DaTa2.hex()[0:4] and len(self.DaTa2.hex()) > 30:
                        self.dT = json.loads(DeCode_PackEt(self.DaTa2.hex()[10:]))
                        self.dT = self.dT["5"]["data"]["1"]["data"] 
                        for i in range(5):
                            self.CliEnts2.send(maq(self.dT,key, iv))      		      	            			      	
                except Exception as e:
                    #self.CliEnts.close() ; self.CliEnts2.close()
                    print("g")
                    #self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                                    
    def GeT_Key_Iv(self , serialized_data):
        my_message = xKEys.MyMessage()
        my_message.ParseFromString(serialized_data)
        timestamp , key , iv = my_message.field21 , my_message.field22 , my_message.field23
        timestamp_obj = Timestamp()
        timestamp_obj.FromNanoseconds(timestamp)
        timestamp_seconds = timestamp_obj.seconds
        timestamp_nanos = timestamp_obj.nanos
        combined_timestamp = timestamp_seconds * 1_000_000_000 + timestamp_nanos
        return combined_timestamp , key , iv    

    def Guest_GeneRaTe(self , uid , password):
        self.url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        self.headers = {"Host": "100067.connect.garena.com","User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)","Content-Type": "application/x-www-form-urlencoded","Accept-Encoding": "gzip, deflate, br","Connection": "close",}
        self.dataa = {"uid": f"{uid}","password": f"{password}","response_type": "token","client_type": "2","client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3","client_id": "100067",}
        try:
            self.response = requests.post(self.url, headers=self.headers, data=self.dataa).json()
            self.Access_ToKen , self.Access_Uid = self.response['access_token'] , self.response['open_id']
            time.sleep(0.2)
            print(' - Starting C4  Freind BoT !')
            print(f' - Uid : {uid}\n - Password : {password}')
            print(f' - Access Token : {self.Access_ToKen}\n - Access Id : {self.Access_Uid}')
            return self.ToKen_GeneRaTe(self.Access_ToKen , self.Access_Uid)
        except Exception: ResTarT_BoT()    
                                        
    def GeT_LoGin_PorTs(self , JwT_ToKen , PayLoad,xR):
        self.UrL = f"{xR}/GetLoginData"
        print(JwT_ToKen)
        self.HeadErs = {
            'Expect': '100-continue',
            'Authorization': f'Bearer {JwT_ToKen}',
            'X-Unity-Version': '2018.4.11f1',
            'X-GA': 'v1 1',
            'ReleaseVersion': 'OB52',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)',
            'Host': 'loginbp.ggwhitehawk.com',
            'Connection': 'close',
            'Accept-Encoding': 'gzip, deflate, br',}       
        try:
                self.Res = requests.post(self.UrL , headers=self.HeadErs , data=PayLoad , verify=False)
                self.BesTo_data = json.loads(DeCode_PackEt(self.Res.content.hex()))  
                address , address2 = self.BesTo_data['32']['data'] , self.BesTo_data['14']['data'] 
                ip , ip2 = address[:len(address) - 6] , address2[:len(address) - 6]
                port , port2 = address[len(address) - 5:] , address2[len(address2) - 5:]             
                return ip , port , ip2 , port2          
        except requests.RequestException as e:
                print(f" - Bad Requests !")
        print(" - Failed To GeT PorTs !")
        return None, None   
        
    def ToKen_GeneRaTe(self , Access_ToKen , Access_Uid):
        self.UrL = "https://loginbp.ggblueshark.com/MajorLogin"
        self.HeadErs = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': 'OB52',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'Content-Length': '928',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
            'Host': 'loginbp.ggblueshark.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'}   
        self.dT = bytes.fromhex('1a13323032352d30322d32362031373a32343a3238220966726565206669726528013a07312e3130392e324232416e64726f6964204f532039202f204150492d3238202850492f72656c2e636a772e32303232303531382e313134313333294a0848616e6468656c645210566572697a6f6e20576972656c6573735a045749464960800a68c00772033234307a2d7838362d3634205353453320535345342e3120535345342e32204156582041565832207c2032343030207c20348001bf2e8a010f416472656e6f2028544d292036343092010d4f70656e474c20455320332e309a012b476f6f676c657c30666330653434362d636132372d346661612d383234612d643430643737373637646539a2010d32302e3137312e37332e323032aa0102766eb201206f70656e5f69645f7a6279ba010134c2010848616e6468656c64ca010c676f6f676c65204730313141ea01406163636573735f7a62f00101ca0210566572697a6f6e20576972656c657373d2020457494649ca03203161633462383065636630343738613434323033626638666163363132306635e003c68102e803d3e801f003af13f80392078004c8f3018804c681029004c8f3019804c68102b00404c80402d2043d2f646174612f6170702f636f6d2e6474732e667265656669726574682d673865444530543236384674466d6e465a3255706d413d3d2f6c69622f61726de00401ea045f35623839326161616264363838653537316636383830353331313861313632627c2f646174612f6170702f636f6d2e6474732e667265656669726574682d673865444530543236384674466d6e465a3255706d413d3d2f626173652e61706bf00406f804018a050233329a050a32303139313138313035b205094f70656e474c455332b805ff01c00504ca05224a034644040d5f5548030b165f03445e4a3e0f5754005c3d0a515f3b000d3b5a0561d2050750686f656e6978da0502415ae005e64fea05093372645f7061727479f2055c4b717348543767744b576b4b3067592f48776d647758496853697a3466516c645833596a5a654b383658425474684b41663162573456737a364469305338767172304a6334485833544d51384b6155553347655676597a574639493df805e7e4068806019006019a060134a2060134')
        self.dT = self.dT.replace(b'2025-02-26 17:24:28' , str(datetime.now())[:-7].encode())
        self.dT = self.dT.replace(b'1.109.2' , '1.120.1'.encode())
        self.dT = self.dT.replace(b'2019118105' , '2019118695'.encode())
        self.dT = self.dT.replace(b'access_zb' , Access_ToKen.encode())
        self.dT = self.dT.replace(b'open_id_zby' , Access_Uid.encode())
        self.PaYload = bytes.fromhex(EnC_AEs(self.dT.hex()))  
        self.ResPonse = requests.post(self.UrL, headers = self.HeadErs ,  data = self.PaYload , verify=False)    
     #   print(self.ResPonse)
        if self.ResPonse.status_code == 200 and len(self.ResPonse.text) > 10:
            self.BesTo_data = json.loads(DeCode_PackEt(self.ResPonse.content.hex()))
            self.JwT_ToKen = self.BesTo_data['8']['data']    
            self.xR = self.BesTo_data['10']['data']       
           # print(self.BesTo_data)
            self.combined_timestamp , self.key , self.iv = self.GeT_Key_Iv(self.ResPonse.content)
            ip , port , ip2 , port2 = self.GeT_LoGin_PorTs(self.JwT_ToKen , self.PaYload,self.xR)            
            return self.JwT_ToKen , self.key , self.iv, self.combined_timestamp , ip , port , ip2 , port2
        else:
            sys.exit()  
      
    def Get_FiNal_ToKen_0115(self):
        token , key , iv , Timestamp , ip , port , ip2 , port2 = self.Guest_GeneRaTe(self.id , self.password)
        self.JwT_ToKen = token        
        try:
            self.AfTer_DeC_JwT = jwt.decode(token, options={"verify_signature": False})
            self.AccounT_Uid = self.AfTer_DeC_JwT.get('account_id')
            self.EncoDed_AccounT = hex(self.AccounT_Uid)[2:]
            self.HeX_VaLue = DecodE_HeX(Timestamp)
            self.TimE_HEx = self.HeX_VaLue
            self.JwT_ToKen_ = token.encode().hex()
            print(f' - ProxCed Uid : {self.AccounT_Uid}')
        except Exception as e:
            print(f" - Error In ToKen : {e}")
            return
        try:
            self.Header = hex(len(EnC_PacKeT(self.JwT_ToKen_, key, iv)) // 2)[2:]
            length = len(self.EncoDed_AccounT)
            self.__ = '00000000'
            if length == 9: self.__ = '0000000'
            elif length == 8: self.__ = '00000000  '
            elif length == 10: self.__ = '000000'
            elif length == 7: self.__ = '000000000'
            else:
                print('Unexpected length encountered')                
            self.Header = f'0115{self.__}{self.EncoDed_AccounT}{self.TimE_HEx}00000{self.Header}'
            self.FiNal_ToKen_0115 = self.Header + EnC_PacKeT(self.JwT_ToKen_ , key , iv)
        except Exception as e:
            print(f" - Erorr In Final Token : {e}")
        self.AutH_ToKen = self.FiNal_ToKen_0115
        self.Connect_SerVer(self.JwT_ToKen , self.AutH_ToKen , ip , port , key , iv , ip2 , port2)        
        return self.AutH_ToKen , key , iv

def StarT_SerVer():
    FF_CLient('uid','pas')
StarT_SerVer()