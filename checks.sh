#!/usr/bin/env bash
echo 'ISORT'
isort --filter-files qrand

echo 'MYPY' 
mypy --scripts-are-modules --ignore-missing-imports --warn-unused-ignores --warn-redundant-casts --warn-return-any --warn-unreachable qrand

echo 'BLACK' 
black qrand

echo 'FLAKE8' 
flake8 qrand
