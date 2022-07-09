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
import msgs


class IMGdown(IMGsqueeze):
  '''Downscale the pixel dimensions of JPEG, PNG and TIFF plus Zlib compression.
  '''
  def __init__(self, directory, algo, width, height, zlib):
    super().__init__()

    self.task = f'{configure.DOWN_MACH}_algo-{str(algo)}_width-{str(width)}_height-{str(height)}_zlib-{str(zlib)}'
    self.dir_proc = directory
    self.algo = algo
    self.ds_width = width
    self.ds_height = height
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

          # Just copy & compress the image
          if not self.check_ds_pixels(this.width_in, this.height_in):
            opened.save(this.path_out, compress_level=self.zlib)
          # Downscale image
          else: 
            new_width, new_height = self.calc_ds_dimensions(this.width_in, this.height_in)
            new = opened.resize((new_width, new_height), resample=self.algo)
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

  def check_ds_pixels(self, width, height):
    '''Returns bool indicating if image is larger 
    than the downscale dimensions and should be processed.
    '''
    # By width
    if not self.ds_height:
      if width <= self.ds_width:
        return False

    # By height
    if not self.ds_width:
      if height <= self.ds_height:
        return False

    # By both width and height
    if self.ds_width and self.ds_height:
      if width <= self.ds_width and height <= self.ds_height:
        return False

    return True
      
  def calc_ds_dimensions(self, width, height):
    '''Per-image calculation of new width 
    and height. Returns `(w,h)` tuple. 
    '''
    # By width
    if not self.ds_height:
      w = self.ds_width
      h = int(w * height / width)

    # By height
    if not self.ds_width:
      h = self.ds_height
      w = int(h * width / height)

    if self.ds_width and self.ds_height: 
      # Arbitrarily try width first.
      w = self.ds_width
      h = int(w * height / width)
      # Then compare to height and swap if necessary.
      if h > self.ds_height: 
        h = self.ds_height
        w = int(h * width / height)

    return (w, h)

#
# Run this puppy :)
def hello():
  '''Prints the app banner to console.
  '''
  print(f'[blue]{msgs.div}')
  print(f'[white]{inspect.cleandoc(configure.DOWN_ASCII)}')
  print(f'[blue]{msgs.div}')
  print(configure.DOWN_DESC)
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
    algo: int = typer.Option(
      default=configure.DOWN_DEFAULT_ALGO, 
      min=0, 
      max=5, 
      help=configure.DOWN_HELP_ALGO
    ),
    width: int = typer.Option(
      default=configure.DOWN_DEFAULT_WIDTH, 
      min=16, 
      help=configure.DOWN_HELP_WIDTH
    ),
    height: int = typer.Option(
      default=configure.DOWN_DEFAULT_HEIGHT, 
      min=16, 
      help=configure.DOWN_HELP_HEIGHT
    ),
    zlib: int = typer.Option(
      default=configure.ZLIB_DEFAULT, 
      min=0, 
      max=9, 
      help=configure.ZLIB_HELP
    )
):
  '''Downscale the pixel dimensions of JPEG, PNG and TIFF, plus Zlib compression.
  
  If only a --width or --height is given, images are downscaled to that dimension.

  If both are given, images are downscaled to fit within both dimensions. One dimension will = its max and the other dimension will be <= its max.
  '''
  if not width and not height:
    print(f'[red]{msgs.down_error_px}')
    raise typer.Exit()

  hello()
  typer.echo(f'directory {directory}')
  typer.echo(f'--algo {algo}')
  if width: 
    typer.echo(f'--width {width}')
  if height:
    typer.echo(f'--height {height}')
  typer.echo(f'--zlib {zlib}')

  typer.echo(msgs.hr)
  conf = Confirm.ask(configure.TASK_CONF, default=True)
  if not conf:
      print(f'[red]{msgs.task_stopped}')
      print(msgs.hr)
      raise typer.Exit()

  print(f'Starting task. [red]{msgs.task_stop}')
  task = IMGdown(directory, algo, width, height, zlib)


if __name__ == '__main__':
    typer.run(main)

