from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Propelwise Modules'
LONG_DESCRIPTION = 'description'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name='p_mod_api', 
        version=VERSION,
        author="Krushnaa R",
        author_email="<youremail@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        license='Apache License Version 2.0, January 2004',
        install_requires=['SimpleITK','torchio',
"unet",
"monai==0.6.0",
"pillow",
"sklearn",
"matplotlib",
"torchcam",
"torchvision",
"imageio",
"numpy",
"scipy",
"nibabel",
"dicom2nifti", 
"pydicom",
"tqdm" ], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'numpy'
        
        keywords=['propelwise'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)