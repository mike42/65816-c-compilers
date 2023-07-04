FROM ubuntu:22.04 as builder

WORKDIR /build

# install node
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -qq install curl gcc g++ make build-essential && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    DEBIAN_FRONTEND=noninteractive apt-get -qq install -y nodejs && \
    node --version

# run front-end build
COPY frontend frontend/
RUN cd frontend && \
    npm install && \
    npm run build

RUN pwd && find frontend/dist/

FROM ubuntu:22.04

# Install anything we need from the package manager, including cc65 open source compiler (6502 target only)
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -qq install python3-venv libtinfo5 cc65 wine32 wine64 xvfb p7zip-full wget libnuma1 psmisc

COPY /installers /installers

# Install proprietary compilers which scripts can fetch themselves
RUN cd installers && \
    ./install-calypsi-6502.sh && \
    ./install-calypsi-65816.sh

# Install proprietary wdc816cc compiler, which must be individually obtained from https://wdc65xx.com/WDCTools
# The install script requires WDCTOOLS.exe to be present in the installers/ directory
RUN cd installers && \
    ./install-wdc816cc.sh

# Install proprietary ORCA/C compiler & tools, running under the Golden Gate compatibility layer, which must both be
# purchased from the Juiced.GS Store.
#  - https://juiced.gs/store/opus-ii-software/
#  - https://juiced.gs/store/golden-gate/
# The install script requires the file 'ByteWorks' and 'Golden Gate.msi' to be present in the installers/ directory.
RUN cd installers && \
    ./install-orca.sh

WORKDIR /app
COPY backend backend
COPY requirements.txt .
COPY --from=builder build/frontend/dist/web-compiler-frontend/ ./backend/static
RUN python3 -m venv venv/ && \
    ls && \
    ./venv/bin/pip install -r requirements.txt

CMD ['./venv/bin/python3', 'backend/main.py']
