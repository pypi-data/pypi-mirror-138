from setuptools import setup, find_packages


setup(
    name='cooolpackage',
    version='0.2',
    author="Daniel Gabitov",
    author_email='work.gabitov@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/DanielGabitov/hse-2022-python',
    keywords='',
    install_requires=[
          'graphviz',
      ],
)
