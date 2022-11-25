# mostly from https://gist.github.com/utkonos/718b150de4f86054c37ac798c02b54c6

import io
import pathlib

import pycdlib

ubuntu = pathlib.Path('ubuntu-22.04-live-server-amd64.iso')
new_iso = pathlib.Path('ubuntu-22.04-live-server-amd64-auto.iso')

iso = pycdlib.PyCdlib()
iso.open(ubuntu)

extracted = io.BytesIO()
iso.get_file_from_iso_fp(extracted, iso_path='/BOOT/GRUB/GRUB.CFG;1')
extracted.seek(0)
data = extracted.read()
print(data.decode())

new = data.replace(b'quiet ---', b'quiet autoinstall ---').replace(b'timeout=30', b'timeout=1')
print(new.decode())

iso.rm_file(iso_path='/BOOT/GRUB/GRUB.CFG;1', rr_name='grub.cfg')
iso.add_fp(io.BytesIO(new), len(new), '/BOOT/GRUB/GRUB.CFG;1', rr_name='grub.cfg')

iso.write(new_iso)
iso.close()