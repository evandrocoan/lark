#! /usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import sublime_api

except ImportError:
    import re
    from setuptools import setup

    #
    # Release process setup see:
    # https://github.com/pypa/twine
    #
    # Run pip install --user keyring
    #
    # Run on cmd.exe and then type your password when prompted
    # keyring set https://upload.pypi.org/legacy/ your-username
    #
    # Run this to build the `dist/PACKAGE_NAME-xxx.tar.gz` file
    #     rm -r ./dist && python setup.py sdist
    #
    # Run this to build & upload it to `pypi`, type addons_zz when prompted.
    #     twine upload dist/*
    #
    # All in one command:
    #     rm -rf ./dist && python3 setup.py sdist && twine upload dist/* && rm -rf ./dist
    #
    __version__ ,= re.findall('__version__ = "(.*)"', open('source/pushdown/__init__.py').read())

    setup(
        name = "pushdown",
        version = __version__,
        package_dir = {
            '': 'source'
        },
        packages = ['pushdown', 'pushdown.parsers', 'pushdown.tools', 'pushdown.grammars'],

        # To install use: pip install -e .[full]
        # To install use: pip install -e debug_tools[full]
        # To install use: pip install -e debug_tools debug_tools[full]
        requires = [],
        install_requires = [],
        extras_require = {
            'debug':  ["debug_tools"]
        },

        package_data = { '': ['*.md', '*.lark'] },

        test_suite = 'tests.__main__',

        # metadata for upload to PyPI
        author = "Erez Shinan, Evandro Coan",
        author_email = "erezshin@gmail.com",
        description = "A fork form lark-parser, a modern parsing library",
        license = "MIT",
        keywords = "Earley LALR parser parsing ast",
        url = "https://github.com/evandrocoan/pushdown",
        download_url = "https://github.com/evandrocoan/pushdown/archive/master.zip",
        long_description = open('README.md').read(),
        long_description_content_type='text/markdown',
        classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            'Environment :: Console',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            "Topic :: Text Processing :: General",
            "Topic :: Text Processing :: Linguistic",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "License :: OSI Approved :: MIT License",
            'Operating System :: OS Independent',
        ],
    )

