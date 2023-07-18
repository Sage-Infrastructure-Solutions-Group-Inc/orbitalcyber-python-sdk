from setuptools import setup, find_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
requires = ['requests']
setup(name='orbitalcyber-sdk',
      version='0.1.2',
      description='This package provides an SDK that can be used to jumpstart projects that interact with the OrbitalCyber API',
      url='https://github.com/Sage-Infrastructure-Solutions-Group-Inc/orbitalcyber-python-sdk',
      author='Rylan Merritt',
      author_email='rmerritt@sageisg.com',
      license='MIT',
      install_requires=requires,
      packages=find_packages(),
      zip_safe=False,
      long_description=long_description,
      long_description_content_type='text/markdown'
      )