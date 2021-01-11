from setuptools import setup, find_packages

setup(
    name='qing-sdk',
    version='0.4',
    py_modules=['command'],
    packages=[''],
    include_package_data=True,
    install_requires=[
        'click==7.1.2',
        'requests==2.25.1'
    ],
    entry_points='''
        [console_scripts]
        qing=command:cli
    '''

)
