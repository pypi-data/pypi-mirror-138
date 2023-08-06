import time
from modules import web


page = web.Page( "test" )
print( f"Printing routes for {page.name}" )
for route in page:
	print( route )
