from setuptools import setup, find_packages

setup(
    name="sample etl job",
    packages=find_packages('src/taxi_trips'),
    package_dir={'': 'src'}
)
