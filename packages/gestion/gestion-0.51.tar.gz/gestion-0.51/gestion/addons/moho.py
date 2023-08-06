import os, json, zipfile

#-----------------------------------------------------------------------
class Layer( dict ):
	def __init__(self, layer, parent=None):
		dict.__init__( self )
		self.parent = parent

		for key in layer.keys():
			self[key] = layer[key]

#-----------------------------------------------------------------------#
class File( object ):
	def __init__( self, path, as_json = True ):
		self.as_json 	= as_json
		self.root 		= {}
		self.path 		= path
		self.tmp_path 	= os.path.split( path )[0]
		self.extension 	= os.path.splitext( path )[1]

		try:
			with zipfile.ZipFile( path, "r" ) as z:
				z.extractall( self.tmp_path )
		except:
			raise ValueError("Cannot extract moho file: %s" % path)

		if as_json:
			self.JSON_to_DICT()
			self.layers 		= self.get_layers()
			self.grouplayers 	=	 self.get_grouplayers()
		else:
			self.as_string 		= self.open_file()

	#-----------------------------------------------------------------------#
	def zipfile_info(self):
		info = {}

		contents 	= [ "Project.%sproj" % self.extension.replace( ".",  "" ), "preview.jpg" ]
		z 			= zipfile.ZipFile( self.path )
		try:
			for item in contents:
				info[ item ] = z.getinfo( item )
		except:
			pass
		return info

	#-----------------------------------------------------------------------#
	def find(self, key):
		for key in self.root.keys():
			print(key)

	#-----------------------------------------------------------------------#
	def pretty_print(self):
		return json.dumps(self.root, indent=4, sort_keys=True)

	#-----------------------------------------------------------------------#
	def open_file(self):
		with open(os.path.join(self.tmp_path, "Project.%sproj" % self.extension.replace(".",  ""))) as f:
			contents = f.read()
		return contents

	#-----------------------------------------------------------------------#
	def replace_in_file(self, _from, _to):
		newstring = self.as_string.replace(_from, _to)
		self.root = json.loads(newstring.decode('utf-8'))

	#-----------------------------------------------------------------------#
	def JSON_to_DICT(self):
		self.root = json.loads( self.open_file() )

	#-----------------------------------------------------------------------#
	def get_layers(self):
		return return_layers(self.root)

	def get_styles(self):
		return self.root["styles"]

	def get_grouplayers(self):
		return return_layergroups(self.root)

	def get_imagelayers(self, recursive=True):
		return return_imagelayers(self.root, recursive=recursive)

	def get_file_info(self):
		return self.decoded.keys()

	@property
	def project_data(self):
		return self.root["project_data"]
	
	@property
	def start_frame(self):
		return self.root["project_data"]["start_frame"]
	
	@start_frame.setter
	def start_frame(self, frame):
		self.root["project_data"]["start_frame"]=frame
	
	@property
	def end_frame(self):
		return self.root["project_data"]["end_frame"]
		
	@end_frame.setter
	def end_frame(self, frame):
		self.root["project_data"]["end_frame"]=frame

	@property
	def fps(self):
		return self.root["project_data"]["fps"]
		
	@fps.setter
	def fps(self, fps):
		self.root["project_data"]["fps"]=fps

	def write_changes(self):
		with open(os.path.join(self.tmp_path, "Project.%sproj" % self.extension.replace(".",  "")), "w") as f:
			f.write(json.dumps(self.root))

	def save(self, path):
		newextension = os.path.splitext(path)[1]
		print("Project.%sproj" % newextension.replace(".",  ""))
		print(os.path.join(self.tmp_path, "Project.%sproj" % self.extension.replace(".",  "")))

		self.write_changes()

		with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as f:
			f.write(os.path.join(self.tmp_path, "Project.%sproj" % self.extension.replace(".",  "")), "Project.%sproj" % newextension.replace(".",  ""))
			f.write(os.path.join(self.tmp_path,"preview.jpg"), "preview.jpg")

	def replace_psd(self):
		pass

#-----------------------------------------------------------------------#
def return_layers(root, recursive=True):
	if not recursive:
		return iter_layers(root)
	else:
		return iter_layers(root, return_type="imagelayer")

def return_layergroups(root):
	return [layer for layer in return_layers(root) if layer["type"].lower()=="grouplayer"]

def return_imagelayers(root, recursive=True):
	return [layer for layer in return_layers(root, recursive=recursive) if layer["type"].lower()=="imagelayer"]

#-----------------------------------------------------------------------#
def versioned_file(path):
	_path, _extension = os.path.splitext(path)
	_path, _file = os.path.split(_path)
	current_version=_file.split("_")[-2]
	_author = _file.split("_")[-1]
	_file="_".join(_file.split("_")[:-2])

	string_list=[]
	int_list=[]

	string_len=len(current_version)
	for i in range(string_len):
		try:
			int(current_version[i])
			int_list.append(current_version[i])

		except:
			string_list.append(current_version[i])

	new_version=int(current_version[len(string_list):])+1
	vString="".join(string_list)+("%0"+str(len(int_list))+"d")%new_version
	
	newfile= os.path.join(_path, (_file+"_"+vString+"_"+_author+_extension))
	return newfile


#-----------------------------------------------------------------------#
def as_string(layer):
	psdkeys=[]

	psdkeys=[key for key in layer.keys() if "psd" in key]
	ss="%s: %s:" + "\n%s "*len(psdkeys)
	allkeys=["name",  "image_path"]+psdkeys

	return ss % (tuple(layer[key] for key in allkeys))


#-----------------------------------------------------------------------#
def iter_layers(root, return_type="layers", layers=[], reset=False ):
	if reset:
		layers=[]

	if hasattr(root, "root"):
		root = root.root

	for layer in root["layers"]:
		if layer["type"].lower()==return_type:
			layers.append(layer)

		elif "layers" in layer.keys():
			iter_layers(layer, return_type=return_type, layers=layers)

	return layers


#-----------------------------------------------------------------------#
def return_psd_layers(root):
	layers=[]
	for layer in iter_layers(root, return_type="imagelayer", reset=True):
		if "psd_layer" in layer.keys():
			layers.append(layer)

	return layers


#-----------------------------------------------------------------------#
def rgb_to_float(rgb, as_string=False):
	new_r=round( (rgb[0]/255.0), 6)
	new_g=round( (rgb[1]/255.0), 6)
	new_b=round( (rgb[2]/255.0), 6)
	if as_string:
		return '{"r":%s,"g":%s,"b":%s,"a":1.0}' % (new_r, new_g, new_b)
	else:
		return {"a":1.0, "r":new_r, "g":new_g, "b":new_b}


#-----------------------------------------------------------------------#
def get_last_version(path):
	mod_time={}
	for _f in os.listdir(path):
		if os.path.splitext(os.path.join(path, _f))[1] == ".anime":
			mod_time[os.path.getctime(os.path.join(path, _f))]=os.path.join(path, _f)

	try:
		return mod_time[sorted(mod_time.keys())[-1]]
	except:
		return None

