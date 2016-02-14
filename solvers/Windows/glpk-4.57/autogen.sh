#!/bin/sh

test -f configure.ac || {
  echo "Please, run this script in the top level project directory."
  exit
}

libtoolize --copy
aclocal -I m4
autoconf
autoheader
automake --add-missing --copy

echo "For installation instructions, please, refer to file INSTALL."
