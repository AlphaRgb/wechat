import json

a = '{"access_token":"ACCESS_TOKEN","expires_in":7200}'
b = json.loads(a)
print(b,type(b))