# IMGsqueeze

Python 3.10+ command line tools to reduce the file size of JPEG, PNG, and TIFF files in bulk. 

* [IMGzlib](#zlib-lossless-compression) - Lossless Zlib compression
* [IMGquant](#quantize-plus-zlib) - Reduce color palette
* [IMGdown](#downscale-plus-zlib) - Downscale pixel dimensions

I wrote IMGsqueeze for 2 broad use cases:

* Reducing file size while maintaining high visual quality.
* Producing intentionally low-res images for things like product listings (anti-scraping tactic).

## Hell No!

* No uploading to a web service. No privacy concerns. No Internet needed.
* No processing limitations like with free services - and even some paid ones.
* No paying for subscription services that include dozens of conversion types you'll never use. 

## Hell Yeah!

### Bulk Processing

* IMGsqueeze tools work on directories. 
* Files directly inside a directory are subject to processing. 
* Subdirectories are ignored.
* The directory can contain a mix of file formats - no need to pre-sort.
* Non-image files + unsupported image formats are ignored. 
* Format is determined by MIME type - and not file extension.

### Pillow Options

Because I wrote IMGsqueeze for 2 opposing reasons, the tools offer most of Pillow's built-in options. For example, there's no good use case for a Zlib level below 6, but there's no logic preventing it. Similarly, you can choose which downscaling algorithm to use. 

One notable exception is with quantize. While the baked-in Pillow method let's you select an algorithm, it has crappy dither options. Here I decided to force the use of LIBIMAGEQUNT because a) it's by far the best RGB algorithm and b) its method allows full dither control. 

### Smart Saving

* IMGsqueeze automatically creates a save directory alongside the proc directory.
* The save directory's name reflects the task & settings. This makes it easy to compare different combinations without the hassle of renaming folders or accidentally overwriting the source directory. 
* IMGsqueeze is non-destructive - images are copied then processed. Original files are unchanged. 
* Filenames are unchanged, so it's easy to update images in existing projects - I hate prefixes and suffixes.

### Helpful Logging

* Processing results are written to the terminal and to a `task.log` inside the save directory.
* Task-level summaries make it easy to spot potential problems - like files that weren't processed or that resulted in a larger file size. 
* Image-specific results include pre- and post-processing data for easy comparison and troubleshooting. 

## VS Code venv

1. Clone repo and open directory in VS Code.
2. In VS Code Bash terminal:

```
# Create venv - adds folder to project.
py -3 -m venv venv

# Activate venv - no visual confirmation.
venv/Scripts/activate.bat

# Command Palette > Python Select Interpreter > Enter Interpreter Path
# Browse to and select: /project/venv/Scripts/python.exe
# Kill / new Bash terminal.

# Do a sanity check.
which pip3

# Install requirements.
py -m pip install -r requirements.txt --upgrade
```

## Test Directories

This repo contains a `test-images` directory. Here you can also view sample `task.log` files.

```
"D:\CornDoggSoup\IMGsqueeze\test-images\jpeg" 
"D:\CornDoggSoup\IMGsqueeze\test-images\png"
"D:\CornDoggSoup\IMGsqueeze\test-images\tiff"
"D:\CornDoggSoup\IMGsqueeze\test-images\other"
```

## [IMGzlib](docs/zlib.md)

```
py IMGzlib.py --help

# Default max 9 zlib
py IMGzlib.py "D:\GitHub\IMGsqueeze\test-images\jpeg"

# Options
py IMGzlib.py --zlib 7 "D:\CornDoggSoup\IMGsqueeze\test-images\jpeg" 
```

## [IMGquant](docs/quantize.md)

```
py IMGquant.py --help

# Default 256 colors, 1.0 dither, 9 zlib
py IMGquant.py "D:\CornDoggSoup\IMGsqueeze\test-images\jpeg"

# Options
py IMGquant.py --colors 64 --dither 0.5 --zlib 7 "D:\CornDoggSoup\IMGsqueeze\test-images\jpeg"
```

## [IMGdown](docs/downscale.md)

```
py IMGdown.py --help

# By width, default LANCZOS, 9 zlib
py IMGdown.py --width 800 "D:\CornDoggSoup\IMGsqueeze\test-images\jpeg"

# By height, default LANCZOS, 9 zlib
py IMGdown.py --height 800 "D:\CornDoggSoup\IMGsqueeze\test-images\jpeg"

# By width + height, default LANCZOS, 9 zlib
py IMGdown.py --width 800 --height 700 "D:\CornDoggSoup\IMGsqueeze\test-images\jpeg"

# By width, BICUBIC, 7 zlib
py IMGdown.py --algo 3 --width 800 --zlib 7 "D:\CornDoggSoup\IMGsqueeze\test-images\jpeg"
```

