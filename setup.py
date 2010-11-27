import os
from setuptools import setup, find_packages

from songkick import get_version


readme_copy = open(os.path.join(os.path.dirname(__file__), 
                                'README.rst')).read()

setup(
    name='python-songkick',
    version=get_version(),
    description='Songkick API wrapper',
    long_description=readme_copy,
    author='Matt Dennewitz',
    author_email='mattdennewitz@gmail.com',
    url='http://github.com/mattdennewitz/python-songkick/tree/master',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
