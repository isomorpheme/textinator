from setuptools import setup

setup(
    name='textinator',
    version='0.1.0',
    py_modules=['convertinator'],
    install_requires=[
        'Click',
        'Pillow'
    ],
    entry_points='''
        [console_scripts]
        textinate=textinator:convert
    '''
)
