import pathlib
import re
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

re_version = r'__version__ = \"([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})\"'
_version = re.search(re_version, (HERE / "mangadex_downloader/__init__.py").read_text())

if _version is None:
  raise RuntimeError("Version is not set")

version = _version.group(1)

requirements = []
with open('./requirements.txt', 'r') as r:
  requirements = r.read().splitlines()

requirements_docs = []
with open('./requirements-docs.txt', 'r') as r:
  requirements_docs = r.read().splitlines()

extras_require = {
  'docs': requirements_docs
}

setup(
  name = 'mangadex-downloader',         
  packages = ['mangadex_downloader'],   
  version = version,
  license='MIT',     
  description = 'Download manga from Mangadex through Python',
  long_description= README,
  long_description_content_type= 'text/markdown',
  author = 'Rahman Yusuf',              
  author_email = 'danipart4@gmail.com',
  url = 'https://github.com/mansuf/mangadex-downloader',  
  download_url = 'https://github.com/mansuf/mangadex-downloader/archive/%s.tar.gz' % (version),
  keywords = ['mangadex'], 
  install_requires=requirements,
  extras_require=extras_require,
  entry_points = {
    'console_scripts': [
      'mangadex-downloader=mangadex_downloader.__main__:main',
      'mangadex-dl=mangadex_downloader.__main__:main'
    ]
  },
  classifiers=[
    'Development Status :: 5 - Production/Stable',  
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
  ],
  python_requires='>=3.5'
)
