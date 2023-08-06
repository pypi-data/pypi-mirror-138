#-----------------------------------------------------------------------
import os
import sys
import json
import time
import shutil
from pathlib import Path, PurePath


#-----------------------------------------------------------------------
if "." in __name__:
	from modules import config
	from modules import tasks
	from modules import database
	from modules import web
	from modules import cli

else:
	import config
	import tasks
	import database
	import web
	import cli


#-----------------------------------------------------------------------
# ~ def create_collections():
	# ~ [ "mounts", "software", "projects", "log", "users" ]
projects 				= database.Blueprint()
projects["name"]		= database.String()
projects["root"]		= database.Path()
projects["kwargs"]		= database.Dictionary()
# ~ projects["uuid"]		= database.String()
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
# ~ perhaps also and extra command to create a function in web as url, something with /cli/func_name?
# ~ web.add_command( ( available_software , type = toggle, url = "/fsefd/fsd/url" )


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
#
# helper functions
#
#-----------------------------------------------------------------------
def create_project( name, root, **kwargs ):
	# ~ projects = database.get_collection( "projects" )
	result 	= projects_collection.find_one( name = name )
	
	if result != None:
		raise ValueError( f'A project with the name {name} already exists with root "{result[ "root" ]}"!' )

	doc = projects_collection.create_document()
	doc["name"] 	= name
	doc["root" ] 	= root
	# kwargs in een bestandje in de root van het project
	doc["kwargs" ] 	= kwargs

	if is_file( doc["root"] ):
		raise ValueError( f'"{root}" is a file, select a directory instead.' )
	elif not is_folder( doc["root"] ):
		raise ValueError( f'{root} does not exist.' )

	projects_collection.append( doc )
	set_project( name )

cli.add_command( create_project )


#-----------------------------------------------------------------------
def available_projects():
	# ~ coll 	= database.get_collection( "projects" )
	results = projects_collection.find()
	
	print("#"*32)
	print( "Projects available:" )
	for result in results:
		print( "%s: %s" % ( result["name"],  result["root"] ) )
	print("#"*32)
	return [ item["name"] for item in results ]

cli.add_command( available_projects )


#-----------------------------------------------------------------------
def set_project( name ):
	if name in available_projects():
		print( f'setting project "{name}"')
		config.PROJECT = name
	else:
		raise Exception( f"No project found with the name: {name}" )

cli.add_command( set_project )

#-----------------------------------------------------------------------
#
# helper functions
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


#-----------------------------------------------------------------------
def toggle_status():
	config.STATUS = not config.STATUS

toggle_by_click 			= web.SimpleClick( "toggle_status" )
toggle_by_click.function 	= toggle_status


#-----------------------------------------------------------------------
def load():
	pass
	# change name to init or start, to indicate it is a first run!
	# ~ create_collections()

#-----------------------------------------------------------------------
load()

