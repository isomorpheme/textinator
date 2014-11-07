from setuptools import setup

setup(
    name='textinator',
    description='A command line image viewer',
    version='0.1.0',

    author='Daan Rijks',
    autor_email='daanrijks@gmail.com',

    license='MIT',

    py_modules=['convertinator'],
    install_requires=[
        'click>=3.3, <4',
        'Pillow>=2.6.1, <3',
        'ansi>=0.1.2, <1'
    ],
    entry_points='''
        [console_scripts]
        textinate=textinator:convert
    '''
)
