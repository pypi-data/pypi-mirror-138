from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Other OS',
    'Topic :: System :: Hardware :: Hardware Drivers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='python-PCF8574',
    version='1.0.0',
    description=" TI's PCF8574 python driver ",
    long_description= long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/goutamkumar77/python-PCF8574',
    author='Goutam Kumar',
    author_email='goutam1000@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='PCF8574',
    packages=find_packages(),
    install_requires=['smbus2']
)