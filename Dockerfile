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

FROM ubuntu:22.04

# Install anything we need from the package manager, including cc65 (6502 target only)
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -qq install python3-venv libtinfo5 cc65 wine32 xvfb p7zip-full wget libnuma1 psmisc
    
COPY /installers /installers

# Install proprietary compilers which scripts can fetch themselves
RUN cd installers && \
    ./install-calypsi-6502.sh && \
    ./install-calypsi-65816.sh
    
# Install proprietary wdc816cc compiler, which must be individually obtained from https://wdc65xx.com/WDCTools
# The install script requires WDCTOOLS.exe to be present in the installers/
RUN cd installers && \
    ./install-wdc816cc.sh

WORKDIR /app
COPY backend .
COPY --from=builder frontend/build/dist/web-compiler-frontend/ ./static
RUN python3 -m venv venv/ && \
    ./venv/bin/pip install -r requirement.txt
COMMAND ['./venv/bin/python3', 'main.py']
