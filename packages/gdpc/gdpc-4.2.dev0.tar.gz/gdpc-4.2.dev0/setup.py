"""The repository setup file."""

from setuptools import setup

setup(name='gdpc',
      version='4.2_dev',
      description='The Generative Design Python Client is a Python-based '
      + 'interface for the Minecraft HTTP Interface mod.\n'
      + 'It was created for use in the '
      + 'Generative Design in Minecraft Competition.',
      url='http://github.com/nilsgawlik/gdmc_http_client_python',
      author='Blinkenlights',
      author_email='blinkenlights@pm.me',
      license='MIT',
      packages=['gdpc'],
      zip_safe=False)
