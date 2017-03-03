FROM ubuntu:16.04
RUN apt-get -y update
# Install dependecies
RUN apt-get install -y git python-gobject ninja python3-cairosvg python3-gi python3-pip python-dev libgtk-3-dev intltool gobject-introspection libgirepository1.0-dev gir1.2-gtk-3.0
RUN pip3 install requests Pillow meson

# Build Icon Requests using meson
RUN git clone https://github.com/bil-elmoussaoui/Icon-Requests
WORKDIR ./Icon-Requests
RUN mkdir build
WORKDIR ./build
RUN meson .. && ninja && sudo ninja install

CMD icon-requests --debug
