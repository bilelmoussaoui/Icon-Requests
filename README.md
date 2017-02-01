[![Build Status](https://travis-ci.org/bil-elmoussaoui/Icon-Requests.svg?branch=master)](https://travis-ci.org/bil-elmoussaoui/Icon-Requests)
# Icon Requests
A Gtk application to report missing icons to your current theme github repository

### Screenshots
<img src="screenshots/screenshot1.png" width="280" /> <img src="screenshots/screenshot2.png" width="280"/> <img src="screenshots/screenshot3.png"  width="280" />


### Install
- Archlinux (AUR):
```bash
yaourt -S icon-requests
```


### Build from source code
1 - Clone the repository
```bash
git clone https://github.com/bil-elmoussaoui/Icon-Requests && cd ./Icon-Requests
```
2 - Install dependecies
  - meson (git version for now)
  - requests
  - python3-cairosvg or inkscape
  - Pillow

3 - Build the application
```bash
mkdir build && cd ./build
meson ..
ninja
sudo ninja install
```
4 - Run the application!
