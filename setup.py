from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='prototypes_sample',
    version='0.1.0',
    description='Prototypes Sample package for notalk.tech',
    long_description=readme,
    author='Wallace Huang',
    author_email='h417652303@gmail.com',
    url='https://github.com/kennethreitz/samplemod',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['numpy>=2.1.0']
    tests_require=['pytest>=3.3.1', 'pytest-cov>=2.5.1']
)
