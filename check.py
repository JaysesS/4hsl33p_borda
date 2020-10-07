import requests as r
from datetime import datetime
from time import sleep
creds = {'username': 'jayse', 'password': '1337'}
print('---------')
try:
    print("Time:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "Main:", r.get("http://46.254.20.217/").status_code, "Login:", r.post('http://46.254.20.217/signin', creds).status_code, "Reg:", r.post('http://46.254.20.217/signup', creds).status_code)
except Exception as e:
    print("Time:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "Error:", e)
print('---------')