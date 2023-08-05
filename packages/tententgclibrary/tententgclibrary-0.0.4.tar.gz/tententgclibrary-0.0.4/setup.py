from setuptools import setup, find_packages

classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]

setup(
    long_description_content_type='text/plain',
    name='tententgclibrary',
    version='0.0.4',
    description='Mathematics calculate library',    
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Thanyapisit Buaprakhong',
    author_email='thanyapisit.bua@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='tententgc',
    packages=find_packages(),
    install_requires=['']
)
