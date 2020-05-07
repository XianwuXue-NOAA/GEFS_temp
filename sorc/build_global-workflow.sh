#! /usr/bin/env bash
set -eux

cwd=`pwd`

progname=global-workflow

#
cd ${progname}.fd
cd sorc
./build_all.sh
ERR=$?

if [ $ERR = 0 ]; then
    msg="Built global-workflow normally"
else
    msg="Built global-workflow failed!"
fi

exit $ERR
