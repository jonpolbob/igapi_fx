import urllib.request 
import urllib.error 
import urllib.parse


#api IG : ouvre le compte demo et lit le header et le body de la reponse
# a partir de ca on peut faire marcher lightstreamer pour avoir des infos en streaming

url = r'https://demo-api.ig.com/gateway/deal/session'
print(url)

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

leheaders={'Content-Type':'application/json; charset=UTF-8',
        'Accept':'application/json; charset=UTF-8',
        'VERSION':'2',
        'X-IG-API-KEY':'2bb67dcbc934cf2b884f5b2922dfe0c4b724db5d',
         'User-Agent':user_agent
         }

lebody = { "identifier": "RM968demo",
           "password": "pqscsq2Snt!"
           }

import json

json_lebody = json.dumps(lebody).encode('utf8')

#print(json_lebody)
json_leheader = json.dumps(leheaders).encode('utf8')
#print(json_leheader)

req = urllib.request.Request(url,method='POST',headers=leheaders)
print('ok')
req.add_header('Content-Type','application/json; charset=UTF-8')
req.add_header('Accept','application/json; charset=UTF-8')
req.add_header('VERSION','2')
req.add_header('X-IG-API-KEY','2bb67dcbc934cf2b884f5b2922dfe0c4b724db5d')
req.add_header('User-Agent',user_agent)

resp = urllib.request.urlopen(req,json_lebody)
content = resp.headers

print(content) #header
parsed_data = json.loads(resp.read())
for item in parsed_data.items():
    print (item)
    

