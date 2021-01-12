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
    # GitHub releases in format "entropeer-X.Y"
    download_url='https://github.com/TheZ3ro/entropeer/archive/entropeer-' + VERSION + '.tar.gz',
    license='MIT',
    author='TheZero',
    author_email='io@thezero.org',
    description='entropeer is ...',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='...',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: LGPLv3 License',
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
        'colorama'
    ],
)
