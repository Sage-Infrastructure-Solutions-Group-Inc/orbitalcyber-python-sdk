from setuptools import setup, find_packages

requires = ['requests']
setup(name='orbitalcyber-sdk',
      version='0.1.0',
      description='This package provides an SDK that can be used to jumpstart projects that interact with the OrbitalCyber API',
      url='https://github.com/Sage-Infrastructure-Solutions-Group-Inc/orbitalcyber-python-sdk',
      author='Rylan Merritt',
      author_email='rmerritt@sageisg.com',
      license='MIT',
      install_requires=requires,
      packages=find_packages(),
      zip_safe=False)