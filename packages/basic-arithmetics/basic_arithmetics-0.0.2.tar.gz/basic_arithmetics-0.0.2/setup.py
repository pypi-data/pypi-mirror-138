from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='basic_arithmetics',
  version='0.0.2',
  description='A very basic arithmetic operations',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ofir Moshe',
  author_email='ofirmoshe1996@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='arithmetics', 
  packages=find_packages(),
  install_requires=[''] 
)