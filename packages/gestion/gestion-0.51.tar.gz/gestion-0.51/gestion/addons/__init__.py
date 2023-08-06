import os
import sys

# ~ from modules import config
# ~ from modules import database
# ~ from modules import web
from modules import tasks
from modules import cli
# ~ from modules import node


#-----------------------------------------------------------------------
__all__ = []


#-----------------------------------------------------------------------
for item in os.listdir( os.path.split( __file__ )[0] ):
	if item[0] not in ["_", "."]:
		file_name, extension = os.path.splitext( item )
		if extension == ".py":
			__all__.append( file_name )
			

#-----------------------------------------------------------------------
from . import *
LOADED = None


#-----------------------------------------------------------------------
def available_addons():
	return [ item for item in LOADED.keys() ]

	
def list_addons():
	print( "#" * 32 )
	print( "Available addon(s):" )
	for item in available_addons():
		print( item )
	print( "#" * 32 )


cli.add_command( list_addons )


#-----------------------------------------------------------------------
def load():
	loaded = {}
	for item in __all__:
		imp = getattr( sys.modules[ __name__ ],  item )
		for item in dir( imp ):
			obj = getattr( imp, item )
			try:
				if isinstance( obj, tasks.Addon ):
					loaded[ obj.func_name ] = obj
			except Exception as e:
				tasks.write_to_log( str( e ) )
	
	setattr(  sys.modules[ __name__ ],  "LOADED", loaded )


#-----------------------------------------------------------------------
def get_addon( name ):
	if name in available_addons():
		return LOADED[ name ]
	else:
		tasks.write_to_log( "No addon found with name: %s" % name )


load()
