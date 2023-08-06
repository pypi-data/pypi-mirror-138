from distutils.core import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')
setup(
  name = 'ht_getter',  
  packages = ['ht_getter'], 
  version = '0.0.1', 
  license='apache-2.0',
  description = "Searches a document for hash tags. Supports multiple natural languages. Works in various contexts.",
  author = 'Rairye', 
  url = 'https://github.com/Rairye/ht-getter',   
  download_url = 'https://github.com/Rairye/ht-getter/archive/refs/tags/v0.0.1.tar.gz',
  keywords = ['hash', 'tag', 'hash-tags'],
  long_description=long_description,
  long_description_content_type='text/markdown',

  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License', 
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
