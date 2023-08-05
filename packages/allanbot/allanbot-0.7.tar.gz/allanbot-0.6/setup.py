
from setuptools import setup, find_packages


setup(
    name='allanbot',
    version='0.6',
    license='MIT',
    author="Allan W",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/memfall/allanbot',
    keywords='allanbot memrise memfall cheat hack client',
    install_requires=[
          'webbot',
      ],

)
