from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()
setup(name='confpars', version='0.1.1', author='Lior Bass', author_email='mail@liorbass.dev',
      install_requires=required, scripts=['conf_parser'], url='https://github.com/liorbass/confpars')
