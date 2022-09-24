#!/bin/bash

set -e

if [ $# -ne 2 ]
then
	echo "Usage: $0 <spec-file> <outdir>" >&2
	exit 1
fi

echo "%_topdir" $(pwd) > .rpmmacros
env HOME=$(pwd) rpmbuild -bs "$1"
mv SRPMS/* "$2"
