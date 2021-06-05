from setuptools import setup, find_packages
setup(name='transformstorm',
      version='0.1.7',
      packages = find_packages(),
      description='A command line interface for playing with language models',
      url='https://github.com/simonmnash/transformstorm',
      author='Simon Nash',
      license='MIT',
      install_requires=['transformers', 'torch', 'click'],
      scripts=["bin/transformstorm"]
      )