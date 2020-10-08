#!/bin/bash

pip wheel .

# get the latest built wheel
# https://stackoverflow.com/questions/5885934/bash-function-to-find-newest-file-matching-pattern
unset -v latest
for file in *.whl; do
  [[ $file -nt $latest ]] && latest=$file
done

echo "$latest"
