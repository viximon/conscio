#!/bin/bash

VENV_HOME=$WORKSPACE/env/

# Delete previously built virtualenv
if [ -d $VENV_HOME ]; then
    rm -rf $VENV_HOME
fi

# Setup environment
virtualenv --no-site-packages $VENV_HOME
. $VENV_HOME/bin/activate
pip install --quiet -r requirements.txt


# Run code report tools
if [ -d $WORKSPACE/codereport ]; then
    rm -rf $WORKSPACE/codereport
fi
mkdir $WORKSPACE/codereport
nosetests --with-xcoverage --with-xunit --cover-package=approot --cover-erase --xunit-file=$WORKSPACE/codereport/nosetests.xml --xcoverage-file=$WORKSPACE/codereport/coverage.xml
pylint -f parseable approot/ | tee $WORKSPACE/codereport/pylint.txt
