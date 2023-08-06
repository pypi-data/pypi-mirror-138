from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='cust',
  version='0.0.1',
  description='Utils',
  url='',  
  author='Miguel Malgarezi',
  author_email='miguelmalgarezi@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='utils', 
  packages=find_packages(),
  install_requires=[''] 
)