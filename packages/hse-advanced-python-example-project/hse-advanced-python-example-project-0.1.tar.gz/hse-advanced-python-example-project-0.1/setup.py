from setuptools import setup, find_packages


setup(
    name='hse-advanced-python-example-project',
    version='0.1',
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
