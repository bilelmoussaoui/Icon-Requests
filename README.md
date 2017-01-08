# Icon Requests
A Gtk application to report missing icons to your current theme github repository

### Screenshots
<img src="screenshots/screenshot1.png" width="280" /> <img src="screenshots/screenshot2.png" width="280"/> <img src="screenshots/screenshot3.png"  width="280" />


### Build from source code
1 - Clone the repository
```bash
git clone https://github.com/bil-elmoussaoui/Icon-Requests && cd ./Icon-Requests
```
2 - Install dependecies
  - meson (git version for now)
  - pyimugr 

3 - Build the application
```bash
mkdir build && cd ./build
meson ..
ninja
sudo ninja install
```
4 - Run the application!
