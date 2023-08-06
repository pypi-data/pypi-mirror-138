from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: MacOS ',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='arunsundaram',
  version='0.0.2',
  description='A very basic adder',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Joshua Lowe',
  author_email='arun_co@yahoo.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='adder', 
  packages=find_packages(),
  install_requires=[''] 
)