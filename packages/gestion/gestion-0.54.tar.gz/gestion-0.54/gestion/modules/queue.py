#-----------------------------------------------------------------------
import time


#-----------------------------------------------------------------------
if "." in __name__:
	from modules import config
	from modules import tasks
	from modules import database
	from modules import node
	from modules import web
	from modules import cli
else:
	import config
	import tasks
	import database
	import node
	import web
	import cli


#-----------------------------------------------------------------------
import addons


#-----------------------------------------------------------------------
#
# create queue collection to add to database
# and create functions for datatypes in database
#
#-----------------------------------------------------------------------
def change_status( doc ):
	print( "change_status {doc} " )
	current_status 	= doc[ "status" ]
	new_status 		= doc[ "status" ]

	if current_status == "processing":
		new_status = "kill"
	
	elif current_status in  [ "killed", "done", "error", "ignore" ]:
		new_status = "waiting"
		
	elif current_status in  [ "waiting" ]:
		new_status = "ignore"
	
	if doc[ "status" ] != new_status:
		# ~ coll			= database.get_collection( "queue" )
		doc[ "status" ] = new_status
		queue_collection[ doc._id ] = doc



queue					= database.Blueprint()

status		 			= database.String() #dictionairy, per user status?
status.value			= "waiting"
status.function			= change_status
queue[ "status" ]		= status

queue[ "addon" ]		= database.String()	
queue[ "arguments" ] 	= database.Dictionary()

project 				= database.String()
project.value 			= "default"
queue[ "project" ]		= project

userhost				= database.Userhost()
userhost.hidden			= True
queue[ "userhost" ]		= userhost

queue[ "date" ]			= database.Date()


#-----------------------------------------------------------------------
#
# create log collection to add to database
# and create functions for datatypes in database
#
#-----------------------------------------------------------------------
def as_html( doc ):
	list_length = len( doc["log"] ) 
	if list_length > 1:
		log = "items"
	else:
		log = "item"	

	return f"{list_length} {log}"


log						= database.List()
log.innertext			= as_html
queue[ "log" ]			= log
queue_collection 		= database.create_collection( "queue", queue )


#-----------------------------------------------------------------------
def loop_queue():
	# error checking of tasks in task class
	while True:
		if config.STATUS == True:
			# ~ conn = database.get_collection( "queue" )
			try:
				doc = queue_collection.find_one( status = "waiting" )
					
				if doc:
					doc[ "status" ] 			= "processing"
					queue_collection[ doc._id ]	= doc

					try:
						results 		= process_queued_item( doc )
						log_id			= node.write_to_log( f"Loop_queue: {results}" )
						doc[ "log" ].insert( 0, log_id )

						
					except Exception as e:
						log_id			= node.write_to_log( f"Loop_queue: {str(e)}" )
						doc[ "log" ].insert( 0, log_id )
						doc[ "status" ] 	= "error"
					queue_collection[ doc._id ] = doc
			
			except Exception as e:
				error = str( e )
				print( error )
				node.write_to_log( f"Loop_queue: {error}" )

		else:
			pass
			print( f"Host: {config.HOST} not available for queue." )

		time.sleep( 5 )


#-----------------------------------------------------------------------
def process_queued_item( queued_item ):
	name 	= queued_item[ "addon" ]
	_id		= queued_item._id

	if name in addons.available_addons():
		addon	= addons.LOADED[ name ]
		kwargs	= queued_item[ "arguments" ]
		results = addon.execute( **kwargs )
		
		try:
			while addon.state:
				doc = queue_collection[ _id ]
				if queue_collection[ _id ][ "status" ] == "kill":
					addon.kill()
					results 		= addon.output
					doc[ "status" ] = "killed" 
					queue_collection[ _id ] = doc
				else:
					time.sleep( 1 )
			
			if doc[ "status" ] != "killed":
				doc[ "status" ] = "done"
			queue_collection[ _id ] = doc
			
			return results
		
		except Exception as exc:
			raise( f"Error occured in processing of queued item" )

	

	# ~ else:
		# ~ raise NameError( f"Addon {name} not found, not processing" )
	
	# ~ if addon.output:
		# ~ return addon.output
	# ~ elif addon.error:
		# ~ print( "addon.error" )
		# ~ raise Exception( str( addon.error ) )
	# ~ else:
		# ~ raise( "Cannot get results from addon, has it been killed" )


#-----------------------------------------------------------------------
loop_queue_task		 = tasks.Task( loop_queue )
loop_queue_task.wait = False


#-----------------------------------------------------------------------
def add_to_queue( addon, project = None, **kwargs ):
	print( f"add_to_queue( {addon}, {project}, {kwargs} )" )
	# ~ builtin a check if file and addon exist
	if project is None:
		project = config.PROJECT

	try:
		if addon in addons.available_addons():
			#
			# need a check if all arguments needed for addon are being passed 
			#
			# ~ coll 						= database.get_collection( "queue" )
			doc 						= queue_collection.create_document()
			doc[ "addon" ]				= addon
			doc[ "project" ]		  	= project
			doc[ "arguments" ]		 	= kwargs
			doc[ "log" ].append( node.write_to_log( f"Added {addon} to queue by {config.USER}" ) )
			# ~ print( doc )
			queue_collection.append( doc )


		else:
			raise NameError( f"Addon {addon} not found, ignoring request and not adding to queue" )

	except Exception as e:
		print( str( e ) )
		node.write_to_log( str( e ) )

cli.add_command( add_to_queue )


#-----------------------------------------------------------------------
#
# create queue webpage
#
#-----------------------------------------------------------------------
queue_template 	= web.CollectionTemplate( queue_collection )
queue_page 		= web.Page( "queue", template = queue_template )




