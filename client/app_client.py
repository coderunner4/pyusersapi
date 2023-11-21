# app_client.py

import requests

base_url = 'http://127.0.0.1:5000' 

def get_url(path):
	return (base_url + path) 

# Manage users
def get_groups():
    return requests.get(get_url('/groups'))

# Manage users
def get_users():
    return requests.get(get_url('/users'))

def get_user(username):
    return requests.get(get_url('/users/{}'.format(username)))

def add_user(username, email, fullname, groups):
    return requests.post(get_url('/users'), json={
		'username': username,
        'email': email,
		'fullname': fullname,
		'groups': groups
        })

def update_user(username, email, fullname, groups):
    url = get_url('/users/{}'.format(username))
    return requests.put(url, json={
 		'email': email,
		'fullname': fullname,
		'groups': groups
        })

def user_delete(username):
    return requests.delete(get_url('/users/{}'.format(username)))

print('==Groups')
resp = get_groups()
for itm in resp.json():
	print(itm)  

username = 'user420'
print('==Users')
resp = get_users()
for itm in resp.json():
	print('{} {}'.format(itm['username'], itm['email']))  
resp = add_user(username, username +'@abc.com', username +' name', ['group1'])
print('==Added:{}'.format(resp.json()['username']))

resp = get_user(username)
res = resp.json()
print('==Info:{} {}'.format(res['username'], res['email']))

resp = update_user(username, username +'@abc123.com', username +' name123', ['group1', 'group2'])
print('==Update:{}'.format(resp.json()['username']))

resp = get_user(username)
res = resp.json()
print('==Info:{} {}'.format(res['username'], res['email']))

resp = user_delete(username)
print('==Deleted:' + str(resp.json()['result']))
