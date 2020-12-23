
import os, sys
import argparse
from PIL import Image, features


# Initiate the parser
parser = argparse.ArgumentParser()

# Add long and short argument
parser.add_argument("--path", "-p", help="Resimleri içeren klasör", required=True)
parser.add_argument("--quality", "-q", help="Kalite 0-100 arasında değer alıyor", required=False, default=80)


# Read arguments from the command line
args = parser.parse_args()

sizes = [(1024,1024)]


if not features.check("webp_anim") :
    sys.exit("Webp desteklenmiyor.")


for infile in os.listdir(args.path):
    f, e = os.path.splitext(infile)
    if e != "WebP":
        try:
            with Image.open(os.path.join(args.path, infile)) as im:
                for size in sizes:
                    im.thumbnail(size)
                    out_put = os.path.join(args.path, f"{f}_{im.size[0]}x{im.size[1]}.WebP")                     
                    im.save(out_put, format = "WebP", minimize_size=True, method=6, quality= args.quality)
        except OSError as e:
            print("cannot convert", infile, str(e))

