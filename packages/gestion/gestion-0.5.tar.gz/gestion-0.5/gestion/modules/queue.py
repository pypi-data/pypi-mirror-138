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
def change_status( doc ):
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


#-----------------------------------------------------------------------
# add collection to database
#
#-----------------------------------------------------------------------
queue					= database.Blueprint()

status		 			= database.String() #dictionairy, per user status
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


def as_html( doc ):
	list_length = len( doc["log"] ) 
	if list_length > 1:
		log = "items"
	else:
		log = "item"	

	return f"{list_length} {log}"


log						= database.List()
log.html				= as_html
queue[ "log" ]			= log

queue_collection 		= database.Collection.create_from_blueprint( "queue", queue )








#-----------------------------------------------------------------------
def loop_queue():
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
						doc[ "status" ]	= "done"
						log_id			= tasks.write_to_log( f"loop_queue: {results.output}" )
						doc[ "log" ].insert( 0, log_id )
						
					except Exception as e:
						log_id			= tasks.write_to_log( f"LOOP_QUEUE: {str(e)}" )
						doc[ "log" ].insert( 0, log_id )
						doc["status"] 	= "error"

					queue_collection[ doc._id ] = doc

			except Exception as e:
				error = str( e )
				print( error )
				tasks.write_to_log( f"loop_queue: {error}" )

		else:
			pass
			# ~ print( f"Host: {config.HOST} not available for queue." )
		time.sleep( 5 )


#-----------------------------------------------------------------------
def process_queued_item( queued_item ):
	# ~ conn 	= database.get_collection( "queue" )
	name 	= queued_item[ "addon" ]
	_id		= queued_item._id

	if name in addons.available_addons():
		addon	= addons.LOADED[ name ]
		kwargs	= queued_item[ "arguments" ]
		addon.execute( **kwargs )

		while addon.state:
			doc = queue_collection[ _id ]
			if queue_collection[ _id ][ "status" ] == "kill":
				print( addon.kill() )
			else:
				time.sleep( 1 )
	else:
		raise NameError( f"Addon {name} not found, not processing" )

	if addon.output:
		return addon.output
	elif addon.error:
		raise Exception( str( addon.error ) )


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
			doc[ "log" ].append( tasks.write_to_log( f"Added {addon} to queue by {config.USER}" ) )
			# ~ print( doc )
			queue_collection.append( doc )


		else:
			raise NameError( f"Addon {addon} not found, ignoring request and not adding to queue" )

	except Exception as e:
		print( str( e ) )
		tasks.write_to_log( str( e ) )

cli.add_command( add_to_queue )


#-----------------------------------------------------------------------
#
# create queue webpage
#
#-----------------------------------------------------------------------
queue_template 	= web.CollectionTemplate( queue_collection )
queue_page 		= web.Page( "queue", template = queue_template )




