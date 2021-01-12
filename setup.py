from setuptools import setup
from os import path
from entropeer import VERSION


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='entropeer',
    version=VERSION,
    url='https://github.com/TheZ3ro/entropeer',
    # GitHub releases in format "X.Y"
    download_url='https://github.com/TheZ3ro/entropeer/archive/' + VERSION + '.tar.gz',
    license='LGPLv3',
    author='TheZero',
    author_email='io@thezero.org',
    description='Searches through files and directories for high entropy strings and secrets. ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='entropy, secrets, grep, recursive',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Security'
    ],
    packages=['entropeer'],
    entry_points={
        'console_scripts': [
            'entropeer = entropeer.__main__:main'
        ]
    },
    include_package_data=True,
    install_requires=[
        'colorama',
    ],
)
