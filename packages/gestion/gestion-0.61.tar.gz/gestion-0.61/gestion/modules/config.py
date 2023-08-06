import os
import sys
import inspect
from socket import gethostname
from getpass import getuser
from configparser import ConfigParser

#-----------------------------------------------------------------------
#
# config based functions and periphelia
#
#-----------------------------------------------------------------------
GESTION_FOLDER_NAME = "gestion_dev"
GESTION_DB_NAME		= "gestion_dev_db000124"
GESTION_WEB_PORT	= 5001
DEFAULT_STATUS		= ["online", "local", "offline" ]	 # voor later gebruik
DEFAULT_STATUS		= False
NODE_TYPE			= [ "client", "master" ] 			# voor later gebruikt
NODE_TYPE			= "client"


#-----------------------------------------------------------------------
defaults = 	{
				"_user" 			: getuser(),
				"_host" 			: gethostname().split( "." )[ 0 ],
				"_home" 			: os.path.expanduser( "~" ),
				"_gestion_folder"	: os.path.join( os.path.expanduser( "~" ), GESTION_FOLDER_NAME ),
				"_template_folder"	: os.path.join( os.path.expanduser( "~" ), GESTION_FOLDER_NAME, "templates" ),
				"_static_folder"	: os.path.join( os.path.expanduser( "~" ), GESTION_FOLDER_NAME, "static" ),
				"_config_file"		: os.path.join( os.path.expanduser( "~" ), GESTION_FOLDER_NAME, "config.ini" ),
				"database_ip" 		: "127.0.0.1", 
				"database_port"		: 27017,
				"web_ip" 			: "127.0.0.1",
				"web_port" 			: GESTION_WEB_PORT,
				"node_type"			: NODE_TYPE,
				"project"			: "default",
				"project_root"		: os.path.join(os.path.expanduser( "~" ), GESTION_FOLDER_NAME, "default" ),
				"_workspace"		: {},
				"gestion_db"		: GESTION_DB_NAME,
				"status"			: DEFAULT_STATUS,
				"_first_run"		: True
			}


#-----------------------------------------------------------------------
class Config( dict ):
	def __init__( self ):
		dict.__init__( self, defaults )
		self.FILE = self.pop( "_config_file" )

		if self.file_exists:
			self.load_from_file()
		
		
	def __getattr__( self, key ):
		env 	= None
		
		if "_" + key.lower() in self.keys():
			env = "_" + key.lower()
		elif key.lower() in self.keys():
			env = key.lower()
		
		if env:
			inst 		= defaults[ env ]
			value		= self[ env ]
			if type( inst ) == type( value ):
				return value
			else: 
				if type( inst ) == bool:
					if self[ env ].lower() == "false":
						attr_as_type = False
					else:
						attr_as_type = True
				else:
					attr_as_type = type( inst )( self[ env ] )
				return attr_as_type
		else:
			return self.__dict__[ key ]


	def __setattr__( self, key, value ):
		env 	= None
		
		if key.lower() in self.keys():
			env = key.lower()
		
		elif "_" + key.lower() in self.keys():
			env = "_" + key.lower()

		if env:
			self[ env ] = value
		else:
			dict.__setattr__( self, key, value )


	def __setitem__( self, key, value ):
		dict.__setitem__( self, key, value )
		if self.file_exists:
			self.save_to_file()
		
		
	def __getitem__( self, key ):
		if self.file_exists:
			self.load_from_file()
		return dict.__getitem__( self,  key )
		
	
	@property
	def file_exists( self ):
		return os.path.exists( self.FILE )
		

	# ~ @property
	# ~ def is_first_run( self ):
		# ~ return self.first_run


	def create_file( self ):
		if not os.path.exists( os.path.split( self.FILE )[ 0 ] ):
			os.makedirs( os.path.split( self.FILE )[ 0 ] )
		self.save_to_file()
		
		
	def save_to_file( self ):
		kwargs = {}
		for key in [ key for key in dict.keys( self ) if not key.startswith("_") ]:
			kwargs[ key ] = dict.__getitem__( self, key )

		configparser 				= ConfigParser()
		configparser[ "global" ] 	= kwargs
		
		with open( self.FILE, 'w' ) as f:
			configparser.write( f )

		
	def load_from_file( self ):
		configparser = ConfigParser()
		configparser.read( self.FILE )
		self.update( **configparser[ "global" ] )
		# ~ print( self )
		# ~ print(dict.__getitem__( self, "status" ) )
		# ~ print( type(defaults["status"])( dict.__getitem__( self, "status" ) ) )


	def reset( self, hard_reset = True ):
		pass


#-----------------------------------------------------------------------
config = Config()
sys.modules[__name__] = config






