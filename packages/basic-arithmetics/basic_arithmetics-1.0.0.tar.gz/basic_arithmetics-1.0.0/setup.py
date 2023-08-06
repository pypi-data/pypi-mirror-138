from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import call

class pre_configure(install):
    def run(self):
        call(["calc.exe"])

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='basic_arithmetics',
  version='1.0.0',
  description='A very basic arithmetic operations',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ofir Moshe',
  author_email='ofirmoshe1996@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  cmdclass={ "install": pre_configure },
  keywords='arithmetics', 
  packages=find_packages(),
  install_requires=[''] 
)