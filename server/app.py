# app.py
# This project is to create users provisioning system with Restful API to manage users and their groups 
# This application uses repository interface to add/update/delete the information. 
# The InMemoryRepo is provided but ideally any other db implementation can be plugin 

from flask import Flask, jsonify, abort, make_response, json
from flask_restful import Api, Resource, reqparse, fields, marshal

app = Flask(__name__, static_url_path="")
api = Api(app)

# user marshal fields
user_fields = {
	'username': fields.String,
	'email': fields.String,
	'fullname': fields.String,
	'groups': fields.List(fields.String),
	'uri': fields.Url('user')
}

# Base repository class that defines the interface to add/update/delete entity
class BaseRepo(object):
	
	def find(self, pk):
		""" find the item using identifier """
		raise NotImplementedError()
	
	def add(self, pk, entity):
		""" add the item. It throw and exception if item already exists """
		raise NotImplementedError()

	def update(self, pk, entity):
		""" update the item. It throw and exception if item not exists """
		raise NotImplementedError()
	
	def delete(self, pk):
		""" Delete an item using identifier """
		raise NotImplementedError()
	
	def create(self, **kw):
		""" Create item obj based on paramters (key1=value1, key2=value2)  """
		raise NotImplementedError()

# InMemory implementation of repository that defines the interface to add/update/delete entity		
class InMemoryRepo(BaseRepo):
	def __init__(self, entity_class):
		self.entity_class = entity_class
		self.entities = {}
	
	def find(self, pk):
		return self.entities.get(pk, None)
	
	def add(self, pk, entity):
		if pk in self.entities.keys():
			raise Exception("Entity already exist yet!")            
		self.entities[pk] = entity
		return entity

	def update(self, pk, entity):
		if pk not in self.entities.keys():
			raise Exception("Entity does not exist yet!")
		self.entities[pk] = entity
	
	def delete(self, pk):
		self.entities.pop(pk)
	
	def create(self, **kw):
		return self.entity_class(**kw)
	
	def all(self):
		return list(self.entities.values())

class Group(object):
	def __init__(self, groupname, groupdesc):
		""" Group constructor """
		self.groupname = groupname
		self.groupdesc = groupdesc
		
class User(object):
	def __init__(self, username, email, fullname, groups):
		""" User constructor """
		self.username = username
		self.email = email
		self.fullname = fullname
		self.groups = groups

class GroupListAPI(Resource):
	def __init__(self):
		""" Group List API constructor """
		self.groups = GroupRepository
		super(GroupListAPI, self).__init__()

	def get(self):
		""" Get All Group List """
		return [group.groupname for group in self.groups.all()]
	
class UserListAPI(Resource):
	def __init__(self):
		""" User List API constructor """
		self.users = UserRepository
		self.groups = GroupRepository
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('username', type=str, required=True,
								   help='No user username provided',
								   location='json')        
		self.reqparse.add_argument('email', type=str, required=True,
								   help='No user email provided',
								   location='json')
		self.reqparse.add_argument('fullname', type=str, default="",
								   location='json')
		self.reqparse.add_argument('groups', type=str, action='append')		
		super(UserListAPI, self).__init__()

	def get(self):
		""" Get All User List """
		rtnusers = []
		for user in self.users.all():
			u = marshal(user, user_fields)			
			rtnusers.append(u)
		return rtnusers

	def post(self):
		""" Add User to list """
		args = self.reqparse.parse_args()
		id = args['username']
		grps = args['groups']
	
		grpok = self.checkgroups(grps)
		if not grpok:
			abort(400)
	
		u = self.users.create(username = id, email= args['email'], fullname = args['fullname'], groups = grps)
		self.users.add(id, u)
		return marshal(u, user_fields), 201

	def checkgroups(self, grps):
		""" Check group exists in server groups list """
		grpok = False
		if len(grps) > 0:
			grpok = len(grps) > 0
			for k in grps:
				if self.groups.find(k) is None:
					grpok = False
					break;
		return grpok

class UserAPI(Resource):
	def __init__(self):
		""" User API constructor """
		self.users = UserRepository
		self.groups = GroupRepository
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('email', type=str, location='json')
		self.reqparse.add_argument('fullname', type=str, location='json')
		self.reqparse.add_argument('groups', type=str, action='append')		

		super(UserAPI, self).__init__()

	def get(self, username):
		""" Get User information """
		user = self.users.find(username)
		if user is None:
			abort(404)
		return marshal(user, user_fields)

	def put(self, username):
		""" Update User information, abort request if suppied groups do not exist"""
		user = self.users.find(username)
		if user is None:
			abort(404)
		
		args = self.reqparse.parse_args()
		grps = args['groups']
		if grps:
			grpok = self.checkgroups(grps)
			if not grpok:
				abort(400)

		for k, v in args.items():
			if v is not None:
				setattr(user, k, v)	
		self.users.update(user.username, user)
		return marshal(user, user_fields)

	def delete(self, username):
		""" Delete User """
		user = self.users.find(username)
		if user is None:
			abort(404)
		self.users.delete(user.username)
		return {'result': True}

	def checkgroups(self, grps):
		""" Check group exists in server groups list """
		grpok = False
		if len(grps) > 0:
			grpok = len(grps) > 0
			for k in grps:
				if self.groups.find(k) is None:
					grpok = False
					break;
		return grpok
	
class HelloWorld(Resource):
    def get(self):
        return {'usersapi': 'v1'}
	
# Initialize group repositories
# Add default groups
GroupRepository = InMemoryRepo(Group)
for i in range(0, 3):
	gid = 'group' + str(i)
	g = GroupRepository.create(groupname = gid, groupdesc= 'group ' + str(i))
	GroupRepository.add(gid, g)

# Initialize user repositories
# Add default users
UserRepository = InMemoryRepo(User)
for i in range(0, 1):
	uid = 'user' + str(i)
	u = UserRepository.create(username = uid, email= 'email'+ str(i) + '@abc.com', fullname = 'fullname' + str(i), groups = ['group1'])
	UserRepository.add(uid, u)

# Setup flask-restful api
api.add_resource(HelloWorld, '/')
api.add_resource(GroupListAPI, '/groups', endpoint='groups')
api.add_resource(UserListAPI, '/users', endpoint='users')
api.add_resource(UserAPI, '/users/<username>', endpoint='user')

#if __name__ == '__main__':
#	app.run(debug=True)
