#!/usr/bin/env python
import pathlib

from setuptools import setup, find_packages

import signalboard


def read_req_file(file_name):
    path = pathlib.Path(__file__).parent.joinpath(file_name)
    with path.open() as fp:
        requires = (line.strip() for line in fp)
        return [req for req in requires if req and not req.startswith("#") and not req.startswith('-')]


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

install_requires = read_req_file("requirements_install.txt")
tests_require = install_requires + read_req_file("requirements.txt")

setup(
    author=signalboard.__author__,
    author_email=signalboard.__email__,
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Board for River library",
    entry_points={
        'console_scripts': [
            'signalboard=signalboard.cli:main',
        ],
    },
    install_requires=install_requires,
    license="BSD license",
    # long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='signalboard',
    name='signalboard',
    packages=find_packages(include=['signalboard', 'signalboard.*']),
    test_suite='tests',
    tests_require=tests_require,
    url='https://github.com/sylwekczmil/signalboard',
    version=signalboard.__version__,
    zip_safe=False,
)
