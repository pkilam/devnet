import json
import requests



requests.packages.urllib3.disable_warnings()

#Create a request to get list of interfaces through RESTCONF
api_url = "https://172.16.1.6/restconf/data/ietf-interfaces:interfaces"

headers = { "Accept": "application/yang-data+json",
            "Content-type": "application/yang-data+json"
          }

#user name and password for the request
basicauth = ("cisco", "cisco")

resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)
print(resp)
response_json = resp.json()
print(response_json)
print(json.dumps(response_json, indent=4))

#Use Put request to add an loopback interface loopback20 to the device
api_url = "https://172.16.1.6/restconf/data/ietf-interfaces:interfaces/interface=Loopback20"
headers = { "Accept": "application/yang-data+json",
            "Content-type": "application/yang-data+json"
          }
#user name and password for the request
basicauth = ("cisco", "cisco")

yangConfig = {
   "ietf-interfaces:interface": {
        "name": "Loopback20",
        "description": "Paul's Loopback 20",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "20.20.20.20",
                    "netmask": "255.255.255.255"
                }
            ]
        },
        "ietf-ip:ipv6": {}    
   }
}

resp = requests.put(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)

print("STATUS CODE: {}".format(resp.status_code))

