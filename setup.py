try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    "description": "NOAA buoy data in pandas",
    "author":"Conner Hoy",
    "version":"0.1",
    "install_requires":["pandas","requests","json","pymongo"],
    "packages":["buoyreader"],
    "scripts":[],
    "name":"buoyreader"
}
setup(**config)
