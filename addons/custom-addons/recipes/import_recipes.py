import xmlrpc.client
import csv

server = "http://localhost:8016"
db = "dietfacts2"
username = "admin"
password = "admin"
# info = xmlrpc.client.ServerProxy('http://localhost:8016/start').start()
# url, db, username, password = info['host'], info['database'], info['user'], info['password']
#
# print(f"url====={url}, db======{db}, username===={username}, password======{password}")
formatted = '{}/xmlrpc/2/common'.format(server)
models = xmlrpc.client.ServerProxy(formatted)
uid = models.authenticate(db, username, password, {})
APIFormatted = '{}/xmlrpc/2/object'.format(server)
print(APIFormatted)
OdooAPI = xmlrpc.client.ServerProxy(APIFormatted)
ids = OdooAPI.execute_kw(db, uid, password, 'res.partner', 'search', [[]])
res = OdooAPI.execute_kw(db, uid, password, 'recipes.recipes', 'read', [ids])
print(res)
for recipe in res:
    print(recipe['name'])

