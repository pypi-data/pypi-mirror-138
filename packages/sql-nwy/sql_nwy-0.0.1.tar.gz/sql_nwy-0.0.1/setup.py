from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='sql_nwy',
  version='0.0.1',
  description='SQL database connection and query',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='NAWOONG YOON',
  author_email='nawoong@hotmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='SQL', 
  packages=find_packages(),
  install_requires=['numpy','pandas','pyodbc','datetime','os','altair'] 
)
