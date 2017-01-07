# Numix-icon-report
A Gtk application to report missing icons to Numix-core repository 

### Screenshots
<img src="screenshots/screenshot1.png" width="280" /> <img src="screenshots/screenshot2.png" width="280"/> <img src="screenshots/screenshot3.png"  width="280" />


### Build from source code
1 - Clone the repository 
```bash
git clone https://github.com/bil-elmoussaoui/Numix-icon-report && cd ./Numix-icon-report
```
2 - Install meson (git version for now)

3 - Build the application
```bash
mkdir build && cd ./build
meson ..
ninja 
sudo ninja install 
```
4 - Run the application! 
