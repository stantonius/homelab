# mostly from https://gist.github.com/utkonos/718b150de4f86054c37ac798c02b54c6

import io
import pathlib
import argparse
import pycdlib

def ubuntu_autoinstall(source: str, target: str):
    """Add an autoinstall file to an Ubuntu ISO image.
    source: path to the autoinstall file
    target: path for the new ISO image that will be created
    """

    assert source.split('.')[-1] == 'iso', 'source must be an iso file'
    assert target.split('.')[-1] == 'iso', 'target must be an iso file'

    ubuntu = pathlib.Path(source)
    new_iso = pathlib.Path(target)

    iso = pycdlib.PyCdlib()
    iso.open(ubuntu)

    # 1. Replace GRUB config
    extracted = io.BytesIO()
    iso.get_file_from_iso_fp(extracted, iso_path='/BOOT/GRUB/GRUB.CFG;1')
    extracted.seek(0)
    data = extracted.read()
    print(data.decode())

    new = data.replace(b' ---', b' autoinstall ds=nocloud;s=/cdrom/nocloud/ ---')
    print(new.decode())

    iso.rm_file(iso_path='/BOOT/GRUB/GRUB.CFG;1', rr_name='grub.cfg')
    iso.add_fp(io.BytesIO(new), len(new), '/BOOT/GRUB/GRUB.CFG;1', rr_name='grub.cfg')

    # 2. Do again for the loopback.cfg
    extracted = io.BytesIO()
    iso.get_file_from_iso_fp(extracted, iso_path='/BOOT/GRUB/LOOPBACK.CFG;1')
    extracted.seek(0)
    data = extracted.read()
    print(data.decode())

    new = data.replace(b' ---', b' autoinstall ds=nocloud;s=/cdrom/nocloud/ ---')
    print(new.decode())

    iso.rm_file(iso_path='/BOOT/GRUB/LOOPBACK.CFG;1', rr_name='loopback.cfg')
    iso.add_fp(io.BytesIO(new), len(new), '/BOOT/GRUB/LOOPBACK.CFG;1', rr_name='loopback.cfg')

    # 3. Do for isolinux bootloader if amd64
    extracted = io.BytesIO()
    iso.get_file_from_iso_fp(extracted, iso_path='/ISOLINUX/TXT.CFG;1')
    extracted.seek(0)
    data = extracted.read()
    print(data.decode())

    new = data.replace(b' ---', b' autoinstall ds=nocloud;s=/cdrom/nocloud/ ---')
    print(new.decode())

    iso.rm_file(iso_path='/ISOLINUX/TXT.CFG;1', rr_name='txt.cfg')
    iso.add_fp(io.BytesIO(new), len(new), '/ISOLINUX/TXT.CFG;1', rr_name='txt.cfg')


    iso.add_directory('/NOCLOUD', rr_name='nocloud')

    # with open("/var/lib/vz/snippets/user-data", "rb") as f:
    #     iso.add_fp(io.BytesIO(f.read()), len(f.read()), '/NOCLOUD/USER_DATA;1', rr_name='user-data')

    user_data = b"""
#cloud-config
autoinstall:
  version: 1
  network:
    version: 2
    ethernets:
      ens18:
        dhcp4: true
  locale: en_US.UTF-8
  keyboard:
    layout: us
  identity:
    hostname: "ubuntu-server"
    username: "ubuntu"
    password: "$6$exDY1mhS4KUYCE/2$zmn9ToZwTKLhCw.b4/b.ZRTIZM30JZ4QrOQ2aOXJ8yk96xpcCof0kxKwuX1kqLG/ygbJ1f8wxED22bTL4F46P0"
  ssh:
    allow-pw: false
    install-server: true
    authorized_keys:
      - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFPsnf+jir942UpHZFPaQ8C7Gfoo0jmLtdA7wbgnpkw9 craig@MBP.lan
  package_upgrade: true
  refresh-installer:
    update: yes
  storage:
    layout:
      name: lvm
    """

    iso.add_fp(io.BytesIO(user_data), len(user_data), '/NOCLOUD/USER_DATA;1', rr_name='user-data')
    iso.add_fp(io.BytesIO(b''), len(b''), '/NOCLOUD/META_DATA;1', rr_name='meta-data')
    iso.write(new_iso)
    iso.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add autoinstall to Ubuntu ISO')
    parser.add_argument('source', help='source iso file')
    parser.add_argument('target', help='target iso file')
    args = parser.parse_args()
    ubuntu_autoinstall(args.source, args.target)