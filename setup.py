from setuptools import setup, find_packages

setup(
    name='mdds',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/yourusername/mdds',
    license='MIT',
    author='Your Name',
    author_email='youremail@example.com',
    description='A multi-dimensional data structures package',
    install_requires=[
        'numpy',
        'scipy',
        # add any other dependencies here
    ],
)