import subprocess


from modules import node
from modules import tasks


def open_file( file ):
	app = node.get_software( name = "filebrowser" )
	if app != None:
		cli = app
		print( cli, file )
		proc = subprocess.Popen( [ cli, file ] )
		proc.wait()
	else:
		raise ValueError( f"Cannot find {app}. If it is installed, add it to the available software" ) 


imageviewer_addon = tasks.Addon( open_file )
imageviewer_addon.wait = False
