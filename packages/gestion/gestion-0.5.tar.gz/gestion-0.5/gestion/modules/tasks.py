import 	os
import 	time
import 	psutil
import 	multiprocessing
from 	multiprocessing import Process
from 	multiprocessing import Queue


#-----------------------------------------------------------------------
if "." in __name__:
	from modules import database
	from modules import web
else:
	import database
	import web


#-----------------------------------------------------------------------
class Proc():
	def __init__( self, func ):
		self.func 	 = func
		self.wait	 = False
		self.daemon	 = False
		self.results = None


	#-------------------------------------------------------------------
	def execute( self, *args, **kwargs ):
		write_to_log( "Starting proces: %s %s" % ( self.func.__name__ , str( kwargs ) ))
		self.queue		= Queue()
		self.queue.put( { "args":args, "kwargs":kwargs } )
		self.proc 		= Process( target = self.wrapped_func )
		self.proc.name	= self.func.__name__
		
		self.proc.daemon = self.daemon
		self.proc.start()

		if self.wait:
			self.proc.join()
		
	
	def kill( self ):
		return self.proc.kill()


	#-------------------------------------------------------------------
	def wrapped_func( self ):
		output 	  = None
		error 	  = None
		arguments = self.queue.get()

		try:
			output = self.func( *arguments[ "args" ], **arguments[ "kwargs" ] )
		except Exception as exc:
			error = str(exc)
		
		self.queue.put( { "output":output, "error":error } )
		# ~ self.get_queue()


	#-------------------------------------------------------------------
	@property
	def output( self ):
		if hasattr( self, "queue" ):
			self.results = self.queue.get()
			delattr( self, "queue" )

		if self.results != None:
			return self.results[ "output" ]
		else:
			return None

			
	@property
	def error( self ):
		print( "error" )
		if hasattr( self, "queue" ):
			self.results = self.queue.get()
			delattr( self, "queue" )

		if self.results != None:
			
			print( "self.results:", self.results )
			return self.results[ "error" ]
		else:
			return None

	
	@property
	def func_name( self ):
		return self.func.__name__


	@property
	def pid(self):
		return self.proc.pid


	@property
	def state(self):
		return self.proc.is_alive()



	@property
	def exitcode( self ):
		return self.proc.exitcode


	@property
	def type(self):
		return self.__class__.__name__.lower()



#-----------------------------------------------------------------------
class Addon( Proc ):
	def __init__( self, func ):
		Proc.__init__( self, func )
		self.daemon = True
		self.wait 	= False


class Task( Proc ):
	def __init__( self, func ):
		Proc.__init__( self, func )
		self.wait	= False


#-----------------------------------------------------------------------
# create collection for log
log 			= database.Blueprint()
log["type"]		= database.String()
log["log"] 		= database.String()
log["userhost"]	= database.Userhost()
log["date"]		= database.Date()
log.set_local( False )

log_collection	= database.create_collection( "log", log )



#-----------------------------------------------------------------------
#
# create webpages
#
#-----------------------------------------------------------------------
log_template 	= web.CollectionTemplate( log_collection )
log_page 		= web.Page( "log", template = log_template )



"""
class task_page( web.SimplePage ):
	def __init__( self ):
		web.SimplePage.__init__( self, "tasks", template = "default"  )
		self.keys = [ "pid" ,"name", "exitcode" ]


	def function( self, *args, **kwargs ):
		# ~ for item in multiprocessing.active_children() :
			# ~ print( dir(item ) )
			# ~ print( item.name, item._parent_name )
		data =  [ p for p in multiprocessing.active_children() ]
		# ~ data = [ proc.info for proc in psutil.process_iter( ["name", "pid"] ) ]
		return web.Template( self.template,  header = self.keys, data = data )
		# ~ self.keys = [ "type", "log" ,"userhost", "date" ]
"""

#-----------------------------------------------------------------------
#
# taskmanager-a-like functions
#
#-----------------------------------------------------------------------
def find_process_by_name( name ):
	results = [ proc.info for proc in psutil.process_iter( ["name", "pid"] ) if name.lower() in proc.info["name"].lower() ]
	return results


#-----------------------------------------------------------------------
def find_process_by_port( port:int ):
	processes = [ psutil.Process(pid=proc.pid) for proc in psutil.net_connections() if proc.laddr.port == port ]
	return processes


#-----------------------------------------------------------------------
def manager():
	while True:
		print("Checking for zombified processes")


#-----------------------------------------------------------------------
def write_to_log( to_log:str ):
	coll 			= database.get_collection( "log" )
	doc		 		= coll.create_document()
	doc[ "log" ]	= to_log
	return coll.append( doc )



#-----------------------------------------------------------------------
# ~ def start():
	# ~ pass


#-----------------------------------------------------------------------
