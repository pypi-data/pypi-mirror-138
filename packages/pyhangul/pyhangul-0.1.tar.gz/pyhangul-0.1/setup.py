from setuptools import setup, find_packages

setup(
    name                = 'pyhangul',
    version             = '0.1',
    description         = 'cn12',
    author              = 'cn12',
    author_email        = 'gamdragon2@gmail.com',
    url                 = 'https://github.com/CN-12/pyhangul',
    download_url        = 'https://github.com/CN-12/pyhangul',
    install_requires    =  [],
    packages            = find_packages(exclude = []),
    keywords            = ['ccpy'],
    python_requires     = '>=3',
    package_data        = {},
    zip_safe            = False,
    classifiers         = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)