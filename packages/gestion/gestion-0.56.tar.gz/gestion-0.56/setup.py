import setuptools
# ~ https://python-packaging.readthedocs.io/en/latest/non-code-files.html

#-----------------------------------------------------------------------
with open("README.md", "r") as fh:
	long_description = fh.read()


#-----------------------------------------------------------------------
setuptools.setup(
	name							= "gestion",
	version							= 0.56,
	url								= "https://github.com/hurgar-nl/gestion.git",
	author							= "Arno de Grijs",
	author_email					= "info@hurgar.nl",
	description						= "Simple project automation manager",
	long_description 				= long_description,
	long_description_content_type 	= "text/markdown",
	packages 						= [ "gestion", "gestion.modules", "gestion.addons" ],
	install_requires 				= [ "click==8.0.1", "Flask==2.0.1", "itsdangerous==2.0.1", "Jinja2==3.0.1", "MarkupSafe==2.0.1", "psutil==5.8.0", "pymongo==3.12.0", "Werkzeug==2.0.1" ],
	include_package_data			= True,
	classifiers						=[
										"Programming Language :: Python :: 3",
										"License :: OSI Approved :: MIT License",
										"Operating System :: OS Independent",
									 ],
 )
