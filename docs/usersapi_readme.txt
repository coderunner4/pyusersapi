The application is implemnted in a way that the there is clear chain of responsibility and each resource API encapsulated under respected classes, and data repositories implemented so the logic is independant of database implementation

Please following instructions 
1. Change _zip to .zip
2. Extract the folder and run setup.bat (it should install necessary components)
3. app.py is restful server side
4. app_client.py is restful api client

The restful api is implemented as follows

Calls to get users/add new http://127.0.0.1:5000/groups
1. [Get] Get Groups

Calls to get users/add new http://127.0.0.1:5000/users
1. [Get] Get Users
2. [Post] Add new user to list

Calls with username to get/update/delete from http://127.0.0.1:5000/users/user0
3. [Get] Get User 
4. [Put] Update User
5. [Delete] Delete User

All calls with group information are checked against precreated groups
Appliations error code has following statuses

2xx Success. ... 200 OK, 201 New Item Created
4xx Client Error. ...400 Client provide information wrong, 404 Not Found
5xx Server Error.