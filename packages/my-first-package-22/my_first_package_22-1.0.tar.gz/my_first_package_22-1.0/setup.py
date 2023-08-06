
import setuptools

setuptools.setup(name="my_first_package_22",
                 version="1.0",
                 long_description=(open("README.md").read()),
                 packages=setuptools.find_packages(exclude=["tests", "data"])
                 )
