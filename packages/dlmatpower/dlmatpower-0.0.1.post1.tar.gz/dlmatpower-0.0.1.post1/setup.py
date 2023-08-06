from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop

import os
import re

import urllib
import shutil

PACKAGE_NAME = 'dlmatpower'
current_path = os.path.abspath(os.path.dirname(__file__))
version_line = open(os.path.join(current_path, PACKAGE_NAME, 'version.py'), "rt").read()

m = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_line, re.M)
__version__ = m.group(1)

def post_install():
    matpower_version = '7.1'
    matpower_dir = 'dlmatpower'
    file_name = os.path.join(matpower_dir, "matpower.zip")
    
    if os.path.exists(file_name):
        print("matpower.zip already exist in destionation.")
        shutil.rmtree(file_name)
    
    matpower_url = "https://github.com/MATPOWER/matpower/archive/refs/tags/" + matpower_version + ".zip"

    print("Downloading MATPOWER...")
    print(matpower_url)
    urllib.request.urlretrieve(matpower_url, file_name) # source, dest

    shutil.unpack_archive(file_name, matpower_dir, 'zip')
    
    os.remove(file_name) # remove zipfile
    
    default_matpower_dir = os.path.join(matpower_dir,'matpower-' + matpower_version)

    renamed_name = os.path.join(matpower_dir,'matpower')
    if os.path.exists(renamed_name):
        print("Matpower folder already exist in path")
        shutil.rmtree(renamed_name)

    os.rename(default_matpower_dir, renamed_name)
    print(f"matpower saved on {renamed_name}")

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        post_install()

class CustomDevelopCommand(develop):
    def run(self):
        develop.run(self)
        post_install()

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = PACKAGE_NAME,
    version = __version__, # versions '0.0.x' are unstable and subject to refactor
    author = "Muhammad Yasirroni",
    author_email = "muhammadyasirroni@gmail.com",
    description = "Make download MATPOWER easier from pip",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://gitlab.com/yasirroni/dlmatpower",
    package_data = {},
    classifiers = [
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering"
    ],
    cmdclass = {
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
        },
    packages = [PACKAGE_NAME]
)



