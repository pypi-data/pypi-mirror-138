#!/usr/bin/bash

name=tsvkit

rm -rf build/ dist/ $name.egg-info/

python setup.py sdist bdist_wheel
twine upload dist/*

rm -rf build/ dist/ $name.egg-info/

echo "pip install -i https://pypi.org/simple -I -U $name"
