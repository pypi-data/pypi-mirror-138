import os
import sys
import time
import shutil
import argparse
from importlib import reload as reload


# -----------------------------------------------------------------------
WORKING_DIR = os.path.split( __file__ )[0]
sys.path.append( WORKING_DIR )


# -----------------------------------------------------------------------
import modules
from modules import config
from modules import cli

if config.is_first_run:
	config.create_file()


print( f"Initializing database" )
from modules import web
web.init( __name__ )

print( "Initializing gestion." )
from modules import database
database.init()

# ~ print( 1 )
from modules import node
# ~ print( 2 )
from modules import tasks
# ~ print( 3 )
from modules import queue
# ~ print( 4 )
from modules import watchfolder
# ~ print( 5 )


#-----------------------------------------------------------------------
def main():
	if config.is_first_run:
		first_run()
		# ~ database.init()
		# ~ print( node.available_projects() )
		if config.PROJECT not in node.available_projects():
			print( "Creating default project, not found in available projects." )
			node.create_project( config.PROJECT, config.PROJECT_ROOT )

	if len( sys.argv ) > 1:
		cli.parse_args_and_execute( sys.argv )
	else:
		start()


# -----------------------------------------------------------------------
def start():
	if not database.database_is_running():
		print( f"Error connecting to database on ip {config.DATABASE_IP}:{config.DATABASE_PORT}" )
		print( "Going to quit gestion" )
		exit()
	
	if config.PROJECT not in node.available_projects():
		print( "creating project , not found in VlVBLE PROJSECT" )
		node.create_project( config.PROJECT, config.PROJECT_ROOT )
	
	node.set_project( config.PROJECT )

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
	import addons
	print( "Loading addons" )
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

	print( f"Connected to database on ip {config.DATABASE_IP}:{config.DATABASE_PORT}" )
	web.start_server()


#-----------------------------------------------------------------------
def first_run():
	# ~ if config.is_first_run:
	print( f"First run, creating gestion config folder: {config.GESTION_FOLDER}" )
	# ~ default = os.path.join( config.GESTION_FOLDER, "default" )
	if not os.path.exists( config.GESTION_FOLDER ):
		os.makedirs( config.GESTION_FOLDER )
	
	for folder in [ "static", "templates", "default" ]:
		src = os.path.join( WORKING_DIR, "template", folder )
		dst = os.path.join( config.GESTION_FOLDER, folder )
		print( f"Copying: {src} -> {dst}" )
		shutil.copytree( src, dst, dirs_exist_ok = True )
	
	config.create_file()
	# ~ node.create_project( "default", default )

#-----------------------------------------------------------------------
def set_env( **kwargs ):
	for key in kwargs.keys():
		setattr( config, key.upper(), kwargs[key] )
	
	config.save_to_file()

cli.add_command( set_env )


# -----------------------------------------------------------------------
if __name__ == "__main__":
	main()




