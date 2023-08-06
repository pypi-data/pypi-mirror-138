#
#    x2c - XML to CSV Conversion
#    Copyright (C) 2022  Martin Valter
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#



from setuptools import setup, find_packages
from io import open
from os import path
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

# with open('./x2c/requirements.txt', encoding='utf-8') as f:
#     all_reqs = f.read().split('\n')

# install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
#     not x.startswith('#')) and (not x.startswith('-'))]
# dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
#                     if 'git+' not in x]
setup (
 name = 'x2c',
 description = 'A simple cli app to convert XML files to CSV, with user-defined columns.',
 version = '1.0.0',
 packages = ['x2c'], # list of all packages
 install_requires = [
     'pandas',
 ],
 python_requires='>=3',
 entry_points='''
        [console_scripts]
        x2c=x2c.cmd:convert
    ''',
 author="Martin Valter",
 long_description=README,
 long_description_content_type="text/markdown",
 license='GPLv3+',
 url='https://github.com/slonki/x2c',
 download_url='',   
 author_email='martin@circo.dev',
 classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ]
)