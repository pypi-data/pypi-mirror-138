import os
import sys
import time
import argparse
from importlib import reload as reload


# -----------------------------------------------------------------------
WORKING_DIR = os.path.split( __file__ )[0]
sys.path.append( WORKING_DIR )


# -----------------------------------------------------------------------
import modules
from modules import config
from modules import database
from modules import cli
from modules import web
from modules import tasks
from modules import web
from modules import queue
from modules import watchfolder
from modules import node


# -----------------------------------------------------------------------
import addons


# -----------------------------------------------------------------------
def start():
	print( "Starting gestion" )
	if config.is_first_run:
		first_run()

	print( f"Using config file: {config.FILE}" )


	print( "Initializing the web server" )
	web.init( __name__ )


	results = database.database_is_running()
	if results is None:
		print( "Cannot connect to server on: %s" % database.DATABASE_IP )
		exit()


	print( "Connecting to database:\t'%s'" % config.GESTION_DB )
	database.load()
	print( "Loading node for host:\t'%s'" % config.HOST )
	node.load()


	#-------------------------------------------------------------------
	pages			 	= []
	processes_to_start 	= []

	for name in [ name for name in dir( modules ) if not name.startswith("__") ]:
		mod = getattr( modules, name )
		for item in dir( mod ):
			obj = getattr( mod, item )
			# ~ if isinstance( obj, type ):
			if isinstance( obj, web.Page ):
				pages.append( obj )
			elif isinstance( obj, tasks.Task ):
				processes_to_start.append( obj )
				# ~ web.create_route( obj )


	#-------------------------------------------------------------------
	addons_path = os.path.join( os.path.split( __file__ )[0], "addons"  )
	for f in os.listdir( addons_path ):
		if f[0] not in ["_", "."]:
			addon_name, extension = os.path.splitext( f )
			if extension.lower() == ".py":
				addon = getattr( addons, addon_name )
				for item in dir( addon ):
					obj = getattr( addon, item )
					# ~ if isinstance( obj, type ):
					if isinstance( obj, web.Page ):
						for route in obj:
							obj = f"/addon/{route}"
						pages.append( obj )
					elif isinstance( obj, tasks.Task ):
						processes_to_start.append( obj )


	print( "Creating pages" )
	for page in pages:
		web.create_route( page )


	print( "Starting tasks" )
	for proc in processes_to_start:
		print( "Starting task: %s" % proc.func_name )
		proc.execute()

	web.start_server()


#-----------------------------------------------------------------------
def first_run():
	print( f"First run, creating folders for gestion in {config.GESTION_FOLDER}" )
	default = os.path.join( config.GESTION_FOLDER, "default" )
	if not node.folder_exists( default ):
		node.create_folder( default )
	
	for folder in [ "static", "templates" ]:
		src = os.path.join( WORKING_DIR, "web", folder )
		dst = os.path.join( config.GESTION_FOLDER, folder )
		print( f"Copying: {src} -> {dst}" )
		node.copy( src, dst )
	
	config.create_file()
	# ~ node.create_project( "default", default )



#-----------------------------------------------------------------------
def main():
	if len( sys.argv ) > 1:
		cli.parse_args_and_execute( sys.argv )
	# check for args, parse them and execute them
	else:
		# ~ print( "else" )
		start()


# -----------------------------------------------------------------------
if __name__ == "__main__":
	main()




