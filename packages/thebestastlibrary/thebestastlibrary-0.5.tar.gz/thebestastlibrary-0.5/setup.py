from setuptools import setup

setup(
    name='thebestastlibrary',
    version='0.05',
    description='Library for vizualizing ast.',
    author='Evgeniia Kirillova',
    author_email='grindevald666@gmail.com',
    license_files = ('LICENSE',),
    url='https://github.com/JaneKirillova/advanced-python/tree/main/hw_1',
    packages=['thebestastlibrary'],
    install_requires=[
        "networkx==2.5.1",
        "pydot==1.4.2"
    ],
)
