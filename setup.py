import codecs
import os
import re
from setuptools import setup, find_packages


def read(*parts):
    return codecs.open(os.path.join(os.path.dirname(__file__), *parts)).read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='python-songkick',
    version=find_version('songkick', '__init__.py'),
    description='Songkick API wrapper',
    long_description=read('README.rst'),
    author='Matt Dennewitz',
    author_email='mattdennewitz@gmail.com',
    url='http://github.com/mattdennewitz/python-songkick/tree/master',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
    install_requires=['httplib2>=0.7.4'],
)
