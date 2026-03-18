import requests , os , psutil , sys , jwt , pickle , json , binascii , time , urllib3 , xKEys , base64 , datetime , re , socket , threading
from protobuf_decoder.protobuf_decoder import Parser
from xTnito import * 
from threading import Thread
from datetime import datetime , timedelta
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

owners_id=''
bot_name=''
tag=''

def auto():
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
    
def restart_program():
    print('\n - ResTartinG The BoT ... ! ')
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
        
ownerr = [f'{owners_id}']
owner = [EnC_Uid(uid , Tp = 'Uid') for uid in ownerr]

Thread(target=auto, daemon=True).start()    

class FF_CLient():

    def __init__(self, id, password):
        self.id = id
        self.password = password
        self.Get_FiNal_ToKen_0115()

    def Connect_SerVer_OnLine(self , Token , tok , host , port , key , iv , host2 , port2):
            global CLients2 , data2 , AutH
            try:
                self.AutH_ToKen_0115 = tok    
                self.CLients2 = socket.create_connection((host2 , int(port2)))
                self.CLients2.send(bytes.fromhex(self.AutH_ToKen_0115))                  
            except:pass        
            while True:
                try:
                    self.data2 = self.CLients2.recv(99999)
                    if '0500' in self.data2.hex()[0:4] and len(self.data2.hex()) > 30:	         	    	    
                            self.packet = json.loads(DeCode_PackEt(f'08{self.data2.hex().split("08", 1)[1]}'))
                            self.AutH = self.packet['5']['data']['7']['data']
                            #print(self.AutH)    		      	
                except:pass    	
                               
    def Connect_SerVer(self , Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code): 
        self.CLients = socket.create_connection((host , int(port)))
        self.CLients.send(bytes.fromhex(tok))                  
        data = self.CLients.recv(1024)       
        self.CLients.send(AuthClan(Guild_Uid , Auth_Code , key , iv))
        threading.Thread(target=self.Connect_SerVer_OnLine, args=(Token , tok , host , port , key , iv , host2 , port2)).start()
        self.Exemple = xMsGFixinG('12345678')
        while True:
            try:
                data = self.CLients.recv(1024)        	
                if len(data) == 0:
                    try:            		    
                        self.CLients.close() ; self.CLients2.close()
                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                    except:
                        try:
                            self.CLients.close() ; self.CLients2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)          
                        except:
                            self.CLients.close() ; self.CLients2.close()
                            restart_program()

                if '1200' in data.hex()[0:4] and 900 > len(data.hex()) > 100:
                    if b"***" in data:data = data.replace(b"***",b"106")
                    self.BesTo_data = json.loads(DeCode_PackEt(data.hex()[10:]))                        
                    try:            	       
                       self.InputMsg = 'besto_love' if '8' in self.BesTo_data["5"]["data"] else self.BesTo_data["5"]["data"]["4"]["data"] 
                       self.name = self.BesTo_data["5"]["data"]["9"]["data"]["1"]["data"]
                       
                    except:self.InputMsg = "None"   
                    self.DeCode_CliEnt_Uid = self.BesTo_data["5"]["data"]["1"]["data"]
                    client_id = EnC_Uid(self.DeCode_CliEnt_Uid , Tp = 'Uid')
                    
                if 'besto_love' in self.InputMsg[:10]:
                    if client_id not in black or client_id in owner and client_id not in black or client_id in approve:           	        
                        self.CLients.send(xSEndMsg(f'''\n[b][c][FFD3EF] > WeLcome To {bot_name} BoT <\n\n[ffffff] To GeT CommandE LisT\n\n Just Send /start Or /help !\n\n For AraBic Menu => ar\n\n Enjoy UsinG ThE BoT WiTh New FeTures And BesT SpEed\n\n[FFD3EF] PowerEd By : {bot_name} !\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        time.sleep(0.3)            		
                        self.CLients.close() ; self.CLients2.close()
                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)    		
                            
                if b'/baybi' in data or b'/help' in data or 'ar' in self.InputMsg[:2]:
                    if client_id not in black or client_id in owner and client_id not in black or client_id in approve:           	
                        self.CLients.send(xSEndMsg(f'''	[b][c][FFD700]مرحبا بك في البوت ايها المستخدم
    
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
    [ffffff]لإرسال سبام الروم الى لاعب[90EE90]
    /sp/id
    [ffffff]لجلب معلومات بروفايل اللاعب[90EE90]
    ++ id
    /code tmcd
    /em1/uid1 uid2 emote_id
    /ou/id ghost_name
    [ffffff] {bot_name}\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        time.sleep(0.5)
                        self.CLients.close() ; self.CLients2.close()
                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)	

                elif '/like' in self.InputMsg[:5]: 	 
                    id = self.InputMsg[6:] 
                    self.Zx = ChEck_Commande(id)          
                    if client_id not in black and True == self.Zx or client_id in owner and client_id not in black and True == self.Zx or client_id in approve:      
                            self.CLients.send(xSEndMsg(f'''\n[b][c][FFD3EF] User : {xMsGFixinG(self.name)}\n\n[b][c][{ArA_CoLor()}] SendinG LiKes To {xMsGFixinG(id)}\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))   
                            a1 , a2 , a3 , a4 , a5 = Likes(id)
                            if a3 == a4:
                                self.CLients.send(xSEndMsg(f'''\n[b][c][FFD3EF] User : {xMsGFixinG(self.name)}\n\n[b][c][{ArA_CoLor()}] Try LiKes AfTer 24H\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.5)
                                self.CLients.close() ; self.CLients2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)	
                            else:
                                self.CLients.send(xSEndMsg(f'''[b][c][90EE90]\n [SuccEssFuLLy] - SEnd LiKes !
        [ffffff]	
          PLayer Name : {a1}
          PLayer Uid : {xMsGFixinG(id)}
          PLayer Level : {xMsGFixinG(a2)}
          LiKes BeFore : {xMsGFixinG(a3)}
          LiKes AFter : {xMsGFixinG(a4)}
          LiKes GiVen : {xMsGFixinG(a5)}
          
           [90EE90]Dev : {bot_name}\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(1)
                                self.CLients.close() ; self.CLients2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)  
                                                      
                                                             
                elif '/spam' in self.InputMsg[:5]:             		
                    id = self.InputMsg[6:]
                    self.Zx = ChEck_Commande(id)    	
                    if client_id not in black or client_id in owner and client_id not in black or client_id in approve and True == self.Zx: 	      
                            self.CLients.send(xSEndMsg(f'''\n[b][c][FFD3EF] User : {xMsGFixinG(self.name)}\n\n[b][c][{ArA_CoLor()}] SendinG Spam To {xMsGFixinG(id)}\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            Req = Requests_SPam(id)
                            if True == Req:
                                self.CLients.send(xSEndMsg(f'''\n[b][c][FFD3EF] User : {xMsGFixinG(self.name)}\n\n[b][c][90EE90]SuccEssFuLLy SendinG SPam\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.5)
                                self.CLients.close() ; self.CLients2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                            elif False == Req:
                                self.CLients.send(xSEndMsg(f'''\n\n[b][c][FFD3EF] User : {xMsGFixinG(self.name)}\n[b][c][FFD700]FaiLEd SendinG SPam\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.5)
                                self.CLients.close() ; self.CLients2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                                                                           
                elif '++' in self.InputMsg[:2]:   
                    id = self.InputMsg[3:]
                    self.Zx = ChEck_Commande(id) 
                    if client_id not in black or client_id in owner and client_id not in black or client_id in approve and True == self.Zx:
                            self.CLients.send(xSEndMsg(f'''\n[b][c][FFD3EF] User : {xMsGFixinG(self.name)}\n\n[{ArA_CoLor()}] GeTinG InFo FoR {xMsGFixinG(id)}\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.5)
                            self.CLients.send(xSEndMsg(GeT_PLayer_InFo(id , Token) , 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.5)
                            self.CLients.close() ; self.CLients2.close() 
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)	   	   
                          
                elif '/5' in self.InputMsg[:2]:            	    
                    if client_id not in black or client_id in owner and client_id not in black or client_id in approve:           	  
                            self.CLients.send(xSEndMsg(f'''\n[b][c][FFD3EF] User : {xMsGFixinG(self.name)}\n\n[b][c][90EE90]GeneRaTinG 5 in SQuid\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(OpEnSq(key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(cHSq(5 , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(SEnd_InV(2 , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(3)		            	    
                            self.CLients.close() ; self.CLients2.close()  
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)		   
                
                elif '/6' in self.InputMsg[:2]:
                    if client_id not in black or client_id in owner and client_id not in black or client_id in approve:       	  
                            self.CLients.send(xSEndMsg(f'''\n[b][c][FFD3EF] User : {xMsGFixinG(self.name)}\n\n[b][c][{ArA_CoLor()}]GeneRaTinG 6 in SQuid\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(OpEnSq(key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(cHSq(6 , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(SEnd_InV(2 , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(4)		            	    
                            self.CLients.close() ; self.CLients2.close()  
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code) 	 

                elif '/3' in self.InputMsg[:2]:            	    
                    if client_id not in black or client_id in owner and client_id not in black or client_id in approve:           	  
                            self.CLients.send(xSEndMsg(f'''\n[b][c][FFD3EF] User : {xMsGFixinG(self.name)}\n\n[b][c][{ArA_CoLor()}]GeneRaTinG 3 in SQuid\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(OpEnSq(key,iv))
                            time.sleep(0.3)
                            self.CLients2.send(cHSq(3 , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(SEnd_InV(2 , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(3)		            	    
                            self.CLients.close() ; self.CLients2.close()  
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)     		
                                                    
                elif '/c5/' in self.InputMsg[:4]: 
                    id = self.InputMsg[4:]            	          
                    self.Zx = ChEck_Commande(id) 
                    if client_id not in black or client_id in owner and client_id not in black or client_id in approve and True == self.Zx:               	  
                            self.CLients.send(xSEndMsg(f'''\n[b][c][FFD3EF] User : {xMsGFixinG(self.name)}\n\n[b][c][{ArA_CoLor()}] 5 in SQuid To {xMsGFixinG(id)}\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(OpEnSq(key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(cHSq(5 , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(SEnd_InV(2 , id , key , iv))
                            time.sleep(4)		            	    
                            self.CLients.close() ; self.CLients2.close()  
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code) 
               
                elif '/c6/' in self.InputMsg[:4]:
                    id = self.InputMsg[4:]            	
                    self.Zx = ChEck_Commande(id) 
                    if client_id not in black or client_id in owner and client_id not in black or client_id in approve and True == self.Zx:               	  
                            self.CLients.send(xSEndMsg(f'''\n[b][c][FFD3EF] User : {xMsGFixinG(self.name)}\n\n[b][c][{ArA_CoLor()}] 6 in SQuid To {xMsGFixinG(id)}\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(OpEnSq(key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(cHSq(6 , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(SEnd_InV(2 , id , key , iv))
                            time.sleep(4)	            	    
                            self.CLients.close() ; self.CLients2.close()  
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code) 	
                            
                elif '/c3/' in self.InputMsg[:4]:
                    id = self.InputMsg[4:]            	
                    self.Zx = ChEck_Commande(id) 
                    if client_id not in black or client_id in owner and client_id not in black or client_id in approve and True == self.Zx:               	  
                            self.CLients.send(xSEndMsg(f'''\n[b][c][FFD3EF] User : {xMsGFixinG(self.name)}\n\n[b][c][{ArA_CoLor()}] 3 in SQuid To {xMsGFixinG(id)}\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(OpEnSq(key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(cHSq(3 , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(SEnd_InV(2 , id , key , iv))
                            time.sleep(4)	            	    
                            self.CLients.close() ; self.CLients2.close()  
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)            
                            
                elif '/get/' in self.InputMsg[:5]:
                    id = self.InputMsg[5:]            	
                    self.Zx = ChEck_Commande(id) 
                    if client_id not in black or client_id in owner and client_id not in black or client_id in approve and True == self.Zx:      	  
                            self.CLients.send(xSEndMsg(f'''\n[b][c][FFD3EF] User : {xMsGFixinG(self.name)}\n\n[b][c][{ArA_CoLor()}] GeTinG PLayer {xMsGFixinG(id)}\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(OpEnSq(key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(cHSq(5 , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CLients2.send(SEnd_InV(1 , id , key , iv))
                            time.sleep(0.1)
                            self.CLients2.send(SEnd_InV(1 , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(4)	            	    
                            self.CLients.close() ; self.CLients2.close()  
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code) 	    

                if '/pp/' in self.InputMsg[:4]:
                        self.id = self.InputMsg[4:]	 
                        self.Zx = ChEck_Commande(self.id)
                        if client_id not in black or client_id in owner and client_id not in black or client_id in approve and True == self.Zx:
                            self.CLients.send(xSEndMsg(f'''\n[b][c][FFD3EF] User : {xMsGFixinG(self.name)}\n\n[b][c][{ArA_CoLor()}] SenDinG Spam To {xMsGFixinG(self.id)}\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv)) 
                            time.sleep(0.1)         	 
                            for i in range(99):      
                                threading.Thread(target=lambda: self.CLients2.send(SPamSq(self.id , key , iv))).start()	        
                                time.sleep(0.1)	
                            time.sleep(0.1) 
                            self.CLients.send(xSEndMsg(f'''\n[b][c][FFD3EF] User : {xMsGFixinG(self.name)}\n\n[b][c][90EE90]SuccEss SendinG SPam\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CLients.close() ; self.CLients2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)  	  
                                                
                elif '/sp/' in self.InputMsg[:4]:
                        self.id , self.nm = (self.InputMsg[4:].split(" ", 1) if " " in self.InputMsg[4:] else [self.InputMsg[4:], "C4 - Team"])
                        self.Zx = ChEck_Commande(self.id)	    
                        if client_id not in black or client_id in owner and client_id not in black or client_id in approve and True == self.Zx:
                            self.CLients.send(xSEndMsg(f'''\n[b][c][FFD3EF] User : {xMsGFixinG(self.name)}\n\n[b][c][{ArA_CoLor()}] Spam Room To {xMsGFixinG(self.id)}\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            try:	      		    
                                self.CLients2.send(GeT_Status(self.id , key , iv))
                                time.sleep(0.3)
                            except:pass    	            	
                            if '0f00' in self.data2.hex()[:4]:
                                try:	            		
                                    packet = self.data2.hex()[10:]
                                    self.BesTo_data = json.loads(DeCode_PackEt(packet))
                                    self.room_uid = self.BesTo_data['5']['data']['1']['data']['15']['data']
                                    for i in range(999):
                                        threading.Thread(target=lambda: self.CLients2.send(SPam_Room(self.id , self.room_uid, self.nm, key, iv))).start()
                                    time.sleep(0.1)	
                                    self.CLients.send(xSEndMsg(f'''\n[b][c][FFD3EF] User : {xMsGFixinG(self.name)}\n\n[b][c][90EE90]SuccEss SEndinG SPam Room\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                    time.sleep(0.1)			    	
                                    self.CLients.close() ; self.CLients2.close()
                                    self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)           	        
                                except:pass    
                elif '/em1/' in self.InputMsg[:5]:
                    parts = self.InputMsg[5:].strip().split()
                    if len(parts) < 2:
                        self.CLients.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - Use: /em1/ <uid1> <uid2> <uid3> <uid4> <uid5> <emote_id>\n - Ex: /em1/ 123456789 987654321 555555555 909000012\n', 1, Guild_Uid, self.DeCode_CliEnt_Uid, key, iv))
                        time.sleep(0.3)
                        self.CLients.close(); self.CLients2.close()
                        self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2, Guild_Uid, Auth_Code)
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
                        self.CLients.send(xSEndMsg(f'\n[b][c][FF0000]Error: Invalid format!\nUse: /em1/ <uid1> <uid2> <uid3> <emote_id>\nExample: /em1/ 123456789 987654321 909000012\n', 1, Guild_Uid, self.DeCode_CliEnt_Uid, key, iv))
                        time.sleep(0.3)
                        self.CLients.close(); self.CLients2.close()
                        self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2, Guild_Uid, Auth_Code)
                        continue
                    
                    all_uids = []
                    if uid1: all_uids.append(str(uid1))
                    if uid2: all_uids.append(str(uid2))
                    if uid3: all_uids.append(str(uid3))
                    if uid4: all_uids.append(str(uid4))
                    if uid5: all_uids.append(str(uid5))
                    
                    if client_id not in black or client_id in owner and client_id not in black or client_id in approve:
                        uid_display = ", ".join([xMsGFixinG(uid) for uid in all_uids])
                        message = f'\n[b][c][{ArA_CoLor()}] Sending emote {emote_id} to {len(all_uids)} players: {uid_display}\n'
                        self.CLients.send(xSEndMsg(message, 1, Guild_Uid, self.DeCode_CliEnt_Uid, key, iv))
                        success_count = 0
                        
                        for player_uid in all_uids:
                            try:
                                self.CLients2.send(EmoTe(int(player_uid), int(emote_id), key, iv))
                                success_count += 1
                                time.sleep(0.1)  
                            except Exception as e:
                                error_msg = f'\n[b][c][FF0000]Error sending to {xMsGFixinG(player_uid)}\n'
                                self.CLients.send(xSEndMsg(error_msg, 1, Guild_Uid, self.DeCode_CliEnt_Uid, key, iv))
                        
                        if success_count > 0:
                            success_msg = f'\n[b][c][90EE90]Successfully sent emote {emote_id} to {success_count}/{len(all_uids)} players!\n'
                            self.CLients.send(xSEndMsg(success_msg, 1, Guild_Uid, self.DeCode_CliEnt_Uid, key, iv))
                        
                        time.sleep(0.3)
                        self.CLients.close(); self.CLients2.close()
                        self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2, Guild_Uid, Auth_Code)
                elif '/code' in self.InputMsg[:5]:
                    parts = self.InputMsg[6:].strip().split()
                    if len(parts) < 1:
                        self.CLients.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - Use: /code <tmcd>\n - Ex: /code 517284\n', 1, Guild_Uid, self.DeCode_CliEnt_Uid, key, iv))
                        time.sleep(0.3)
                        self.CLients.close(); self.CLients2.close()
                        self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2, Guild_Uid, Auth_Code)
                        continue
                    
                    tmcd = parts[0]
                    ghost_name = parts[1] if len(parts) > 1 else "@VeNoMi"
                    
                    if client_id not in black or client_id in owner and client_id not in black or client_id in approve:
                        self.CLients.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] SeNding Ghosts For this team code  {tmcd}\n', 1, Guild_Uid, self.DeCode_CliEnt_Uid, key, iv))
                        self.CLients2.send(GenJoinSquadsPacket(tmcd, key, iv))
                        time.sleep(0.3)
                        
                        if '0500' in self.data2.hex()[0:4] and len(self.data2.hex()) > 30:
                            self.dT = json.loads(DeCode_PackEt(self.data2.hex()[10:]))
                            sq = self.dT["5"]["data"]["31"]["data"]
                            idT = self.dT["5"]["data"]["1"]["data"]
                            self.CLients2.send(ExiT('000000', key, iv))
                            
                            for i in range(1000):
                                self.CLients2.send(GenJoinSquadsPacket(tmcd, key, iv))
                                time.sleep(0.001)
                                self.CLients2.send(ExiT('000000', key, iv))
                                self.CLients2.send(ghost_pakcet(idT, ghost_name, sq, key, iv))
                                
                        time.sleep(0.1)
                        self.CLients.close(); self.CLients2.close()
                        self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2, Guild_Uid, Auth_Code)

                elif '/ou/' in self.InputMsg[:4]:
                    id_part = self.InputMsg[4:]
                    parts = id_part.split(" ", 1)
                    target_id = parts[0] 
                    ghost_name = parts[1] if len(parts) > 1 else "@VeNoM"
                    
                    if client_id not in black or client_id in owner and client_id not in black or client_id in approve:
                        try:
                            self.CLients.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] جاري إرسال طلب انضمام إلى سكواد اللاعب {xMsGFixinG(target_id)}\n', 1, Guild_Uid, self.DeCode_CliEnt_Uid, key, iv))
                            self.CLients2.send(SPamSq(target_id, key, iv))
                            time.sleep(2)
                            self.CLients.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] في انتظار قبول الطلب...\n', 1, Guild_Uid, self.DeCode_CliEnt_Uid, key, iv))
                            self.CLients2.send(AccEpT(target_id, self.AutH, key, iv))
                            time.sleep(2)
                            
                            start_time = time.time()
                            while time.time() - start_time < 10:  
                                if '0500' in self.data2.hex()[0:4] and len(self.data2.hex()) > 30:
                                    packet = self.data2.hex()[10:]
                                    self.BesTo_data = json.loads(DeCode_PackEt(packet))
                                    sq_code = self.BesTo_data["5"]["data"]["31"]["data"]
                                    sq_leader = self.BesTo_data["5"]["data"]["1"]["data"]
                                    self.CLients2.send(ExiT('000000', key, iv))
                                    time.sleep(1)
                                    self.CLients.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] جاري إرسال الشبح "{ghost_name}" إلى السكواد {xMsGFixinG(sq_code)}\n', 1, Guild_Uid, self.DeCode_CliEnt_Uid, key, iv))
                                    self.CLients2.send(ghost_pakcet(sq_leader, ghost_name, sq_code, key, iv))
                                    time.sleep(0.01)
                                    self.CLients2.send(ExiT('000000', key, iv))
                                    time.sleep(0.01)
                                    self.CLients.send(xSEndMsg(f'\n[b][c][90EE90]تم إرسال الشبح "{ghost_name}" بنجاح!\n', 1, Guild_Uid, self.DeCode_CliEnt_Uid, key, iv))
                                    break
                                time.sleep(0.1)
                            else:
                                self.CLients.send(xSEndMsg(f'\n[b][c][FF0000]لم يتم قبول الطلب خلال الوقت المحدد\n', 1, Guild_Uid, self.DeCode_CliEnt_Uid, key, iv))
                                
                        except Exception as e:
                            self.CLients.send(xSEndMsg(f'\n[b][c][FF0000]حدث خطأ: {str(e)}\n', 1, Guild_Uid, self.DeCode_CliEnt_Uid, key, iv))
                        
                        time.sleep(0.3)
                        self.CLients.close(); self.CLients2.close()
                        self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2, Guild_Uid, Auth_Code)

                elif '/all' in self.InputMsg[:4]:
                        msg = self.InputMsg[5:]
                        if client_id in owner:
                            for i in range(60):
                                self.CLients.send(xSEndMsg(f'[b][c][{ArA_CoLor()}]{msg}', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.5)
                            time.sleep(0.2)
                            self.CLients.close() ; self.CLients2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                        else:          		    		
                                self.CLients.send(xSEndMsg(f'[b][c]\nالقائد يمكن له استعمال الميزة فقط !\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.1)
                                self.CLients.close() ; self.CLients2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                                
                elif '/owner' in self.InputMsg[:6]:
                    if client_id in owner:
                        self.CLients.send(xSEndMsg(f'''[b][c]
     [ffffff]   مرحبا أيها القائد\n\n => {self.name} <=

     [FFD700]  أولا لدينا أوامر البلاك ليست :
                             
     [90EE90]اضافة أيدي إلى البلاك ليست\n\n[ffffff]=> /add id	 
          
     [90EE90]حدف أيدي من البلاك ليست\n\n[ffffff]=> /delete id	 
     
     [90EE90]إضهار الأيديات الموجودة بالقائمة\n\n[ffffff]=> /show
     
     [90EE90]حدف جميع الأيديات بالقائمة\n\n[ffffff]=> /clear\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        time.sleep(0.5)
                        self.CLients.send(xSEndMsg(f'''[b][c]
     [FFD700]  تانيا لدينا أوامر قبول عضو لإستخدام البوت رغم انه لم يضع الشعار :
                             
     [90EE90]قبول مستخدم لإستخدام البوت\n\n[ffffff]=> /approve id	 
          
     [90EE90]ايقاف مستخدم من دون شعار\n\n[ffffff]=> /deapprove id	 
     
     [90EE90]إضهار الأيديات الموجودة بالقائمة\n\n[ffffff]=> /list
     
     [90EE90]حدف جميع الأيديات بالقائمة\n\n[ffffff]=> /clr/approvs\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        time.sleep(0.5)
                        self.CLients.send(xSEndMsg(f'''[b][c]
     [FFD700]  تالتا لدينا امرين تانويين فقط :
                             
     [90EE90]تكرار رسالتك من اجل إعلان ما\n\n[ffffff]=> /all msg	 
          
     [90EE90]إيقاف تشغيل البوت مدة معينة \n\n[ffffff]=> /shotdown (1h/1min/etc...)	 
     
    [FFD700]  DeVLoper : {bot_name}\n''', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))		
                        time.sleep(0.3)
                        self.CLients.close() ; self.CLients2.close()
                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                    else:          		    		
                        self.CLients.send(xSEndMsg(f'[b][c]\nالقائد يمكن له استعمال الميزة فقط !\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        time.sleep(0.1)
                        self.CLients.close() ; self.CLients2.close()
                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)            		    		
                                
                elif '/add' in self.InputMsg[:4]:
                        id = self.InputMsg[5:]
                        Req = Add_Black(id)
                        if client_id in owner and True == Req:
                            self.CLients.send(xSEndMsg(f'\n[b][c][90EE90] [SuccEssFuLLy] AddinG !\n\n[{ArA_CoLor()}] Uid : {xMsGFixinG(id)}\n\n To BLack Liste !\n\n[ffffff] By Owner : {self.name}\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CLients.close() ; self.CLients2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                            
                        if client_id in owner and False == Req:
                            self.CLients.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] [Error] AddinG !\n\n Uid : {xMsGFixinG(id)}\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CLients.close() ; self.CLients2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                                                        
                        elif client_id not in owner:
                                
                                self.CLients.send(xSEndMsg(f'[b][c]\nالقائد يمكن له استعمال الميزة فقط !\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.1)
                                self.CLients.close() ; self.CLients2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                                                              
                elif '/delete' in self.InputMsg[:7]:
                        id = self.InputMsg[8:]            	
                        Req = Rem_Black(id)            	
                        if client_id in owner and True == Req:
                            self.CLients.send(xSEndMsg(f'\n[b][c][90EE90][SuccEssFuLLy] RemovinG !\n\n[{ArA_CoLor()}] Uid : {xMsGFixinG(id)}\n\n From BLack Liste !\n\n [ffffff] By Owner : {self.name}\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CLients.close() ; self.CLients2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                            
                        if client_id in owner and False == Req:
                            self.CLients.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] Uid : {xMsGFixinG(id)} NoT Found !\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CLients.close() ; self.CLients2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code) 
                                    
                        elif client_id not in owner:
                                
                                self.CLients.send(xSEndMsg(f'[b][c]\nالقائد يمكن له استعمال الميزة فقط !\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.1)
                                self.CLients.close() ; self.CLients2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                                                              
                elif '/show' in self.InputMsg[:5]:           	
                        Req = Show_Uids()            	
                        if client_id in owner and Req:
                            self.CLients.send(xSEndMsg(f'\n[b][c] Uids In BLack LisTe :\n\n{xMsGFixinG(Req)}\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CLients.close() ; self.CLients2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                            
                        if client_id in owner and False == Req:
                            self.CLients.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] Uids In BLack Liste NoT Found !\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)   
                            self.CLients.close() ; self.CLients2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)         
                                    
                        elif client_id not in owner:
                                self.CLients.send(xSEndMsg(f'[b][c]\nالقائد يمكن له استعمال الميزة فقط !\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.1)
                                self.CLients.close() ; self.CLients2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                                
                elif '/clear' in self.InputMsg[:6]:           	
                        Req = Clear()            	
                        if client_id in owner and True == Req:
                            self.CLients.send(xSEndMsg(f'\n[b][c][90EE90][SuccEssFuLLy] - CLearinG !\n\n[{ArA_CoLor()}] BLack LisTe !\n\n [ffffff]By Owner : {self.name}\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CLients.close() ; self.CLients2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                            
                        if client_id in owner and False == Req:
                            self.CLients.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] Uids In BLack Liste NoT Found !\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CLients.close() ; self.CLients2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)          	    
                        elif client_id not in owner:         		
                                self.CLients.send(xSEndMsg(f'[b][c]\nالقائد يمكن له استعمال الميزة فقط !\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.1)
                                self.CLients.close() ; self.CLients2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)

                elif '/approve' in self.InputMsg[:8]:
                        id = self.InputMsg[9:]
                        Req = Approved(id)
                        if client_id in owner and True == Req:
                            self.CLients.send(xSEndMsg(f'\n[b][c][90EE90] [SuccEssFuLLy] AddinG !\n\n[{ArA_CoLor()}] Uid : {xMsGFixinG(id)}\n\n To ApproVEd UsErs !\n\n[ffffff] By Owner : {self.name}\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CLients.close() ; self.CLients2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                            
                        if client_id in owner and False == Req:
                            self.CLients.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] [Error] AddinG !\n\n Uid : {xMsGFixinG(id)}\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CLients.close() ; self.CLients2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                                                        
                        elif client_id not in owner:
                                self.CLients.send(xSEndMsg(f'[b][c]\nالقائد يمكن له استعمال الميزة فقط !\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.1)
                                self.CLients.close() ; self.CLients2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)     
                                
                elif '/deapprove' in self.InputMsg[:10]:
                        id = self.InputMsg[11:]            	
                        Req = DeApproved(id)            	
                        if client_id in owner and True == Req:
                            self.CLients.send(xSEndMsg(f'\n[b][c][90EE90][SuccEssFuLLy] RemovinG !\n\n[{ArA_CoLor()}] Uid : {xMsGFixinG(id)}\n\n From ApproVEd Liste !\n\n [ffffff] By Owner : {self.name}\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CLients.close() ; self.CLients2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                            
                        if client_id in owner and False == Req:
                            self.CLients.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] Uid : {xMsGFixinG(id)} NoT Found !\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CLients.close() ; self.CLients2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code) 
                                    
                        elif client_id not in owner:   		
                                self.CLients.send(xSEndMsg(f'[b][c]\nالقائد يمكن له استعمال الميزة فقط !\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.1)
                                self.CLients.close() ; self.CLients2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)

                elif '/list' in self.InputMsg[:5]:           	
                        Req = Show_Approvs()            	
                        if client_id in owner and Req:
                            self.CLients.send(xSEndMsg(f'\n[b][c] Uids In ApproVEd LisT :\n\n{xMsGFixinG(Req)}\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            
                        if client_id in owner and False == Req:
                            self.CLients.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] Uids In ApproVEd Liste NoT Found !\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CLients.close() ; self.CLients2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)         
                                    
                        elif client_id not in owner:
                                self.CLients.send(xSEndMsg(f'[b][c]\nالقائد يمكن له استعمال الميزة فقط !\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.1)
                                self.CLients.close() ; self.CLients2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)

                elif '/clr/approvs' in self.InputMsg[:12]:           	
                        Req = Clear_Approvs()            	
                        if client_id in owner and True == Req:
                            self.CLients.send(xSEndMsg(f'\n[b][c][90EE90][SuccEssFuLLy] - CLearinG !\n\n[{ArA_CoLor()}] ApproVEd LisT !\n\n [ffffff]By Owner : {self.name}\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CLients.close() ; self.CLients2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                            
                        if client_id in owner and False == Req:
                            self.CLients.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] Uids In ApproVEd Liste NoT Found !\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CLients.close() ; self.CLients2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)          	    
                        elif client_id not in owner:         		
                                self.CLients.send(xSEndMsg(f'[b][c]\nالقائد يمكن له استعمال الميزة فقط !\n', 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.1)
                                self.CLients.close() ; self.CLients2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                                                              
                elif '/shotdown' in self.InputMsg[:9]:
                        self.time = self.InputMsg[10:]
                        if 'h' in self.time:
                                hours = int(self.time.replace('h', ''))
                                sleep_time = timedelta(hours=hours)
                        elif 'min' in self.time:
                            minutes = int(self.time.replace('min', ''))
                            sleep_time = timedelta(minutes=minutes)
                        else:
                            print("Invalid time format.")
                        end_time = datetime.now() + sleep_time
                        end_time = end_time.strftime('%d/%m/%y - %I:%M%p')
                        self.CLients.send(xSEndMsg(f"\n[b][c][90EE90][SuccEssFuLLy] ShoT Down ! \n\n[{ArA_CoLor()}] For : {self.time}\n\n ResTartinG At :\n\n  {xMsGFixinG(end_time)}\n\n[ffffff] By Owner : {self.name} ! \n", 1 , Guild_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        time.sleep(0.3)
                        self.CLients.close() , self.CLients2.close()    
                        time.sleep(sleep_time.total_seconds())
                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2 , Guild_Uid , Auth_Code)
                        time.sleep(0.3)
                        #restart_program()
                elif '0500' in self.DaTa2.hex()[0:4] and len(self.DaTa2.hex()) > 30:
                        self.dT = json.loads(DeCode_PackEt(self.DaTa2.hex()[10:]))
                        self.dT = self.dT["5"]["data"]["1"]["data"] 
                        self.CliEnts2.send(maq(self.dT, key, iv))   	       	
            except Exception as e:
                pass
                                 
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
            print('- Starting C4 CLan BoT ')
            return self.ToKen_GeneRaTe(self.Access_ToKen , self.Access_Uid)
        except Exception as e: print(e) ; restart_program()    
                                        
    def GeT_LoGin_PorTs(self , JwT_ToKen , PayLoad,xR):
        self.UrL = f"{xR}/GetLoginData"
        self.HeadErs = {
            'Expect': '100-continue',
            'Authorization': f'Bearer {JwT_ToKen}',
            'X-Unity-Version': '2018.4.11f1',
            'X-GA': 'v1 1',
            'ReleaseVersion': 'OB52',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)',
            'Host': 'clientbp.common.ggbluefox.com',
            'Connection': 'close',
            'Accept-Encoding': 'gzip, deflate, br',}       
        try:
                self.Res = requests.post(self.UrL , headers=self.HeadErs , data=PayLoad , verify=False)
                self.BesTo_data = json.loads(DeCode_PackEt(self.Res.content.hex()))  
                address , address2 = self.BesTo_data['32']['data'] , self.BesTo_data['14']['data'] 
                ip , ip2 = address[:len(address) - 6] , address2[:len(address) - 6]
                port , port2 = address[len(address) - 5:] , address2[len(address2) - 5:]
                try: self.Guild_Uid , self.Auth_Code = self.BesTo_data['20']['data'] , self.BesTo_data['55']['data'] 
                except: self.Guild_Uid , self.Auth_Code = None , None     
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
        self.dT = self.dT.replace(b'1.109.2' , '1.120.2'.encode())
        self.dT = self.dT.replace(b'2019118105' , '2019118105'.encode())
        self.dT = self.dT.replace(b'access_zb' , Access_ToKen.encode())
        self.dT = self.dT.replace(b'open_id_zby' , Access_Uid.encode())
        self.PaYload = bytes.fromhex(EnC_AEs(self.dT.hex()))  
        self.ResPonse = requests.post(self.UrL, headers = self.HeadErs ,  data = self.PaYload , verify=False)        
        if self.ResPonse.status_code == 200 and len(self.ResPonse.text) > 10:
            self.BesTo_data = json.loads(DeCode_PackEt(self.ResPonse.content.hex()))
            self.JwT_ToKen = self.BesTo_data['8']['data']           
            self.combined_timestamp , self.key , self.iv = self.GeT_Key_Iv(self.ResPonse.content)
            ip , port , ip2 , port2 = self.GeT_LoGin_PorTs(self.JwT_ToKen , self.PaYload)            
            return self.JwT_ToKen , self.key , self.iv, self.combined_timestamp , ip , port , ip2 , port2
        else:
            sys.exit()
      
    def Get_FiNal_ToKen_0115(self):
        token , key , iv , Timestamp , ip , port , ip2 , port2 = self.Guest_GeneRaTe(self.id, self.password)
        self.JwT_ToKen = token              
        try:
            self.AfTer_DeC_JwT = jwt.decode(token, options={"verify_signature": False})
            self.AccounT_Uid = self.AfTer_DeC_JwT.get('account_id')
            self.EncoDed_AccounT = hex(self.AccounT_Uid)[2:]
            self.HeX_VaLue = DecodE_HeX(Timestamp)
            self.TimE_HEx = self.HeX_VaLue
            self.JwT_ToKen_ = token.encode().hex()
            print(f'- ProxCed Uid => {self.AccounT_Uid}')
        except Exception as e:
            print(f"- Error In ToKen : {e}")
            return
        try:
            self.Header = hex(len(EnC_PacKeT(self.JwT_ToKen_ , key , iv)) // 2)[2:]
            length = len(self.EncoDed_AccounT)
            self.__ = '00000000'
            if length == 9: self.__ = '0000000'
            elif length == 8: self.__ = '00000000'
            elif length == 10: self.__ = '000000'
            elif length == 7: self.__ = '000000000'
            else:
                print('Unexpected length encountered')                
            self.Header = f'0115{self.__}{self.EncoDed_AccounT}{self.TimE_HEx}00000{self.Header}'
            self.FiNal_ToKen_0115 = self.Header + EnC_PacKeT(self.JwT_ToKen_ , key , iv)
        except Exception as e:
            print(f" - Erorr In Final Token : {e}")
        self.AutH_ToKen = self.FiNal_ToKen_0115
        print(f'- GuiLd Uid => {self.Guild_Uid}\n- AuTh CodE => {self.Auth_Code}')
        self.Connect_SerVer(self.JwT_ToKen , self.AutH_ToKen , ip , port , key , iv , ip2 , port2 , self.Guild_Uid , self.Auth_Code)       
        return self.AutH_ToKen , key , iv
        
def StarT_SerVer():

    FF_CLient('uid','pas')
  
StarT_SerVer()