import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bzmicrostitcher",
    version="0.1.5",
    author="Cory Poole",
    author_email="cory_poole@urmc.rochester.edu",
    description="A package to stitch microscope images.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LungWizard/BZMicroStitcher",
    project_urls={
        "Bug Tracker": "https://github.com/LungWizard/BZMicroStitcher/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
	
	install_requires = [
    'numpy>=1.22.1',
    'scipy>=1.7.3',
    'tifffile>=2021.11.2',
    'pyside2==5.15.1',
	'shiboken2==5.15.1',
	'pyglet==1.4.10',
	'stitch2d>=1.0',
	'tk==0.1.0',
	'opencv-contrib-python==4.5.5.62',
	'ome-types==0.2.4',
	'datetime==4.3',
	'openpyxl==3.0.9',
	'pillow==9.0.0'
]

)