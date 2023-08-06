from setuptools import setup, find_packages


setup(
    name='skyml',
    version='0.1',
    author="Zongheng Yang",
    author_email='zongheng.y@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='example project',
)
