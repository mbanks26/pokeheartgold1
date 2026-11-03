#!/bin/bash
set -euo pipefail
mkdir -p /workspace/.setup/apt/lists/partial /workspace/.setup/apt/cache/archives/partial /workspace/.setup/root /workspace/.setup/bin
cat > /workspace/.setup/apt/sources.list <<'SETUP_EOF'
deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://deb.debian.org/debian trixie main
SETUP_EOF
cat > /workspace/.setup/apt/apt.conf <<'SETUP_EOF'
Dir::Etc::main "-";
Dir::Etc::parts "-";
Dir::Etc::sourcelist "/workspace/.setup/apt/sources.list";
Dir::Etc::sourceparts "-";
Dir::State "/workspace/.setup/apt";
Dir::State::status "/var/lib/dpkg/status";
Dir::State::lists "/workspace/.setup/apt/lists";
Dir::Cache "/workspace/.setup/apt/cache";
APT::Sandbox::User "agent";
SETUP_EOF
cat > /workspace/.setup/activate.sh <<'SETUP_EOF'
export PATH=/workspace/.setup/root/usr/bin:$PATH
export LD_LIBRARY_PATH=/workspace/.setup/root/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export PKG_CONFIG_PATH=/workspace/.setup/root/usr/lib/x86_64-linux-gnu/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}
export PKG_CONFIG_SYSROOT_DIR=/workspace/.setup/root
export BISON_PKGDATADIR=/workspace/.setup/root/usr/share/bison
export NINJAFLAGS=-j4
export PKG_CONFIG_PATH_FOR_BUILD="$PKG_CONFIG_PATH"
export PKG_CONFIG_SYSROOT_DIR_FOR_BUILD="$PKG_CONFIG_SYSROOT_DIR"
export PATH=/workspace/.setup/bin:$PATH
export M4=/workspace/.setup/root/usr/bin/m4
SETUP_EOF
cat > /workspace/.setup/bin/ninja <<'SETUP_EOF'
#!/bin/sh
exec /workspace/.setup/root/usr/bin/ninja -j4 "$@"
SETUP_EOF
cat > /workspace/.setup/prepare-toolchain.py <<'SETUP_EOF'
from pathlib import Path
import subprocess
root=Path('/workspace/pokeheartgold1/tools/metroskrew/bin')
for f in list(root.iterdir()):
    if '.elf32' in f.name or not f.is_file():
        continue
    if f.read_bytes()[:5] != b'\x7fELF\x01':
        continue
    subprocess.run(['/workspace/.setup/root/usr/bin/patchelf','--set-interpreter','/workspace/.setup/root/usr/lib32/ld-linux.so.2','--set-rpath','/workspace/.setup/root/usr/lib32',str(f)],check=True)
    real=f.with_name(f.name+('.elf32.exe' if f.name.endswith('.exe') else '.elf32'))
    f.rename(real)
    f.write_text('#!/bin/sh\nexec /workspace/.setup/root/usr/bin/qemu-i386 "'+str(real)+'" "$@"\n')
    f.chmod(0o755)
SETUP_EOF
chmod +x /workspace/.setup/bin/ninja
export APT_CONFIG=/workspace/.setup/apt/apt.conf
/usr/bin/apt-get update
cd /workspace/.setup/apt/cache/archives
/usr/bin/apt-get download ninja-build nasm bison flex gcc-arm-none-eabi binutils-arm-none-eabi libc6-i386 libpng-dev libpng16-16t64 zlib1g-dev patchelf libfl2 libfl-dev qemu-user m4
for package in *.deb; do dpkg-deb -x "$package" /workspace/.setup/root; done
source /workspace/.setup/activate.sh
cd /workspace/pokeheartgold1
make skrew meson
python3 /workspace/.setup/prepare-toolchain.py
mkdir -p subprojects/packagecache
curl -fL --max-time 60 https://github.com/mesonbuild/wrapdb/releases/download/yyjson_0.12.0-1/yyjson_0.12.0-1_patch.zip -o subprojects/packagecache/yyjson_0.12.0-1_patch.zip
printf '%s\n' '014582b328e13671dea64fcb49a795e70142360216a505212b8045134781b3b5  subprojects/packagecache/yyjson_0.12.0-1_patch.zip' | sha256sum -c -
make
