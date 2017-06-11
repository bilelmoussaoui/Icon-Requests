from os import path
from tempfile import NamedTemporaryFile
from PIL import Image
from abc import ABCMeta, abstractmethod
from io import BytesIO
from subprocess import Popen, PIPE, call
from gi import require_version
try:
    require_version('Rsvg', '2.0')
    from gi.repository import Rsvg
    from cairo import Context, ImageSurface, FORMAT_ARGB32
    use_inkscape = False
except (ImportError, AttributeError, ValueError):
    ink_flag = call(['which', 'inkscape'], stdout=PIPE, stderr=PIPE)
    if ink_flag == 0:
        use_inkscape = True
    else:
        exit("Can't load cariosvg nor inkscape")


class Upload:
    __metaclass__ = ABCMeta

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        self._client_id = client_id

    @abstractmethod
    def upload_icon(self, icon_path, app_name):
        """Upload the icon."""

    def upload(self, icon_path, app_name=None):
        icon_extension = path.splitext(icon_path)[1].lower().strip(".")
        was_scaled = False
        if icon_extension in ["svg", "png"]:
            outfile = NamedTemporaryFile().name
            if icon_extension == "svg":
                convert_svg2png(icon_path, outfile, 48, 48)
                icon_path = outfile
                was_scaled = True
                icon_extension = "png"
            if icon_extension == "png":
                if not was_scaled:
                    scale_png_image(icon_path, outfile, 48, 48)
                    icon_path = outfile
            icon_url = self.upload_icon(icon_path, app_name)
            return icon_url
        return None


def convert_svg2png(infile, outfile, w, h):
    """
        Converts svg files to png using Cairosvg or Inkscape
        @file_path : String; the svg file absolute path
        @dest_path : String; the png file absolute path
    """
    if use_inkscape:  # Using Inkscape
        Popen(["inkscape", "-z", "-f", infile, "-e", outfile,
               "-w", str(w), "-h", str(h)],
              stdout=PIPE, stderr=PIPE).communicate()
    else:  # Using Cairo & Rsvg
        handle = Rsvg.Handle()
        svg = handle.new_from_file(infile)
        dim = svg.get_dimensions()

        img = ImageSurface(FORMAT_ARGB32, w, h)
        ctx = Context(img)
        ctx.scale(w / dim.width, h / dim.height)
        svg.render_cairo(ctx)

        png_io = BytesIO()
        img.write_to_png(png_io)
        with open(outfile, 'wb') as fout:
            fout.write(png_io.getvalue())
        svg.close()
        png_io.close()
        img.finish()


def scale_png_image(inputfile, outfile, width, height):
    img = Image.open(inputfile)
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save(outfile, "PNG")
