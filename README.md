# Icon Requests
A Gtk application to report missing icons to your current theme github repository

### Screenshots
<img src="screenshots/screenshot1.png" width="280" /> <img src="screenshots/screenshot2.png" width="280"/> <img src="screenshots/screenshot3.png"  width="280" />

## Dependencies

### Building Dependencies:
  - `meson`
  - `ninja`

### Running Dependencies:
  - `python-requests`
  - `imagemagick`
  - `gtk 3.16+`
  - `python 3.3+`


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

3 - Build the application
```bash
meson builddir --prefix=/usr
sudo ninja -C builddir install
```
4 - Run the application
```bash
icon-requests
```