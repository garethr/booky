from setuptools import setup, find_packages

setup(
    name = "booky",
    version = "0.1",
    
    packages = find_packages('src'),
    package_dir = {'':'src'},
    scripts = ['src/booky/bin/booky'],
)