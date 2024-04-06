import requests
import json


print("\ntest JSON->XML\n")
url = "http://127.0.0.1:5000/json_to_xml"
headers = {'Content-type': 'application/json'}
with open("modules/templates/App_info.json", encoding="utf-8") as file:
    data = json.load(file)
response = requests.post(url, data=json.dumps(data), headers=headers)

if response.status_code == 200:
    print(response.text)
else:
    print(response.status_code, response.text)

print("\ntest XML->JSON\n")
url = "http://127.0.0.1:5000/xml_to_json"
headers = {"Content-type": "application/xml"}
with open("modules/templates/Get_Entrant_List.xml", encoding="utf-8") as file:
    data = file.read()
response = requests.post(url, data=data.encode("utf-8"), headers=headers)


if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)
