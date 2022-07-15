import logging
log = logging.getLogger(__name__)

import imagequant
import inspect
from pathlib import Path
from PIL import Image
from rich import print
from rich.prompt import Confirm
import typer
import warnings
warnings.filterwarnings("ignore", category=Image.DecompressionBombWarning)

from IMGsqueeze import IMGsqueeze
from IMGimage import IMGimage
import configure
from helpers import msgs


class IMGquant(IMGsqueeze):
  '''Quantize for JPEG, PNG and TIFF with Zlib compression
  '''
  def __init__(self, directory, colors, dither, zlib):
    super().__init__()

    self.task = f'{configure.QUANT_MACH}_colors-{str(colors)}_dither-{str(dither)}_zlib-{str(zlib)}'
    self.dir_proc = directory
    self.colors = colors
    self.dither = dither
    self.zlib = zlib

    self.run()


  def run(self):
    '''The primary controller method for this class.
    '''
    try: 
      if not self.preflight():
        self.goodbye()
        return
      self.process_images()
      self.postlfight()
      self.goodbye()

    except KeyboardInterrupt:
      self.stopped()
      
    except Exception as e:
      self.error(repr(e))
      return

  def process_images(self):
    '''Compress images in self.files.
    '''
    print(msgs.hr)
    print(msgs.proc_start)
    print(f'[yellow]{msgs.task_stop}')
    f_on = 0

    for f in self.files:
      f_on += 1
      print(msgs.hr)
      print(f'Processing {f_on} of {len(self.files)}: {f}')

      this = IMGimage(f)
      this.path_in = Path(self.dir_proc.joinpath(f)) 
      this.path_out = Path(self.dir_save.joinpath(f)) 

      if not this.check_is_file():
        self.files_results.append(this.__dict__)
        this.print_results()
        continue

      if not this.check_max_mb():
        self.files_results.append(this.__dict__)
        this.print_results()
        continue

      try:
        with Image.open(this.path_in) as opened:

          if not this.check_format(opened):
            self.files_results.append(this.__dict__)
            this.print_results()
            continue

          if not this.check_max_pixels(opened):
            self.files_results.append(this.__dict__)
            this.print_results()
            continue

          # Quantize the image
          new = imagequant.quantize_pil_image(opened, max_colors=self.colors,         
                                              dithering_level=self.dither)
          if this.format_in == 'JPEG':
            new = new.convert('RGB')

          new.save(this.path_out, compress_level=self.zlib)

        # If we've made it this far, check the saved file
        this.check_saved()
        this.print_results()
        self.files_results.append(this.__dict__)

      # In case file makes it past find_files()
      except Image.UnidentifiedImageError:
        this.proc_result = configure.PROC_ERROR
        this.proc_msg = configure.PROC_MSG_NOT_IMAGE
        this.print_results()
        self.files_results.append(this.__dict__)

      except Exception as e:
        this.proc_result = configure.PROC_ERROR
        this.proc_msg = configure.PROC_MSG_SOURCE_ERROR
        print(repr(e))
        this.print_results()
        self.files_results.append(this.__dict__)


#
# Run this puppy :)
def hello():
  '''Prints the app banner to console.
  '''
  print(f'[blue]{msgs.div}')
  print(f'[white]{inspect.cleandoc(configure.QUANT_ASCII)}')
  print(f'[blue]{msgs.div}')
  print(configure.QUANT_DESC)
  print(f'{configure.APP_NAME}: {configure.APP_REPO}')
  print(msgs.hr)

def main(
    directory: Path = typer.Argument(
      ...,
      exists=True,
      file_okay=False,
      dir_okay=True,
      writable=True,
      readable=True,
      resolve_path=True,
      help=configure.DIR_HELP
    ),
    colors: int = typer.Option(
      default=configure.QUANT_DEFAULT_COLORS, 
      min=1, 
      max=256, 
      help=configure.QUANT_HELP_COLORS
    ),
    dither: float = typer.Option(
      default=configure.QUANT_DEFAULT_DITHER, 
      min=0, 
      max=1, 
      help=configure.QUANT_HELP_DITHER
    ),
    zlib: int = typer.Option(
      default=configure.ZLIB_DEFAULT,
       min=0, 
       max=9, 
       help=configure.ZLIB_HELP
    )
):
  '''Quantize JPEG, PNG, and TIFF. Optional Zlib compression.
  '''
  # Logging
  import logging
  from helpers import logger
  logger.setup_logging()
  log = logging.getLogger(__name__)

  # Hello + confirm
  hello()
  typer.echo(f"directory {directory}")
  typer.echo(f"--colors {colors}")
  typer.echo(f"--dither {dither}")
  typer.echo(f"--zlib {zlib}")

  typer.echo(msgs.hr)
  conf = Confirm.ask(configure.TASK_CONF, default=True)
  if not conf:
      print(f'[red]{msgs.task_stopped}')
      print(msgs.hr)
      raise typer.Exit()

  # Start
  print(f'Starting task. [red]{msgs.task_stop}')
  task = IMGquant(directory, colors, dither, zlib)


if __name__ == "__main__":
    typer.run(main)

