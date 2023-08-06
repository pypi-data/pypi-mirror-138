from setuptools import setup

with open("Readme.md" , "r") as fh:
    long_description = fh.read()



setup(
    name = "cpptopy",
    version = '0.0.1' ,
    description = 'Runs a cpp program written as a triplequoted string inside python' ,
    py_modules = ["cpptopy"],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    package_dir ={'':'cpptopy'}

    )
    
