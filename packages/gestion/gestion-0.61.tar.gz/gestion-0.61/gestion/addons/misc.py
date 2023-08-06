#-----------------------------------------------------------------------
import time
import subprocess
import os
import shutil
import re
# ~ import moho 

#-----------------------------------------------------------------------
# ~ import config
# ~ config.load()

#-----------------------------------------------------------------------
# ~ from modules import addon
# ~ from modules import gestion


#-----------------------------------------------------------------------
def removeVersion(path):
	pattern= r"_[vV]\d*_"
	
	base, head = os.path.split(path)
	filename ,extension= os.path.splitext(head)

	results=re.search( pattern, filename )
	
	if results:
		match = results.group()
		result = filename.split(match)[0]
	else:
		result = filename
		
	return result


#-----------------------------------------------------------------------
def Test(path, end, start):
	print("*"*16)
	print(path)
	print(end)
	print(start)
	print("*"*16)


#-----------------------------------------------------------------------
# ~ test=addon.Addon()
# ~ test.set_function(Test)


#-----------------------------------------------------------------------
def GetShotsFolder(path):
	found=None
	while path:
		path=os.path.split(path)[0]
		if "shots" == os.path.split( path )[1].lower():
			found=path
			break
	
	return found
	
#-----------------------------------------------------------------------
def replace_server_path(path):
	results = []
	previous_root = None
	root = path

	while root and root != previous_root:
		previous_root = root
		root, tip = os.path.split(root)
		results.insert(0, tip)

	if "Club Baboo" in results:
		index = results.index("Club Baboo")
		new_path = os.path.join( "Y:", *results[index:])
	else:
		new_path = path
	
	return new_path

#-----------------------------------------------------------------------# command line opties voor moho
# http://www.lostmarble.com/forum/viewtopic.php?t=1318
#-----------------------------------------------------------------------
def replace_images_in_file(path):
	m = moho.MOHO(path)
	new_path = path
	is_changed=False

	new_base = None
	
	for layer in m.get_imagelayers(recursive=True):
		oldpath = layer["image_path"]
		newpath = layer["image_path"]
		
		
		if "megagamma" in oldpath.lower():
			splitted = oldpath.lower().split("megagamma")
			start = len(oldpath)-len(splitted[-1])
			newpath = "Y:"+  oldpath[start:]
			
		
		elif "meggamma" in oldpath.lower():
			splitted = oldpath.lower().split("meggamma")
			start = len(oldpath)-len(splitted[-1])
			newpath = "Y:"+  oldpath[start:]
		
		elif "omicron" in oldpath.lower():
			splitted = oldpath.lower().split("omicron")
			start = len(oldpath)-len(splitted[-1])
			newpath = "Z:"+  oldpath[start:]
		

		if oldpath != newpath:
			is_changed = True
			layer["image_path"] = newpath
			layer["image_fileref"]["path"]= newpath
	
	# save to a local folder to keep the server clean
	_dir, _file = os.path.split(path)
	base, ext = os.path.splitext(_file)
	new_file_name = base + "_RENDER" + ext
	
	render_folder = os.path.join(config.HOME, "gestion", "renderfiles")
	if not os.path.exists(render_folder):
		os.makedirs(render_folder)
	
	new_path = os.path.join(render_folder, new_file_name)

	m.save(new_path)
	return new_path
		
	

#-----------------------------------------------------------------------
def Render(file, start=None, end=None, project=None, replace_paths=True):
	from modules import client
	local_file=client.map_to_client(file)
	renderer=client.get_renderer("moho")
	
	if os.path.exists(local_file):
		if renderer!=None:
			print( "Found Moho executable: ", renderer)
			print( "Going to render file: ", local_file)		

			# check for missing image files within moho file
			new_file=replace_images_in_file(local_file)

			cli=[renderer]
			cli.append("-r")
			cli.append(new_file)
			cli.append("-f")
			cli.append("PNG")
			
			if start!=None:
				cli.append("-start")
				cli.append(str(start))
			if end!=None:
				cli.append("-end")
				cli.append(str(end))

			
			print("Project: ", project)
			
			workspace = client.get_project(project)
			print(workspace)
			local_root="Y:\Club Baboo"		
			print("local_root: ", local_root)	

			outputdir=removeVersion(file)
			outputpath=os.path.normpath(os.path.join(local_root, workspace["images"], outputdir, "%s" % outputdir))
			
			if not os.path.exists(os.path.split(outputpath)[0]):
				os.makedirs(os.path.split(outputpath)[0])

			cli.append("-o")
			cli.append(outputpath)
			
			proc=subprocess.Popen( cli, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True )
			print(proc.stderr.readlines())
			if proc.returncode != 0:
				print( "Error rendering %s " % file )
				return False
			else:
				return True

		# ~ else:
			# ~ print("No moho renderer found, skipping")
			# ~ raise ValueError( "No moho renderer found, skipping"  )
		
		#time.sleep(5)

		print("*"*16)
		return True

#-----------------------------------------------------------------------
# ~ render=addon.Addon()
# ~ render.set_function(Render)

# ~ print(replace_server_path("/volumes/megagamma/Club Baboo/SHANGHAI_ACROSSMEDIA_ART/Marketing Material/20210601_PromoArt/"))
# ~ print( replace_images_in_file("/volumes/megagamma/Club Baboo/SHOTS/MagicShow/MS16_Rubberboot/Shots/061_VeloSprong/MS16_061_VeloSprong_v016_L.moho"))



