from setuptools import setup, find_packages

setup(
    name='textinator',
    description='A command line image viewer',
    version='0.1.0',

    author='Daan Rijks',
    autor_email='daanrijks@gmail.com',

    license='MIT',

    packages=find_packages(),
    install_requires=[
        'click>=3.3, <4',
        'Pillow>=2.6.1, <3',
        'ansi>=0.1.2, <1'
    ],
    entry_points='''
        [console_scripts]
        textinator=textinator:textinator
    '''
)
