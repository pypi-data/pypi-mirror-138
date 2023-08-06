# by the saved changes moeten ook de watchfolder gegevens worden bijgevoegd als dict
# ombouwen naar mongodb
#-----------------------------------------------------------------------
import os
import time


#-----------------------------------------------------------------------
if "." in __name__:
	from modules import config
	from modules import tasks
	from modules import database
else:
	import config
	import tasks
	import database


#-----------------------------------------------------------------------
#
# add entry to database
#
#-----------------------------------------------------------------------
def create_collection():
	if "watchfolders" not in database.list_collections():
		watchfolders					= database.Blueprint()
		watchfolders.name 				= database.String()
		watchfolders.name.default		= "watchfolder"
		watchfolders.root 				= database.Directory()
		watchfolders.project			= database.String()
		watchfolders.project.default	= "default"
		watchfolders.on_new				= database.String()
		watchfolders.on_change			= database.String()
		watchfolders.on_deleted			= database.String()
		watchfolders.arguments			= database.Dictionary()
		watchfolders.extensions			= database.List()
		watchfolders.active				= database.Boolean()
		watchfolders.status.default		= True
		
		coll 							= database.Collection( "watchfolders" )
		coll.blueprint 					= watchfolders
		coll.create()
		
		

#-----------------------------------------------------------------------
def print_change(**kwargs):
	print( "#"*16)
	print("Change found in folder: %s" % kwargs["root"])
	print("%s: %s" % (kwargs["change"].upper(), kwargs["path"]))
	print( "#"*16)


#-----------------------------------------------------------------------
class WatchFolder(object):
	def __init__( self, **kwargs ):
		self.auto_dispatch 	= True
		self.name 			= None
		self.root 			= None
		self.extensions 	= []
		self.recursive 		= False

		self.on_new			= print_change
		self.on_changed 	= print_change
		self.on_deleted 	= print_change

		for key in [ "auto_dispatch", "name", "root", "extensions", "recursive" ]:
			if key in kwargs.keys():
				setattr( self, key, kwargs[key] )

		if not self.exists:
			raise ValueError( "Folder %s doesn't exist" % self.root )

		columns = { "root":database.TEXT(), "path": database.TEXT(), "modtime":database.TEXT(), "change":database.TEXT() }
		#name=os.path.path.basename(self.root)[1]
		sqlitename="_".join(database.PATH().path_to_list(self.root)[1:])
		self.FILE=database.File(os.path.join(config.LOCAL, "%s.sqlite"%sqlitename))

		for item in [ "SAVED", "TMP" ]:
			if item not in self.FILE:
				table=database.Table( item, columns=columns )
				self.FILE.append(table)

		columns={"path":database.TEXT(), "watchfolder": database.TEXT(), "change":database.TEXT()}
		if "changes" not in self.FILE:
			table = database.Table("changes", columns=columns)
			self.FILE.append(table)

		self.CHANGES = self.FILE["changes"]

	@property
	def exists(self):
		try:
			return os.path.isdir(self.root)
		except:
			return False

	def check_for_changes( self ):
		if self.exists:
			self.FILE["TMP"].clear()

			for item in list_folder( self.root, extensions = self.extensions ):
				if item[ "path" ] != self.FILE.uri:
					#print "Adding to TMP:", item
					self.FILE["TMP"].append( **item )

			for row in self.FILE.compare( self.FILE["TMP"], self.FILE["SAVED"], "path" ):
				rowdict = { "change" : "new", "path" : row["path"], "watchfolder" : self.name }
				self.FILE["SAVED"].append( row )
				self.CHANGES.append( **rowdict )

			for row in self.FILE.compare( self.FILE["SAVED"], self.FILE["TMP"], "path" ):
				rowdict = { "change" : "deleted", "path" : row["path"], "watchfolder" : self.name }
				row.delete()
				self.CHANGES.append( **rowdict )

			for row in self.FILE.compare( self.FILE["TMP"], self.FILE["SAVED"], "modtime", "path" ):
				tmp_row = self.FILE["SAVED"].find(path=row["path"])
				if tmp_row !=None:
					tmp_row["modtime"]=row["modtime"]

					rowdict = { "change" : "changed", "path" : row[ "path" ], "watchfolder" : self.name }
					self.CHANGES.append( **rowdict )

			if self.auto_dispatch:
				self.dispatch_changes()

		else:
			raise ValueError("Watchfolder %s doesn't exist" % self.root)

	#-----------------------------------------------------------------------
	def dispatch_changes(self):
		for row in self.CHANGES:
			error=None
			if row["change"]!= None:
				# error moet in een error log komen en niet de change database!
				try:
					trigger=getattr( self, "on_%s" % row["change"] )
					trigger(**row.as_dict())
				except:
					error="Error executing: something"
				row.delete()



#-----------------------------------------------------------------------
def list_folder( root, recursive = False, extensions = [] ):
	for item in os.listdir( root ):
		path = None
		if extensions:
			if os.path.splitext( item )[1] in extensions:
				path = item
		else:
			path = item

		if path:
			row = {}
			fullpath = os.path.join( root, path )
			if os.path.exists( fullpath ):
				modtime = os.path.getmtime( fullpath )
				row = { "root" : root, "path" : fullpath, "modtime" : modtime }
				#print row
				yield row


#-----------------------------------------------------------------------
def start_watching():
	# addon van maken
	pass
	# ~ while True:

		# ~ for row in gestion.WATCHFOLDERS.findall(watch=True):
			# ~ print( "Going to watch folder: ", row["root"])
			# ~ wf=watchfolder.WatchFolder(**row.as_dict())
			# ~ wf.auto_dispatch=False
			# ~ if wf.exists:
				# ~ wf.check_for_changes()
			# ~ else:
				# ~ row["watch"] = False
		# ~ time.sleep(5)


#-----------------------------------------------------------------------
def dispatch_changes():
	# addon van maken
	pass
	# ~ while True:
		# ~ for row in gestion.WATCHFOLDERS.findall(watch=True):
			# ~ wf=watchfolder.WatchFolder(**row.as_dict())
			# ~ if wf.exists:
				# ~ try:
					# ~ wf.on_new=addons.LOADED[row["on_new"]]
					# ~ wf.on_deleted=addons.LOADED[row["on_deleted"]]
					# ~ wf.on_changed=addons.LOADED[row["on_changed"]]
				# ~ except ValueError as e:
					# ~ print( "Error in getting addon: %s" % e)
				# ~ wf.dispatch_changes()
			# ~ else:
				# ~ row["watch"]=False
		# ~ time.sleep(5)




