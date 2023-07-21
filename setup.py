from setuptools import setup, find_packages

setup(name='parse_medpc_file',
      license='MIT',
      version='1.0',
      description='Python Module for parsing MED-PC data files',
      author='Patrick Walsh',
      author_email='patrick.walsh@barquest.us',
      url='https://github.com/pw42020/Mouse-data-processing-pipeline',
      packages=find_packages(),
      package_dir={'file_parser': 'file_parser'},
      install_requires=['scipy==1.11.1'],
     )