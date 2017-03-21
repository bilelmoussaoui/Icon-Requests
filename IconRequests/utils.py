from os import path, makedirs, remove
from gi import require_version
import requests
import json
from urllib.parse import urlencode
from IconRequests.const import ISSUES_PER_PAGE, NB_PAGES
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
except (ImportError, AttributeError, ValueError):
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
        Check if the current desktop env is gnome
    """
    return GLib.getenv("XDG_CURRENT_DESKTOP").lower() == "gnome"


def is_app_menu():
    """
    Check if the top application menu is enabled or not.
    """
    default = True
    try:
        gsettings = Gio.Settings.new('org.gnome.settings-daemon.plugins.xsettings')
        overrides = gsettings.get_value('overrides')['Gtk/ShellShowsAppMenu']
        show_app_menu = not bool(GLib.Variant.new_int32(overrides))
    except Exception:
        show_app_menu = default
    return show_app_menu


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
    size_dirs = ["48", "48x48", "scalable"]
    for size in size_dirs:
        for icon_dir in icons_dirs:
            subdirs.append("{0}/{1}/".format(size, icon_dir))
            subdirs.append("{0}/{1}/".format(icon_dir, size))
    icons = []
    folder_icons = []
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
    try:
        if "symbolic" in icon_path:
            icon = (None, icon_path)
        else:
            icon = GdkPixbuf.Pixbuf.new_from_file(icon_path)
            if icon.get_width() != 48 or icon.get_height() != 48:
                icon = icon.scale_simple(48, 48, GdkPixbuf.InterpType.BILINEAR)
        return icon
    except GLib.Error:
        return None

def get_issues_list(repository):
    """
        Get a list of open issues on a repository.
    """
    cache_dir = path.join(GLib.get_user_cache_dir(), "IconRequests", "")
    cache_file = path.join(cache_dir, "{0}.json".format(repository.replace("/", "-")))
    if not path.exists(cache_dir):
        makedirs(cache_dir)
    issues_list = []
    url_data = {
        "state" : "open",
        "per_page": str(ISSUES_PER_PAGE),
        "page" : "1"
    }
    base_uri = "https://api.github.com/repos/{0}/issues?".format(repository)
    for page in range(1, NB_PAGES + 1):
        url_data["page"] = str(page)
        try:
            query = requests.get(base_uri + urlencode(url_data))
            issues_list.extend(query.json())
        except requests.exceptions.ConnectionError:
            issues_list = []
            break
    if len(issues_list) != 0 and not isinstance(issues_list[0], str):
        if path.exists(cache_file):
            remove(cache_file)
        with open(cache_file, 'w') as file_object:
            json.dump(issues_list, file_object, sort_keys=True, indent=4)
        file_object.close()
    else:
        if path.exists(cache_file):
            with open(cache_file, 'r') as file_object:
                issues_list = json.load(file_object)
            file_object.close()
    return issues_list
