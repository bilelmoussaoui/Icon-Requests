from os import path, environ as env
from gi import require_version
from io import BytesIO
from subprocess import Popen, PIPE, call
from shutil import copyfile
from glob import glob
require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gio, GLib
try:
    require_version('Rsvg', '2.0')
    from gi.repository import Rsvg
    import cairo
    use_inkscape = False
except (ImportError, AttributeError):
    ink_flag = call(['which', 'inkscape'], stdout=PIPE, stderr=PIPE)
    if ink_flag == 0:
        use_inkscape = True
    else:
        exit("Can't load cariosvg nor inkscape")


def copy_file(src, destination, overwrite=False):
    """
    Simple copy file function with the possibility to overwrite the file.
    Args :
        src(str) : source file
        dest(str) : destination folder
        overwrite(bool) : True to overwrite the file False by default
    """
    if overwrite:
        if path.isfile(destination):
            remove(destination)
        copyfile(src, destination)
    else:
        if not path.isfile(destination):
            copyfile(src, destination)


def change_icon_name(desktop_file, icon_name):
    config = RawConfigParser()
    config.read(desktop_file)
    config.set("Desktop Entry", "Icon", icon_name)


def is_gnome():
    """
        Check if the current distro is gnome
    """
    return env.get("XDG_CURRENT_DESKTOP").lower() == "gnome"


def get_supported_icons():
    theme_name = Gio.Settings.new(
        "org.gnome.desktop.interface").get_string("icon-theme")
    icons_paths = [
        '{0}/.icons/{1}/'.format(GLib.get_home_dir(), theme_name),
        '{0}/.local/share/icons/{1}/'.format(GLib.get_home_dir(), theme_name),
        '/usr/local/share/icons/{0}/'.format(theme_name),
        '/usr/share/icons/{0}/'.format(theme_name),
    ]
    subdirs = []
    icons_dirs = ["apps", "applications", "web"]
    size_dirs = ["48", "48x48"]
    for size in size_dirs:
        for icon_dir in icons_dirs:
            subdirs.append("{0}/{1}/".format(size, icon_dir))
    icons = []
    extensions = [".svg" , ".png", ".xpm"]
    for icon_path in icons_paths:
        for icon_size in subdirs:
            icons_dir = icon_path + icon_size
            if path.exists(icons_dir):
                for ext in extensions:
                    folder_icons.extend(glob("{0}*{1}".format(icons_dir, ext)))
                for icon in folder_icons:
                    icon = path.basename(icon)
                    for ext in extensions:
                        icon = icon.replace(ext, "")
                    if icon not in icons:
                        icons.append(icon)
            folder_icons = []
    return icons

def convert_svg2png(infile, outfile, w, h):
    """
        Converts svg files to png using Cairosvg or Inkscape
        @file_path : String; the svg file absolute path
        @dest_path : String; the png file absolute path
    """
    if use_inkscape:
        p = Popen(["inkscape", "-z", "-f", infile, "-e", outfile,
                   "-w", str(w), "-h", str(h)],
                  stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
    else:
        handle = Rsvg.Handle()
        svg = handle.new_from_file(infile)
        dim = svg.get_dimensions()

        img = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        ctx = cairo.Context(img)
        ctx.scale(w / dim.width, h / dim.height)
        svg.render_cairo(ctx)

        png_io = BytesIO()
        img.write_to_png(png_io)
        with open(outfile, 'wb') as fout:
            fout.write(png_io.getvalue())
        svg.close()
        png_io.close()
        img.finish()


def get_icon(icon_path):
    """
        Generate a GdkPixbuf image
        :param image: icon name or image path
        :return: GdkPixbux Image
    """
    icon = GdkPixbuf.Pixbuf.new_from_file(icon_path)
    if icon.get_width() != 48 or icon.get_height() != 48:
        icon = icon.scale_simple(48, 48, GdkPixbuf.InterpType.BILINEAR)
    return icon
