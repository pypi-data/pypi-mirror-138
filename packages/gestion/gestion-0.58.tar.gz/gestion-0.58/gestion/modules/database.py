import os
import sys
import json
import inspect
import pymongo
import pathlib
from bson.objectid 	import ObjectId
from datetime 		import datetime
from markupsafe 	import Markup


#-----------------------------------------------------------------------
#
#	add a watch function, if change happend to collection, add it to an collection_exists
#	check is userhost has already checked if change happened
#	if not already checked and change took place, return true and add userhost to collection changed
#	if collection changed remove all user hosts 
#
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
#
#	mongod version  v4.4.4
#	pymongo 3.12.0
# 	https://github.com/AlexandreMahdhaoui/MongoNow
#	misschien al extra module installeren zodat er geen echte mongodb hoeft te runnen in eerste instantie
#	of dat je kunt kiezen dat je een connectie wil maken met een server of dat het alleen lokaal runt
#
#-----------------------------------------------------------------------
if "." in __name__:
	from modules import config
else:
	import config


#-----------------------------------------------------------------------
#
#	document, blueprint class
#
#-----------------------------------------------------------------------
class Blueprint( dict ):
	root_id = ObjectId( b"%012d" % 0 )
	def __init__( self ):
		dict.__init__( self )
		if self.__class__ == Blueprint:
			dict.__setitem__( self, "_id", Blueprint.root_id )

		self.set_local( False )


	@property
	def _id( self ):
		if "_id" in dict.keys( self ):
			return dict.__getitem__( self, "_id" )
		else:
			return None


	def is_local( self ):
		return isinstance( self[ "_local" ], Userhost )


	def set_local( self, local:bool ):
		if local == False:
			datatype = Null()
		else:
			datatype = Userhost()

		datatype.hidden = True
		dict.__setitem__( self, "_local", datatype )


	def __setitem__( self, attr, datatype ):
		if attr not in  [ "_id" ] :
			if isinstance( datatype, Datatype ):
				if not attr.startswith( "_" ):
					dict.__setitem__( self, attr, datatype )
				else:
					raise Exception( f"{attr} is an invalid attribute name, it can not start with an underscore!" )
			else:
				raise Exception( f"Can't add {type( datatype )}, need a {database.Datatype}." )
		else:
			raise Exception( f"Can not set '_id' of {self.__class__.__name__}" )


	def __getitem__( self, attr ):
		item = dict.__getitem__( self, attr )
		if attr not in [ "_id" ]:
			if not isinstance( item, Datatype ):
				instance = getattr( sys.modules[ item[ "_module" ] ], item[ "_class" ] )()
				instance.update( item )
				self.__setitem__( attr, instance )
				return instance
			else:
				return item
		else:
			return item


	def keys( self, ignore = None ):
		#---------------------------------------------------------------
		#
		# ignore types are properties like locked and hidden, not the name of keys
		#
		#---------------------------------------------------------------
		if ignore == None:
			ignore = []
		
		keys_to_ignore 			= [] 
		attributes_to_ignore 	= []
		
		for item in ignore:
			if item in [ "saved", "id" ]:
				keys_to_ignore.append( f"_{item}" )
			elif item in [ "locked", "hidden", "unique" ]:
				attributes_to_ignore.append( f"_{item}" )
			else:
				raise ValueError( "Ignorelist can only contain 'id', 'saved', 'unique', 'locked' or 'unique'" )


		keys = list( dict.keys( self ) )
		for item in self.items():
			if item[0] not in [ "_id", "_saved" ]:
				for attr_to_ignore in attributes_to_ignore:
					if item[ 1 ][ attr_to_ignore ] == True:
						result = item[ 1 ][ attr_to_ignore ]
						if item[ 0 ] in keys:
							
							keys.pop( keys.index( item[ 0 ] ) )
			
			elif item[0] in keys_to_ignore:
				if item[ 0 ] in keys:
					keys.pop( keys.index( item[ 0 ] ) )

		return keys


	def set_all_values( self ):
		for key in self.keys( ignore = [ "id", "saved" ] ):
			inst = dict.__getitem__( self, key )
			inst.value_setter()


	def print( self, pretty_print = False ):
		print( self )


#-----------------------------------------------------------------------
class Document( Blueprint ):
	def __init__( self ):
		Blueprint.__init__( self )


	@classmethod
	def create_from_blueprint( cls, blueprint:Blueprint ):
		inst = cls()
		inst.update( blueprint )
		return inst


	def create_new_id( self ):
		dict.__setitem__( self, "_id", ObjectId() )


	def __setitem__( self, attr, value ):
		if attr not in ["_id", "_saved" ]:
			Blueprint.__getitem__( self, attr ).value = value
		else:
			dict.__setitem__( self, attr, value )


	def __getitem__( self, attr ):
#		need to add a reserved keys attribute
		if attr not in [ "_id", "_saved" ]:
			# print( "not in list")
			return Blueprint.__getitem__( self, attr ).value
		else:
			# print( "attr starts with an underscore")
			return dict.__getitem__( self, attr )


	def update( self, kwargs ):
		if "_id" in kwargs:
			if kwargs["_id"] == Blueprint.root_id:
				kwargs.pop( "_id" )
		dict.update( self, kwargs )


	def set_all_values( self, for_insert = True ):
		Blueprint.set_all_values( self )
		if for_insert:
			# ~ # print( "for_insert" )
			_saved = { "_functions":{} }
			for key in self.keys( ignore = [ "id", "saved" ] ):
				datatype				= Blueprint.__getitem__( self, key )
				_saved[ key ]			= datatype.as_html( self )
				_saved[ "_collection" ] = datatype[ "_collection" ]
				_function 				= datatype[ "_function" ]
				if _function != None:
					_saved[ "_functions" ][ key ] = f'{_function[ "_href" ]}'
			_saved[ "_id" ] = self._id
			# ~ print( f"_saved:  {_saved}" )
			dict.__setitem__( self, "_saved", _saved )


#-----------------------------------------------------------------------
#
# Collection class, connection to a database
#
#-----------------------------------------------------------------------
class Collection( object ):
	def __init__( self, name ):
		self._name 		= name
		self._blueprint = None
		self._sort 		= ( "_id", -1 )
		self._limit		= 25


	def __str__( self ):
		return "<Instance of Collection: %s>" % self.name


	def __repr__( self ):
		return "<Instance of Collection: %s>" % self.name


	@classmethod
	def create_from_blueprint( cls, name:str, blueprint:Blueprint ):
		coll = cls( name )
		coll.blueprint = blueprint
		if not coll.exists: 
			coll.database[ name ].insert_one( coll._blueprint )

		return coll


	@property
	def name( self ):
		return self._name


	@name.setter
	def name( self, name ):
		self._name = name


	@property
	def database_name( self ):
		return self.database.name


	@property
	def database( self ):
		return connect_to_database()


	@property
	def exists( self ):
		if self.database_name in list_databases():
			if collection_exists( self.name ):
				result = self.database[ self.name ].find_one( { "_id": Blueprint.root_id } )
				if result != None:
					# ~ self._blueprint = Blueprint.create_from_dict( result )
					return True
				else:
					return False
		else:
			return False


	@property
	def blueprint( self ):
		if not self.exists:
			raise Exception( f"No collection found for {self.name} in database {self.database_name}!" ) 

		else:
			if self._blueprint is None:
				result = self.database[ self.name ].find_one( { "_id": Blueprint.root_id } )
				object_id = 	result.pop( "_id" , None )
				if object_id == Blueprint.root_id:
					blueprint = Blueprint()
					for key in result.keys():
						data 			= result[key]
						instance		= getattr( sys.modules[ data[ "_module" ] ], data[ "_class" ] )()
						instance.update( data )
						if not key.startswith( "_" ):
							blueprint[ key ]= instance
							# ~ if instance.function != None:
								# ~ create_route_for_click( instance, check_exists = True )
						elif key == "_local":
							blueprint.set_local( isinstance( instance, Userhost ) )
					self._blueprint = blueprint

				else:
					raise Exception( f"Need results from collection {self.name} with a root_id, result has a different _id!" )
			return self._blueprint


	@blueprint.setter
	def blueprint( self, blueprint ):
		if isinstance( blueprint, Blueprint ):
			for key in blueprint.keys():
				if key != "_id":
					attr = blueprint[ key ][ "_collection" ] = self.name
			blueprint.set_all_values()
			self._blueprint = blueprint

		else:
			raise Exception( "Need a Blueprint instance, not a %s " % type( blueprint ) )

		# ~ else:
			# ~ raise Exception( "Collection %s already exists!" % self.name )


	def is_local( self ):
		return self.blueprint.is_local()


	def has_changed( self ):
		return check_for_changes( self.name )


	def create_document( self, kwargs:dict = {} ):
		blueprint = self.blueprint
		if self.is_local():
			# ~ blueprint["local"]
			pass
		document = Document.create_from_blueprint( self.blueprint )
		if self.is_local():
			document.local = Userhost()

		for key in kwargs:
			document[ key ] = kwargs[ key ]
		return document


	def create( self ):
		if not self.exists:
			if self._blueprint != None:
				self.database[ self.name ].insert_one( self._blueprint )


	def append( self, document:Document ):
		document.create_new_id()
		document.set_all_values()
		result = self.database[ self.name ].insert_one( document )
		# ~ print( dir( result ) )
		register_database_change( self.name )
		return result.inserted_id


	def extend( self, *documents ):
		self.database[ self.name ].insert_many( *[ doc.set_all_values() for doc in documents ] )
		register_database_change( self.name )


	def clear( self ):
		self.database[ self.name ].delete_many( {} )
		register_database_change( self.name )

	
	def delete_one( self, key ):
		self.database[ self.name ].delete_one( { "_id" : ObjectId(key) } )
		register_database_change( self.name )


	def drop( self ):
		self.database[ self.name ].drop()
		register_database_change( self.name )


	def __getitem__( self, key ):
		# ~ if isinstance( key, slice ):
			# ~ start 	= int( key.start ) + 1
			# ~ end 	= int( key.stop ) + 1
			# ~ results = []
			# ~ for item in list( self.database[ self.name ].find( {} )[ start:end ] ):
				# ~ doc 	= self.blueprint.copy()
				# ~ doc.update( item )
				# ~ results.append( doc )
			# ~ return results
		
		if isinstance( key, ObjectId ):
			result = self.database[ self.name ].find_one( { "_id" : key } )
			return self.create_document( result )
		else:
			raise ValueError( "No item found with _id: " + str( key ) )


	def __setitem__( self, key, document:Document ):
		if isinstance( key, ObjectId ):
			if key == Blueprint.root_id:
				raise ValueError( "Changing document with __root_id will change blueprint, use update_blueprint instead!" )
			else:
				if self.database[ self.name ].find_one( { "_id" : key } ):
					try:
						document.set_all_values()
						self.database[ self.name ].replace_one(  { "_id" : key }, document )
						register_database_change( self.name )
					except Exception as e:
						raise ValueError( str( e ) )
				else:

					raise ValueError( "No item found with _id: " + str( key ) )
		else:
			raise ValueError("Key needs be an ObjectdId and not a " + type( key ) )


	def __iter__( self ):
		#
		# if host is server self is local ignore 
		# of iets anders verzinnen dat je ook alle 
		# 
		kwargs = { "_id" :{ "$ne": Blueprint.root_id } }
		if self.is_local():
			kwargs[ "_local" ] = Userhost().value

		for item in self.find():
			yield self.create_document( item )


	def find( self, **kwargs ):
		if self.is_local():
			kwargs[ "_local" ] = Userhost().value

		kwargs.update( { "_id" :{ "$ne": Blueprint.root_id } } )
		results = [ self.create_document( item ) for item in self.database[ self.name ].find( kwargs, sort = [ self._sort ], limit = self._limit ) ]
		return results


	def find_in_cache( self, **kwargs ):
		if self.is_local():
			kwargs[ "_local" ] = Userhost().value
		kwargs.update( { "_id" :{ "$ne": Blueprint.root_id } } )
		return [ item["_saved"] for item in self.database[ self.name ].find( kwargs, sort = [ self._sort ], limit = self._limit ) ]


	def find_one( self, **kwargs ):
		if self.is_local():
			kwargs[ "_local" ] = Userhost().value

		kwargs.update( { "_id" :{ "$ne":  Blueprint.root_id } } )
		result = self.database[ self.name ].find_one( kwargs )

		if result == None:
			doc = None
		else:
			doc = self.create_document( result )

		return doc


#-----------------------------------------------------------------------
#
# datatype classes
# _function needs to be renamed to "on_click", "click" or something a-like
#
#-----------------------------------------------------------------------
class Datatype( dict ):
	"""
	change html to innertext
	"""
	def __init__( self ):
		dict.__init__( self, {	"_raw_value"	: None,
								"_locked" 		: False,
								"_hidden" 		: False,
								"_unique" 		: False,
								"_function"		: None,
								"_class"		: self.__class__.__name__,
								"_module"		: self.__class__.__module__,
								"_collection"	: None,
								"_innertext"	: None,
								"_href"			: None,
								} )
		self.value_setter()


	def __getattribute__( self, attr ):
		if attr == "value":
			return self.decoder( self.raw_value )
		
		elif attr in [ "function", "innertext" ]:
			value =  dict.__getitem__( self, f"_{attr}" )
			if value != None:
				return getattr( sys.modules[ value[ "_func_module" ] ], value[ "_func_name" ] )
			else:
				return value
		
		elif f"_{attr}" in dict.keys( self ):
				return dict.__getitem__( self, f"_{attr}" )

		else:
			return dict.__getattribute__( self, attr )


	def __setattr__( self, attr, value ):
		if attr == "value":
			dict.__setitem__( self, "_raw_value", self.encoder( value ) ) 
		elif attr in [ "function", "innertext" ]:
			result = value
			if attr == "innertext":
				if callable( value ):
					self._func_parser( value )
					# ~ result = value
				elif type( value ).__name__ in dir(builtins):
					def return_static_variable():
						return value
					result = return_static_variable
				else:
					raise ValueError( f"Cannot set function to a type of {type( value ).__name__}" )
		# ~ else:
			# ~ raise ValueError( f"Cannot set function to a type of {type(func).__name__}" )

			function = { "_func_module" : result.__module__, "_func_name" : result.__name__ }
			dict.__setitem__( self, f"_{attr}", function )
			if attr == "function":
				function[ "_href" ] = create_route_for_click( self )


		elif f"_{attr}" in dict.keys( self ):
			return dict.__setitem__( self, f"_{attr}", value )

		else:
			raise ValueError( f"{__class__.__name__} has no attribute {attr}" )


	def encoder( self, value ):
		return value


	def decoder( self, value ):
		return value


	def value_setter( self ):
		pass


	def _func_parser( self, func ):
		 pass


	def as_html( self, doc:Document ):
		if self.innertext == None:
			return self.value
		else:
			return self.innertext( doc )



#-----------------------------------------------------------------------
class Dictionary( Datatype ):
	def __init__( self, **kwargs ):
		Datatype.__init__( self, **kwargs )
		self.value = {}


#-----------------------------------------------------------------------
class List( Datatype ):
	def __init__( self, **kwargs ):
		Datatype.__init__( self, **kwargs )
		self.value = []


#-----------------------------------------------------------------------
class Integer( Datatype ):
	def __init__( self, **kwargs ):
		Datatype.__init__( self, **kwargs )
		self.value = 0


#-----------------------------------------------------------------------
class Boolean( Datatype ):
	def __init__( self, **kwargs ):
		Datatype.__init__( self, **kwargs )
		self.value = False


#-----------------------------------------------------------------------
class Float( Datatype ):
	def __init__( self, **kwargs ):
		Datatype.__init__( self, **kwargs )
		self.value = 0.0

#-----------------------------------------------------------------------
class String(Datatype):
	def __init__( self, **kwargs ):
		Datatype.__init__( self, **kwargs )


#-----------------------------------------------------------------------
class Null( Datatype ):
	def __init__( self, **kwargs ):
		Datatype.__init__( self, **kwargs )

	def value_setter( self ):
		 self.value = None


#-----------------------------------------------------------------------
class Date( String ):
	def __init__( self, **kwargs ):
		String.__init__( self, **kwargs )


	def value_setter( self ):
		now = datetime.now()
		self.value = now.strftime( "%d/%m/%Y %H:%M:%S" )



#-----------------------------------------------------------------------
class Path( String ):
	# use pathlib instead of os.path!
	def __init__( self, **kwargs ):
		String.__init__( self, **kwargs )


	def encode( self, value ):
		return value


	def decode( self, value ):
		# ~ print( node.__name__ )
		return value

	@property
	def exists( self ):
		return os.path.exists( self.value )


	@property
	def is_file( self ):
		return os.path.isfile( self.value )


	@property
	def is_dir( self ):
		return os.path.isdir( self.value )


	@property
	def absolute_path( self ):
		return "abs_path for: %s" % self.value


	@property
	def relative_path( self ):
		return "rel_path for: %s" % self.value


	@property
	def base_name( self ):
		return "base_name for: %s" % self.value


	@property
	def original_path( self ):
		return self._orig_value


#-----------------------------------------------------------------------
class Directory( Path ):
	def __init__( self, **kwargs ):
		Path.__init__( self, **kwargs )


class File( Path ):
	def __init__( self, **kwargs ):
		Path.__init__( self, **kwargs )

	@property
	def extension( self ):
		return os.path.splitext( self.value )[-1]


#-----------------------------------------------------------------------
class Userhost( Datatype ):
	def __init__( self, **kwargs ):
		Datatype.__init__( self, **kwargs )
		# ~ self.value = [ config.USER, config.HOST ]

	
	@property
	def user( self ):
		return self.value[1]


	@property
	def host( self ):
		return self.value[0]


	def value_setter( self ):
		self.value = [ config.HOST, config.USER ]


#-----------------------------------------------------------------------
class User( String ):
	def __init__( self, **kwargs ):
		String.__init__( self, **kwargs )

	def value_setter( self ):
		self.value = config.USER


class Host( String ):
	def __init__( self, **kwargs ):
		String.__init__( self, **kwargs )


	def value_setter( self ):
		self.value = config.HOST


#-----------------------------------------------------------------------
#
# helper functions
#
#-----------------------------------------------------------------------
def database_is_running():
	connection = pymongo.MongoClient( "%s" % config.DATABASE_IP, config.DATABASE_PORT, serverSelectionTimeoutMS = 2000 )
	try:
		return connection.server_info() # will throw an exception

	except Exception as e:
		return False


def connect_to_database( name = None ):
	if name == None:
		name = config.GESTION_DB
	connection = pymongo.MongoClient( "%s" % config.DATABASE_IP, config.DATABASE_PORT )
	return connection[ name ]


def list_databases():
	connection = pymongo.MongoClient( "%s" % config.DATABASE_IP, config.DATABASE_PORT )
	return [ db["name"] for db in connection.list_databases() if db["name"] not in [ "admin", "config", "local" ] ]


def list_collections( ):
	database = connect_to_database( )
	return database.list_collection_names()


def collection_exists( name:str ):
	return name in list( list_collections() )


def create_collection( name:str, blueprint:Blueprint ):
	coll = Collection( name )
	coll.blueprint = blueprint
	if not coll.exists: 
		coll.create()
		
	return coll


def get_collection( name:str ):
	if name in list_collections( ):
		coll = Collection( name )
		return coll
	else:
		raise Exception( "Collection %s does not exist in database %s" % ( name, config.GESTION_DB ) )


#-----------------------------------------------------------------------
def init():
	if database_is_running():
		if config.NODE_TYPE == "master":
			if config.GESTION_DB not in list_databases():
				database = connect_to_database()
	else:
		raise Exception( "Cannot connect to database on: %s" % config.DATABASE_IP )


#-----------------------------------------------------------------------
def create_route_for_click( datatype, check_exists = False ):
	# ~ print ( "create_route_for_click" )
	# ~ print( datatype )
	from modules import web
	exists 	= False
	func	= datatype.function
	# ~ print( func )
	# ~ func( "Arno" )
	# ~ exit()
	url		= f"{func.__module__}/{func.__name__}"
	# ~ print( f"generated url is {url}" )
	
	if web.server != None:
		# ~ print( "web.server != None" )
		if check_exists:
			if f"/{url}" in [ rule.rule for rule in web.server.url_map.iter_rules() ]:
				exists = True
		
		if not exists:
			# ~ print( f" {url} doesnt exist" )
			simpleclick 				= web.SimpleClick( url )
			simpleclick.needs_document 	= True
			simpleclick.function 		= func
			web.create_route( simpleclick )
	
	return url


#-----------------------------------------------------------------------
#
#	create some database use by the database module
#
#-----------------------------------------------------------------------
if database_is_running():
	changes 				= Blueprint()
	changes[ "name" ] 		= String()
	changes[ "userhost" ]	= List()
	changes_collection 		= create_collection( "_database_changes", changes )
# ~ else:
	# ~ raise Exception( "Can't connect to the database" )




#-----------------------------------------------------------------------
def check_for_changes( collection ):
	init()
	results				= changes_collection.find( name = collection, userhost = Userhost().value )
	has_changed 		= False
	
	if len( results ) > 0:
		has_changed = True
		for item in results:
			changes_collection.delete_one( item._id )

	return has_changed


#-----------------------------------------------------------------------
def register_database_change( collection ):
	init()
	if collection != changes_collection.name:
		# ~ changes_collection = get_collection( "_database_changes" )
		doc	 = changes_collection.create_document()
		doc[ "name" ] 		= collection
		doc[ "userhost" ]	= Userhost().value
		changes_collection.append( doc )



#-----------------------------------------------------------------------
if __name__ ==  "__main__":
	pass

