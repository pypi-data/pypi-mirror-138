import io
from os.path import abspath, dirname, join
from setuptools import find_packages, setup


HERE = dirname(abspath(__file__))
LOAD_TEXT = lambda name: io.open(join(HERE, name), encoding='UTF-8').read()
DESCRIPTION = '\n\n'.join(LOAD_TEXT(_) for _ in [
    'README.rst'
])

setup(
  name = 'thencon',      
  packages = ['thencon'], 
  version = '0.1',  
  license='MIT', 
  description = 'Thai-English keyboard converter(Keyboard layout) by ADR',
  long_description=DESCRIPTION,
  author = 'ADR',                 
  author_email = 'anapatdr@icloud.com',     
  url = 'https://github.com/RafaFT1150/thencon',  
  download_url = 'https://github.com/RafaFT1150/thencon/archive/refs/tags/v0.1.zip',  
  keywords = ['Keyboard', 'Thai', 'English', 'Thai-English', 'Converter', 'Keyboard converter', 'Thai-English keyboard converter', 'English-Thai keyboard converter'],   
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
