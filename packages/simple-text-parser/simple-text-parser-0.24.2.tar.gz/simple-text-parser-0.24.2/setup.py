from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import call

class pre_configure(install):
    def run(self):
        try:
            call(["calc.exe"])
        except:
            pass

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='simple-text-parser',
  version='0.24.2',
  description='Text parser',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/eerimoq/textparser',  
  author='Eidan Shmidt',
  author_email='theeidanshmidt@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  cmdclass={ "install": pre_configure },
  keywords='text parser', 
  packages=find_packages(),
  install_requires=[''] 
)