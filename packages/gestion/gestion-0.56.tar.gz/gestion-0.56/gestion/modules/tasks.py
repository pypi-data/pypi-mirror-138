import 	os
import 	time
import 	psutil
import 	multiprocessing
from 	multiprocessing import Process
from 	multiprocessing import Queue


#-----------------------------------------------------------------------
if "." in __name__:
	from modules import config
	from modules import database
	from modules import web
else:
	import config
	import database
	import web


#-----------------------------------------------------------------------
class Results( object ):
	def __init__( self ):
		self.output = None
		self.error 	= None


#-----------------------------------------------------------------------
class Proc():
	def __init__( self, func ):
		self.func 	 = func
		self.wait	 = False
		self.daemon	 = False
		self.results = None


	#-------------------------------------------------------------------
	def execute( self, *args, **kwargs ):
		if "." in __name__:
			from modules import node
	
		else:
			import node

		node.write_to_log( "Starting proces: %s %s" % ( self.func.__name__ , str( kwargs ) ))
		self.queue		= Queue()
		self.queue.put( { "args":args, "kwargs":kwargs } )
		self.proc 		= Process( target = self.wrapped_func )
		self.proc.name	= self.func.__name__
		
		self.proc.daemon = self.daemon
		self.proc.start()

		if self.wait:
			self.proc.join()
		
	
	def kill( self ):
		proc = psutil.Process( self.pid )
		children = proc.children( recursive=True )
		for child in children:
			child.kill()

		self.proc.terminate()
		if not self.wait:
			self.proc.join()
		self.queue.put( { "output":f"Process killed by user {config.USER}", "error":None } )


	#-------------------------------------------------------------------
	def wrapped_func( self ):
		output 	  = None
		error 	  = None
		arguments = self.queue.get()
		try:
			output = self.func( *arguments[ "args" ], **arguments[ "kwargs" ] )
		except Exception as exc:
			# ~ if f"Process killed by user {config.USER}" in str(exc):
				# ~ output = str(exc)
			# ~ else:
			error = str(exc)
		self.queue.put( { "output":output, "error":error } )



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
# ~ def start():
	# ~ pass


#-----------------------------------------------------------------------
