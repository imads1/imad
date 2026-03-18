import requests
from xTnito import xGeT

uid = ""
pas = ""
URL = "https://clientbp.ggblueshark.com/ChooseEmote"
T = xGeT(uid,pas)
PyL = bytes.fromhex("CAF683222A25C7BEFEB51F59544DB313")

Hrr = {
    "Expect": "100-continue",
    "X-Unity-Version": "2018.4.11f1",
    "X-GA": "v1 1",
    "ReleaseVersion": "OB52",
    "Authorization": "Bearer " + T,
    "Host": "loginbp.common.ggbluefox.com"
}

response = requests.post(URL, data=PyL, headers=Hrr, timeout=10)


print(f"resultat : {response.status_code}")