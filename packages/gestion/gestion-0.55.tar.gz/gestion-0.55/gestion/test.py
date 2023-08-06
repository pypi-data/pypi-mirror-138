import time
from modules import web
from modules import database


def toggle_status( doc:database.Document ):
	print( doc )
	print( "djkf" )


click 			= web.SimpleClick( "test" )
click.function 	= toggle_status
