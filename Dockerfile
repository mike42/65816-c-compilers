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
    DEBIAN_FRONTEND=noninteractive apt-get -q -y install \
    cc65 \
    libavcodec58 \
    libavformat58 \
    libavutil56 \
    libc6-i386 \
    libegl1 \
    libfuse2 \
    libgif7 \
    libglu1 fuse \
    libglu1-mesa \
    libnuma1 \
    libtinfo5 \
    p7zip-full \
    psmisc \
    python3-venv \
    unar \
    unzip \
    wget \
    wine32 \
    wine64 \
    xvfb

COPY /installers /installers

# Install proprietary compilers, fetched via install script
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

# Install proprietary MPW IIgs tools, which must be purchased from the Juiced.GS store
# - https://juiced.gs/store/apda-software/
# The install script requires the file 'MPW IIgs.sit' to be present in the installers/ directory
RUN cd installers && \
    ./install-mpw.sh


WORKDIR /app
COPY backend backend
COPY requirements.txt .
COPY --from=builder build/frontend/dist/web-compiler-frontend/ ./backend/static
RUN python3 -m venv venv/ && \
    ./venv/bin/pip install -r requirements.txt

CMD ["./venv/bin/uvicorn", "backend.main:app", "--host", "0.0.0.0"]
