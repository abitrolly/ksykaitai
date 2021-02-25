#!/bin/bash

set -e
set -x

#pip wheel .

#pip install build

# remove build dir, because it looks like `setuptools`
# caches files there and can pack stuff already removed
rm -rf build/
rm -rf dist/

python -m build
# for debugging
#python -m build --no-isolation

# get the latest built wheel
# https://stackoverflow.com/questions/5885934/bash-function-to-find-newest-file-matching-pattern
unset -v latest
for file in dist/*.whl; do
  [[ $file -nt $latest ]] && latest=$file
done

echo "$latest"
