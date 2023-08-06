import subprocess

from modules import config
from modules import node
from modules import tasks

#-----------------------------------------------------------------------
from . import moho

#-----------------------------------------------------------------------
#
# Switches for renderling moho
#
#-----------------------------------------------------------------------
"""
Moho -r CS10_001_Dinosaur_v020_L.moho -o Renders/CS10_001_Dinosaur/CS10_001_Dinosaur.png -f png -start 1 -end 2800 -halfsize no -multithread no -extrasmooth yes
Moho -r CS10_001_Dinosaur_v020_L.moho -o Renders/CS10_001_Dinosaur/CS10_001_Dinosaur.png -f png -start 1 -end 2800 -halfsize no -multithread no -extrasmooth yes -layercomp AllComps -createfolderforlayercomp yes -addlayercompsuffix yes
"""

#-----------------------------------------------------------------------
def render( file, start = 1, end = 25, multithread = True, halfsize = False, f = "png", extrasmooth = True, layercomp = False ):
	software 	= node.get_software( "moho" )
	choice 		= { False : "no", True : "yes" }
	output 		= "/nog/te/bepalen"


	if software != None:
		cli = 			[ 	software,
							"-r", 			file,
							"-o", 			output,
							"-f", 			f,
							"-start",		start,
							"-end",			end,
							"-halfsize", 	choice[ halfsize ],
							"-multithread",	choice[ multithread ],
							"-extrasmooth", choice[ extrasmooth ],
						]
			
		if bool( layercomp ) == True:

			cli.extend( [ 	"-layercomp", "AllComp",
							"-createfolderforlayercomp", choice[ True ],
							"-addlayercompsuffix", choice[ True ],
						] )
						
		proc = subprocess.Popen( cli )
		proc.wait()
	
	else:
		raise ValueError( "Cannot find path to moho executable" )
		

#-----------------------------------------------------------------------
#
# check if moho software is available, if so than create addon
#
#-----------------------------------------------------------------------
if "moho" in node.available_software():
	mohorender_addon = tasks.Addon( render )
	mohorender_addon.wait = True

# ~ mohorender_addon = tasks.Addon( render )
# ~ mohorender_addon.wait = True

