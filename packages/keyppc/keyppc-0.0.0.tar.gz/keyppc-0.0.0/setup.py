import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()
setuptools.setup(
	name="keyppc",
	version="0.0.0",
	author="Keywind",
	author_email="kevinwater127@gmail.com",
	description="A simple library to bind your mouse and keyboard.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/keyywind/keyppc",
	project_urls={
		"Bug Tracker": "https://github.com/keyywind/keyppc/issues",
	},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	package_dir={"": "src"},
	packages=setuptools.find_packages(where="src"),
	python_requires=">=3.7",
	
	install_requires=[
		'markdown',
		'keyscraper',
		'pynput',
		'opencv-python',
		'keygim'
	]
)