#-----------------------------------------------------------------------
import os
import sys
import time
import inspect
import builtins

from flask import Flask
from flask import Response
from flask import stream_with_context
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import json
from markupsafe import Markup


#-----------------------------------------------------------------------
routes_to_be_created 	= []
server 					= None


#-----------------------------------------------------------------------
if "." in __name__:
	from modules import config
	from modules import database
else:
	import config
	import database


#-----------------------------------------------------------------------
def init( name ):
	setattr( sys.modules[ __name__ ], "server", Flask( name, static_folder = config.STATIC_FOLDER, template_folder = config.TEMPLATE_FOLDER ) ) # static folder default in home static


#-----------------------------------------------------------------------
def start_server( debug = True, use_reloader = False ):
	threaded = False
	server.run( debug = debug, host = config.WEB_IP, port = config.WEB_PORT, threaded = threaded, use_reloader = use_reloader )


#-----------------------------------------------------------------------
#
#	template classes
#
#-----------------------------------------------------------------------
class Template():
	def __init__( self, html_template ):
		self.html_template	= html_template
		self.header			= []


	@property
	def html_template( self ):
		return self._html_file


	@html_template.setter
	def html_template( self, name ):
		self._html_file = f"{name}.html"


	def render_page( self, *args, **kwargs ):
		return render_template( self.html_template, header = self.header, *args, **kwargs )


#-----------------------------------------------------------------------
class DefaultTemplate( Template ):
	def __init__( self ):
		Template. __init__( self, "default" )


#-----------------------------------------------------------------------
class CollectionTemplate( Template ):
	if "." in __name__:
		from modules import database
	else:
		import database


	def __init__( self, collection:database.Collection ):
		Template. __init__( self, "default" )
		self.collection = collection
		self.header		= collection.blueprint.keys( ignore=[ "id", "hidden", "saved" ] )


	def return_page( self, *args, **kwargs ):
		# aanpassen naar return_page ?
		return render_template( self.html_template, header = self.header, **kwargs )


#-----------------------------------------------------------------------
class Redirect( Template ):
	def __init__( self ):
		self.url = None


	def return_page( self ):
		return url_for( "/%s" % self.url )


#-----------------------------------------------------------------------
class Referrer( Template ):
	def __init__( self ):
		pass


	def return_page( self ):
		return redirect(  request.referrer )


#-----------------------------------------------------------------------
def collection_function():
	print( request.referrer )


#-----------------------------------------------------------------------
class Page( list ):
	def __init__( self, route:str, template = DefaultTemplate(), methods = [ "GET" ] ):
		list.__init__( self, [ route ] )
		# ~ self.module		= None
		self.methods	= methods
		self.template	= template
 
 
	def __iter__( self ):
		# replace '.' with '_" or '/' or delete?
		for item in list.__iter__( self ):
			if item.startswith("/"):
				yield item
			else:
				yield f"/{item}"


	@property
	def name( self ):
		return list.__getitem__(self, 0 )


	@property
	def template( self ):
		return self._template


	@template.setter
	def template( self, template ):
		if issubclass( template.__class__, Template ):
			self._template = template
		else:
			raise Exception( f"Error in {self.__class__.__name__}: Need a class subclassed from a Template, not a {template.__class__.__name__}" ) 


	@property
	def methods( self ):
		return self._methods


	@methods.setter
	def methods( self, methods:list = [], *args ):
		if not hasattr( self, "_methods" ):
			self._methods = []

		methods.extend( args )
		for method in methods:
			if method not in self._methods:
				self._methods.append( method )
				
	
	@property
	def function( self ):
		# function expcets a function, but this isn ot the case, so need anther name?
		if hasattr( self, "_function" ):
			return self._function
		else:
			return None


	@function.setter
	def function( self, func ):
		if callable( func ):
			self._func_parser( func )
			self._function = func
		else:
			raise ValueError( f"Need a function, not a {type(func)}" )


	def _func_parser( self, func ):
		pass


	def wrapper_function( self, *args, **kwargs ):
		start 	= time.time()
		if self.function:
			results	= self.function( *args, **kwargs )
		else:
			if issubclass( self.template.__class__, CollectionTemplate ):
				results = self.collection_wrapper_function( *args, **kwargs )
			else:
				results = f"Rendering page: {self.name}"
		end 	= time.time()

		return self.template.render_page( data = results, page = self, config = config )
	
	#---------------------------------------------------------------
	#
	# speciale class maken voor collection
	# met deze function, voor het overzicht
	#
	#---------------------------------------------------------------
	def collection_wrapper_function( self, *args, **kwargs ):
		# perhaps check for collection_function
		referrer 	= request.referrer
		root 		= request.url_root
		args 		= request.args

		if "sort" in args:
			key 	= args.get( "sort" )
			sort	= -1

			if referrer != None:
				old_args = referrer[len(root):]
				if key in old_args:
					if self.template.collection._sort[1] == -1:
						sort = 1
			self.template.collection._sort = ( key, sort )

		return self.template.collection.find_in_cache( **kwargs )


#-----------------------------------------------------------------------
class SimpleClick( Page ):
	def __init__( self, route, *args, **kwargs ):
		Page.__init__( self, route, *args, **kwargs )
		self.needs_document		= False
		self.needs_collection	= False
		self.is_filter			= False
		# ~ self.needs_id			= False


	def _func_parser( self, func ):
		has_document = False
		sig = inspect.signature( func)
		for parameter in sig.parameters:
			if issubclass( sig.parameters[parameter].annotation, database.Document ):
				self.needs_document = True
				break


	def wrapper_function( self, *args, **kwargs ):
		# ~ from modules import database
		# ~ if 
		# ~ print( "id in  request.args", ("id" in  request.args) )
		if self.needs_document:
			# ~ print( "needs a document" )
			if "id" in request.args:
				_id 	= request.args.get( "id" )

			if  "db" in request.args:
				_db 	= request.args.get( "db" )

			if _id	!= None and _db != None:
				coll 	= database.get_collection( _db )
				doc 	= coll[ database.ObjectId( _id ) ] 
				results = self.function( doc )


		elif self.needs_collection:
			_db 	= request.args.get( "db" )
		# ~ elif _db != None:
			results = self.function( _db, *args, **kwargs )
		
		else:
			results = self.function( *args, **kwargs )
		
		return redirect( request.referrer )


#-----------------------------------------------------------------------\
#
# helper functions
#
#-----------------------------------------------------------------------
def create_route( page ):
	
	if server == None:
		raise Exception( "The server has not yet been initialized!" )
	else:
		# mss de naam veranderen in create_route, page is meer met een template.
		if issubclass( page.__class__, Page ):
			try:
				func_name = f"{page.name}_function"
				for route in page:
					# ~ if issubclass( page.__class__, SimpleClick ):
						# ~ if page.needs_colection:
							# ~ route = f"{route}?db={}" 
					server.add_url_rule( route, func_name, page.wrapper_function, methods = page.methods )
					server.view_functions[ route ] = page.wrapper_function
					print( "Created route(s) for:\t%s " % route )

			except Exception as e:
				print( "Error creating route(s) for: %s " % page.name )
				print( str( e ) )

