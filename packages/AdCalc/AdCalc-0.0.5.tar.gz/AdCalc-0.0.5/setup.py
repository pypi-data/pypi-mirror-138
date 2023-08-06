from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='AdCalc',
    version='0.0.5',
    description='AdCalc (Advanced calculator), A python module has some ready functions to use in math.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',  
    author='Ali Hasan',
    author_email='ah7915523@gmail.com',
    license='MIT', 
    classifiers=classifiers,
    keywords='calculator', 
    packages=find_packages(),
    install_requires=[''] 
)
