#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ 'notebook' ]

test_requirements = [ ]

setup(
    author="Akram Zaytar",
    author_email='zaytarakram@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A ChatGPT front-end for Jupyter notebooks (Copilot for Jupyter notebooks).",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='jupyter_plz',
    name='jupyter_plz',
    packages=find_packages(include=['jupyter_plz', 'jupyter_plz.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/akramz/jupyter_plz',
    version='0.1.1',
    zip_safe=False,
)
