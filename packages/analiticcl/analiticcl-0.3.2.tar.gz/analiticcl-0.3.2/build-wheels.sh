#!/usr/bin/env sh
docker pull konstin2/maturin
docker run --rm -v $(pwd):/io konstin2/maturin build --release
#also build musl-compatible wheels for distros like Alpine Linux:
docker run --rm -v $(pwd):/io konstin2/maturin build --release --compatibility musllinux_1_1
