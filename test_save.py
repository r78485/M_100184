import requests
import json

url = "http://127.0.0.1:8000/api/save-student/"
data = {
    "name": "Test Student",
    "dob": "2015-05-05",
    "gender": "Male",
    "blood": "O+",
    "cls": "Class 5",
    "religion": "Islam",
    "father": "Test Father",
    "phone": "01711111111",
    "mother": "Test Mother",
    "motherPhone": "",
    "presentAddr": "Dhaka",
    "admNum": "",
    "section": "A",
    "roll": ""
}
try:
    res = requests.post(url, json=data)
    print("Status Code:", res.status_code)
    print("Response Content:", res.text)
except Exception as e:
    print(e)
