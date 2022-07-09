#
# App 
APP_NAME = "IMGsqueeze"
APP_DESC = 'Python tools to reduce the size of JPEG, PNG, and TIFF files.'
APP_REPO = 'https://github.com/wcDogg/IMGsqueeze'
AUTHOR_NAME = 'wcDogg'
AUTHOR_URL = 'https://github.com/wcDogg'

#
# Supported file formats.
FILE_FORMATS = ['JPEG', 'TIFF', 'PNG']
MIME_TYPES = ['image/jpeg', 'image/tiff', 'image/png']

#
# Max file size to process. Out-of-range are skipped. 
MAX_MB = 60

#
# Max width * height px to process.
# Decompression bomb threshold.
MAX_PX = 144000000

#
# Task
DIR_HELP = 'The path to a directory with images to process.'
TASK_CONF = 'Are the options above correct?'

#
# Zlib
ZLIB_HUMAN = 'IMGzlib'
ZLIB_MACH = 'zlib'
ZLIB_DESC = 'Lossless Zlib compression for JPEG, PNG, and TIFF.'
ZLIB_DEFAULT = 9  # 9 max
ZLIB_HELP = 'An integer from 0 (no compression) to 9 (max compression). Below 6 is ineffective and more likely to increase file size.'

#
# Quantize
QUANT_HUMAN = 'IMGquant'
QUANT_MACH = 'quant'
QUANT_DESC = 'Quantize JPEG, PNG, and TIFF. Optional Zlib compression.'
QUANT_DEFAULT_COLORS = 256   # 256
QUANT_DEFAULT_DITHER = 1.00  # 1.00
QUANT_HELP_COLORS = 'The max number of colors to retain. An integer from 1 (grayscale) to 256 (max colors).'
QUANT_HELP_DITHER = 'The level of halftones applied to gradients. A float from 0.00 (polygons) to 1.00 (full halftones).'

#
# Downscale
DOWN_HUMAN = 'IMGdown'
DOWN_MACH = 'down'
DOWN_DESC = 'Downscale pixel dimensions of JPEG, PNG, and TIFF. Optional Zlib compression.'
DOWN_DEFAULT_WIDTH = None  # None
DOWN_DEFAULT_HEIGHT = None # None
DOWN_DEFAULT_ALGO = 1      # 1 LANCZOS

DOWN_HELP_ALGO = 'The numeric ID of the downscale algorithm: 0 NEAREST, 1 LANCZOS, 2 BILINEAR, 3 BICUBIC, 4 BOX, 5 HAMMING'
DOWN_HELP_WIDTH = 'The maximum width in pixels.'
DOWN_HELP_HEIGHT = 'The maximum height in pixels.'

#
# An image is either processed or not.
PROC_TRUE = 'Processed'
PROC_FALSE = 'Not processed'
PROC_ERROR = 'Error'
# And here are the reasons why:
PROC_MSG_NOT_FOUND = 'File not found'
PROC_MSG_NOT_IMAGE = 'File is not an image'
PROC_MSG_MAX_MB = f'File exceeds the {MAX_MB} MB max'
PROC_MSG_MAX_PX = f'File exceeds the {MAX_PX} max'
PROC_MSG_FORMAT = 'Unsupported image format'
PROC_MSG_SOURCE_ERROR = 'Error with source image'
PROC_MSG_SAVED_ERROR = 'Error with saved image'
PROC_MSG_MB_UP = 'File size increased'

#
# ASCII art (O8)
# https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20

ZLIB_ASCII = '''
ooooo oooo     oooo  ooooooo8             o888  o88   oooo        
 888   8888o   888 o888    88 ooooooooooo  888  oooo   888ooooo   
 888   88 888o8 88 888    oooo     8888    888   888   888    888 
 888   88  888  88 888o    88   8888       888   888   888    888 
o888o o88o  8  o88o 888ooo888 o888ooooooo o888o o888o o888ooo88   
'''

DOWN_ASCII = '''
ooooo oooo     oooo  ooooooo8         oooo                                     
 888   8888o   888 o888    88    ooooo888   ooooooo  oooo  o  oooo oo oooooo   
 888   88 888o8 88 888    oooo 888    888 888     888 888 888 888   888   888  
 888   88  888  88 888o    88  888    888 888     888  888888888    888   888  
o888o o88o  8  o88o 888ooo888    88ooo888o  88ooo88     88   88    o888o o888o 
'''


QUANT_ASCII = '''  
ooooo oooo     oooo  ooooooo8                                                 o8   
 888   8888o   888 o888    88    ooooooooo oooo  oooo   ooooooo   oo oooooo o888oo 
 888   88 888o8 88 888    oooo 888    888   888   888   ooooo888   888   888 888   
 888   88  888  88 888o    88  888    888   888   888 888    888   888   888 888   
o888o o88o  8  o88o 888ooo888    88ooo888    888o88 8o 88ooo88 8o o888o o888o 888o 
                                      888o                                         
'''

