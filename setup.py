from setuptools import setup

setup(name='HDS',
    version='0.1',
    description='Testing installation of Package',
    url='#',
    author='CF',
    author_email='CF@gmail.com',
    license='HDS',
    packages=['HDS'],
    install_requires=[
        'adafruit_ads1x15','mysql.connector','RPi.GPIO'
    ],
zip_safe=False)
