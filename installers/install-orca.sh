#!/bin/bash
# install-orca.sh: Install the ORCA/C compiler and related tools.
# This script requires 'Golden Gate.msi' and 'ByteWorks' to be in the current directory.
set -exu -o pipefail

if [ "$EUID" -ne 0 ]
  then echo "This script requires root to run."
  exit
fi

# Set up WINE prefix
WINEARCH=win64 WINEPREFIX="/opt/goldengate/" wine64 wineboot

# Install 'Golden Gate.msi' via msiexec
WINEARCH=win64 WINEPREFIX="/opt/goldengate/" wine64 msiexec /i "Golden Gate.msi"

# Extract Opus tools inc. ORCA with helper
WINEARCH=win64 WINEPREFIX="/opt/goldengate/" wine64 "/opt/goldengate/drive_c/Program Files (x86)/GoldenGate/opus-extractor.exe" ByteWorks

# Output a wine wrapper script
echo -e '#!/bin/bash\nset -x\nWINEPREFIX="/opt/goldengate/" WINEARCH=win64 wine64 "/opt/goldengate/drive_c/Program Files (x86)/GoldenGate/iix.exe" $@' > /usr/local/bin/iix
chmod +x /usr/local/bin/iix

# Run it once to confirm it is ok - if something is wrong then 'empty.sym' and 'empty.sym:AFP_AfpInfo' will not be created.
echo '' > /tmp/empty.c
/usr/local/bin/iix compile /tmp/empty.c
rm /tmp/empty.c /tmp/empty.sym /tmp/empty.sym:AFP_AfpInfo

# Ensure wineserver is no longer running - socket files confuse Docker
pgrep --exact wineserver64 && killall --wait --exact wineserver64 || true
