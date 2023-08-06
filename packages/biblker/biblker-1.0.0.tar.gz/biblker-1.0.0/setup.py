from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='biblker',
  version='1.0.0',
  description='dev test biblker',
  long_description=open('README.rst').read(),
  url='',  
  author='Kerso87',
  author_email='kerso8877@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='biblker',
  packages=find_packages(),
  install_requires=[] 
)