from os import listdir, path, getuid, environ as env
from gi import require_version
from pwd import getpwuid
require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gio
from subprocess import Popen, PIPE, call
from collections import OrderedDict
from shutil import copyfile
from IconRequests.modules.upload.imgur import imgur_upload_img
from tempfile import NamedTemporaryFile
from io import BytesIO
from PIL import Image
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


def get_user_destkop():
    p = Popen(["xdg-user-dir", "DESKTOP"], stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    return output.decode("utf-8").strip() + "/"


def get_username():
    return getpwuid(getuid())[0]

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

def upload_icon(icon_path, app_name):
    icon_extension = path.splitext(icon_path)[1].lower().strip(".")
    was_scaled = False
    if icon_extension in ["svg" ,"png"]:
        outfile = NamedTemporaryFile().name
        if icon_extension == "svg":
            convert_svg2png(icon_path, outfile, 48, 48)
            icon_name = outfile
            was_scaled = True
            icon_extension = "png"
        if icon_extension == "png":
            if not was_scaled:
                img = Image.open(icon_path)
                img = img.resize((48, 48), Image.ANTIALIAS)
                img.save(outfile, "PNG")
                icon_path = outfile
            icon_url = imgur_upload_img(icon_path, app_name)
            return icon_url
    return None


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
