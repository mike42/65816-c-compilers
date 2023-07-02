#!/bin/bash
# install-wdc816cc.sh: Install the C compiler from WDC tools (65816 target). 
# This script requires WDCTOOLS.exe to be in the current directory.
set -exu -o pipefail

if [ "$EUID" -ne 0 ]
  then echo "This script requires root to run."
  exit
fi

# Set up WINE prefix
WINEARCH=win32 WINEPREFIX="/opt/wdctools/" wineboot

# Extract WDCTOOLS.exe manually via 7zip
7z x WDCTOOLS.exe -o/opt/wdctools/drive_c/wdc
find /opt/wdctools/

# Output a wine/xvfb-run wrapper
echo -e '#!/bin/bash\nset -x\n(cd /opt/wdctools/drive_c/wdc/Tools/bin/ && WINEARCH=win32 WINEPREFIX="/opt/wdctools/" wine WDC816CC.exe $@)' > /usr/local/bin/wdc816cc
chmod +x /usr/local/bin/wdc816cc

# Run it once to confirm it is ok - if something is wrong then 'empty.obj' will not be created
echo '' > /tmp/empty.c
/usr/local/bin/wdc816cc /tmp/empty.c
rm /tmp/empty.c /tmp/empty.obj

# Ensure wineserver32 is no longer running - socket files confuse Docker
pgrep --exact wineserver32 && killall --wait --exact wineserver32 || true
