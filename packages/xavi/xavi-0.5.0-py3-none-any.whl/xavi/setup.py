
#from distutils.core import setup
from setuptools import setup
setup(
  name = 'xavi',
  packages = ['xavi'], # this must be the same as the name above
  version = '0.5.0',
  description = 'A collection of commonly used Python methods',
  author = 'Xavier Wattermann',
  author_email = 'xwattermann@gmail.com',
  url = 'https://github.com/XavierWattermann/common', # use the URL to the github repo
  download_url = 'https://github.com/XavierWattermann/common/archive/0.5.tar.gz', # I'll explain this in a second
  keywords = ['testing', 'debugging', 'common'], # arbitrary keywords
  classifiers = [],
)

"""
Steps:
1) Create a tag on GritLab -- git tag <version>; git push origin --tags
2) Update this file; change version, update download_url

"""
