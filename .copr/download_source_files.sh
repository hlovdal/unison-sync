#!/bin/bash

set -e

if [ $# -ne 2 ]
then
	echo "Usage: $0 <spec-file> <sources-dir>" >&2
	exit 1
fi

# Version:        1.4.0
VER=$(sed -n '/^Version:\s*/s///p' "$1")
#echo $VER


#Source0:   https://github.com/bcpierce00/unison/archive/v%{version}.tar.gz
#Source1:   http://www.cis.upenn.edu/~bcpierce/unison/download/releases/unison-%{version}/unison-manual.html
for url in \
	$(sed -n "/^Source.*:\s*https:\/\/github.com\/bcpierce00\/unison/{s/%{version}/$VER/g; s/.*https/https/; p}" "$1") \
	$(sed -n "/^Source.*:\s*http:\/\/www.cis.upenn.edu\/~bcpierce\/unison\/download/{s/%{version}/$VER/g; s/.*http/http/; p}" "$1")
do
	pushd "$2"
	curl -Lo $(basename $url) $url
	popd
done
