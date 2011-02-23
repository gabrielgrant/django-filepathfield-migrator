from setuptools import setup

setup(
    name='django-portfolio-pages',
    version='0.1.0dev',
    author='Gabriel Grant',
    packages=[
        'filepathfield_migrator',
        'filepathfield_migrator.management',
        'filepathfield_migrator.management.commands',
    ],
    license='LGPL',
    long_description=open('README').read(),
    install_requires=[
        'django',
    ],
)

