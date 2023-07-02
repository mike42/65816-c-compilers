#!/bin/bash
# install-calypsi-6502.sh: Download & install Calypsi C compiler (6502 target).
set -exu -o pipefail

if [ "$EUID" -ne 0 ]
  then echo "This script requires root to run."
  exit
fi

export CALYPSI_VERSION="4.4"

# download and install calypsi 6502
wget "https://github.com/hth313/Calypsi-tool-chains/releases/download/${CALYPSI_VERSION}/calypsi-6502-${CALYPSI_VERSION}.deb" -O "/tmp/calypsi-6502-${CALYPSI_VERSION}.deb"
dpkg -i "/tmp/calypsi-6502-${CALYPSI_VERSION}.deb"
rm "/tmp/calypsi-6502-${CALYPSI_VERSION}.deb"

/usr/local/bin/cc6502 --version

