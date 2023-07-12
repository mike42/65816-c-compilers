#!/bin/bash
# install-mpw.sh: Install the Macintosh Programmer's Workshop (MPW) IIgs tools.
# This script requires 'MPW IIgs.sit' to be in the current directory.
set -exu -o pipefail

if [ "$EUID" -ne 0 ]
  then echo "This script requires root to run."
  exit
fi

# Install darling, runtime environment for OS X applications (runs on Linux)
wget --quiet "https://github.com/darlinghq/darling/releases/download/v0.1.20220704/darling_0.1.20220704.focal_amd64.deb" -O "/tmp/darling.focal_amd64.deb"
dpkg -i /tmp/darling.focal_amd64.deb

# Install MPW emulator, a runtime environment for Mac 68K applications (runs on Mac OS X)
wget --quiet "https://github.com/ksherlock/mpw/releases/download/r-0.8.3/mpw.0.83.zip" -O "/tmp/mpw.0.83.zip"
unzip /tmp/mpw.0.83.zip -d /opt/mpw_emu/
rm "/tmp/mpw.0.83.zip"

# TODO this script is not yet complete.
#  Need to extract 'MPW IIgs.sit', set up ~/mpw/ directory
# find /opt/mpw_emu/
# which unar
# unar -output-directory /tmp/mpw "MPW IIgs.sit"
# find /tmp/mpw/
