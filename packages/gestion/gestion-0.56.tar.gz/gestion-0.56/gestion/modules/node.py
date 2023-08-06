#-----------------------------------------------------------------------
import os
import sys
import json
import time
import shutil
from pathlib import Path, PurePath
from configparser import ConfigParser


#-----------------------------------------------------------------------
if "." in __name__:
	from modules import config
	from modules import database
	from modules import web
	from modules import cli
	from modules import tasks

else:
	import config
	import database
	import web
	import cli
	import tasks


#-----------------------------------------------------------------------
# ~ def create_collections():
	# ~ [ "mounts", "software", "projects", "log", "users" ]
projects 				= database.Blueprint()
projects["name"]		= database.String()
projects["root"]		= database.Path()
projects.set_local( True )
projects_collection 	= database.create_collection( "projects", projects )


software 				= database.Blueprint()
software["name"]		= database.String()
software["path"]		= database.Path()
software["extension"]	= database.String() # misschien list met strings?
software.set_local( True )
software_collection 	= database.create_collection( "software", software )


# https://stackoverflow.com/questions/54750273/pymongo-and-ttl-wrong-expiration-time
nodes 				= database.Blueprint()
nodes["host"]		= database.Host()
nodes["status"]		= database.String()
nodes["heartbeat"]	= database.Integer()
nodes_collection 	= database.create_collection( "nodes", nodes )


log 				= database.Blueprint()
log["type"]			= database.String()
log["log"] 			= database.String()
log["userhost"]		= database.Userhost()
log["date"]			= database.Date()
log.set_local( False )

log_collection		= database.create_collection( "log", log )



#-----------------------------------------------------------------------
#
# node tasks
#
#-----------------------------------------------------------------------
# https://stackoverflow.com/questions/54750273/pymongo-and-ttl-wrong-expiration-time
def heartbeat():
	while True:
		doc = nodes_collection.find_one( host = config.HOST )
		time.sleep( 10 )

heartbeat_task 		= tasks.Task( heartbeat )
heartbeat_task.wait = False


#-----------------------------------------------------------------------
#
# commonly used functions included
#
#-----------------------------------------------------------------------
def map_path( path ):
	pass


#-----------------------------------------------------------------------
def add_software( name, path, extension = None ):
	coll 				= database.get_collection( "software" )
	doc 				= coll.create_document()
	doc["name"]			= name
	doc["path"]			= path
	doc["extension"]	= extension
	coll.append( doc )

cli.add_command( add_software )


#-----------------------------------------------------------------------
def available_software():
	coll 	= database.get_collection( "software" )
	results = coll.find()
	
	print( f"Available software on {config.HOST}" )
	for item in results:
		print( f'{item["name"]}' )
	return [ item["name"] for item in results ]

cli.add_command( available_software )


#-----------------------------------------------------------------------
def get_software( name = None, extension = None ):
	path = None
	if name in available_software():

		kwargs = {}
		if name != None:
			kwargs[ "name" ] = name
		if extension != None:
			 kwargs[ "extension" ] = extension
		# print( kwargs )
		document = database.Collection("software").find_one( **kwargs )
		# print( document )
		if document:
			path = document[ "path" ]
		
		
	
	if path is None:
		raise ValueError( f"Cannot find specified software on {config.HOST}" )
	else:
		print( path )
		return path

cli.add_command( get_software )


#-----------------------------------------------------------------------
# ~ https://linuxtut.com/en/9f4dd46c96a86608f519/
# ~ parser.optionxform = str
#-----------------------------------------------------------------------
def create_workspace( name, root, **kwargs ):
	
	configparser 			 = ConfigParser()
	configparser[ "global" ] = kwargs
	workspace_file 			 = os.path.join( root, f"{name.lower()}.gestion" )
	print( f"Creating workspace with file:{workspace_file}" )
	with open( workspace_file, 'w' ) as f:
		configparser.write( f )


def load_workspace( workspace_file ):
	root, base 		= os.path.split( workspace_file )
	workspace_file 	= os.path.join( root, base.lower() )
	print( f"Load workspace from file:{workspace_file}" )
	configparser 	= ConfigParser()
	configparser.read( workspace_file )
	return configparser[ "global" ]


def workspace_exists( name ):
	doc = projects_collection.find_one( name = name )
	if doc == None:
		return False
	else:
		return file_exists( os.path.join( doc[ "root" ], f"{name}.gestion" ) )


#-----------------------------------------------------------------------
def create_project( name, root, **kwargs ):
	result 	= projects_collection.find_one( name = name )
	
	if result == None:
		if folder_exists( root ):
			if is_file( root ):
				raise ValueError( f'"{root}" is a file, select a directory instead.' )
			elif not is_folder( root ):
				raise ValueError( f'{root} does not exist.' )
			
			workspace_file = os.path.join( root, f"{name.lower()}.gestion" )
			if file_exists( workspace_file ):
				# ~ load_workspace( workspace_file )
				print( f'A project has already been created for {root}, not creating workspace.' )
			
			else:
				create_workspace( name, root, **kwargs )

			doc = projects_collection.create_document()
			doc["name"] 	= name
			doc["root" ] 	= root
			projects_collection.append( doc )
		# kwargs in een bestandje in de root van het project
	
	if workspace_exists( name ):
		set_project( name )


cli.add_command( create_project )


#-----------------------------------------------------------------------
def set_project( name ):
	doc = projects_collection.find_one( name = name )
	if doc != None:
		if workspace_exists( name ):
			workspace_file 		= os.path.join( doc[ "root" ], f"{name}.gestion" )
			config.WORKSPACE	= load_workspace( workspace_file )
			config.PROJECT_ROOT	= doc[ "root" ]
			config.PROJECT_NAME	= name
		else:
			raise Exception( f"Cannot find a workspace file in {doc[ 'root' ]}" )

	else:
		raise Exception( f"No project found in projects database with the name: {name}" )
	
	

cli.add_command( set_project )


#-----------------------------------------------------------------------
def available_projects():
	results = projects_collection.find()
	print("#"*32)
	print( "Projects available:" )
	for result in results:
		print( "%s: %s" % ( result["name"],  result["root"] ) )
	print("#"*32)
	return [ item["name"] for item in results ]

cli.add_command( available_projects )


#-----------------------------------------------------------------------
def delete_project( name ):
	doc = projects_collection.find_one( name = name )
	if doc != None:
		projects_collection.delete_one( doc._id )


cli.add_command( delete_project )


#-----------------------------------------------------------------------
def write_to_log( to_log:str ):
	coll 			= database.get_collection( "log" )
	doc		 		= coll.create_document()
	doc[ "log" ]	= to_log
	return coll.append( doc )



#-----------------------------------------------------------------------
#
# os helper functions
#
#-----------------------------------------------------------------------
def is_file( path ):
	path = Path( path )
	if path.exists():
		return path.is_file()
	else:
		return False


def is_folder( path ):
	path = Path( path )
	if path.exists():
		return path.is_dir()
	else:
		return False


def file_exists( path ):
	if Path( path ).exists():
		return is_file( path )
	else:
		return False


def folder_exists( path ):
	if Path( path ).exists():
		return is_folder( path )
	else:
		return False


def create_folder( path ):
	path = Path( path )
	if not path.exists():
		path.mkdir( parents=True )
	else:
		raise FileExistsError( f"Can not create directory {path}, it already exists.")


def copy( src, dst ):
	if is_folder( src ):
		shutil.copytree( src, dst, dirs_exist_ok = True )
	elif is_file( src ):
		shutil.copy( src, dst )

#-----------------------------------------------------------------------
#
# web pages for the node
#
#-----------------------------------------------------------------------
index_page				= web.Page( "/" )
settings_page			= web.Page( "settings", template = web.CollectionTemplate( software_collection ) )
project_page			= web.Page( "projects", template = web.CollectionTemplate( projects_collection ) )

log_template 	= web.CollectionTemplate( log_collection )
log_page 		= web.Page( "log", template = log_template )


#-----------------------------------------------------------------------
def toggle_status():
	config.STATUS = not config.STATUS

toggle_by_click 			= web.SimpleClick( "toggle_status" )
toggle_by_click.function 	= toggle_status




