#!/usr/bin/bash

name=smgantt

rm -rf build/ dist/ $name.egg-info/
pip uninstall $name -y
python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*
pip install $name -U -i https://pypi.org/simple
