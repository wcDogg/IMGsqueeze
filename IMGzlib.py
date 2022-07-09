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


class IMGzlib(IMGsqueeze):
  '''Lossless Zlib compression for JPEG, PNG and TIFF.
  '''
  def __init__(self, dir_proc, zlib):
    super().__init__()

    self.task = f'{configure.ZLIB_MACH}-{str(zlib)}'
    self.dir_proc = dir_proc
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

          # Compress the image
          opened.save(this.path_out, compress_level=self.zlib)
        
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
  print(f'[white]{inspect.cleandoc(configure.ZLIB_ASCII)}')
  print(f'[blue]{msgs.div}')
  print(configure.ZLIB_DESC)
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
    zlib: int = typer.Option(
      default=configure.ZLIB_DEFAULT, 
      min=0, 
      max=9, 
      help=configure.ZLIB_HELP
    )
):
  '''Launches task from command line.
  '''
  hello()
  typer.echo(f"directory {directory}")
  typer.echo(f"--zlib {zlib}")

  typer.echo(msgs.hr)
  conf = Confirm.ask(configure.TASK_CONF, default=True)
  if not conf:
      print(f'[red]{msgs.task_stopped}')
      print(msgs.hr)
      raise typer.Exit()

  print(f'Starting task. [yellow]{msgs.task_stop}')
  task = IMGzlib(directory, zlib)


if __name__ == "__main__":
    typer.run(main)

