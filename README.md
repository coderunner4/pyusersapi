# pyusersapi
Python UsersAPI
The application is implemnted in a way that the there is clear chain of responsibility and each resource API encapsulated under respected classes, and data repositories implemented so the logic is independant of database implementation

Please following instructions 
1. Change _zip to .zip
2. Extract the folder and
   ```
   py -m venv .venv
   .venv\scripts\activate
   ```
   then to install dependencies (it should install necessary components)
   ```
   pip install -r requirements.txt
   ```
   Now run the application
   ```
   flask run
   ```
4. app.py is restful server side
5. app_client.py is restful api client

The restful api is implemented as follows

Calls to get users/add new http://127.0.0.1:5000/groups
1. [Get] Get Groups

Calls to get users/add new http://127.0.0.1:5000/users
1. [Get] Get Users
2. [Post] Add new user to list

Calls with a given username to get/update/delete from http://127.0.0.1:5000/users/user0
1. [Get] Get User
2. [Put] Update User
3. [Delete] Delete User

All calls with group information are checked against pre-papulated groups list on server

Appliations error code has following statuses
2xx Success. ... 200 OK, 201 New Item Created
4xx Client Error. ...400 Client provide information wrong, 404 Not Found
5xx Server Error.
