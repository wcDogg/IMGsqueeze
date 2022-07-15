import logging
log = logging.getLogger(__name__)

from pathlib import Path
from PIL import Image
from rich import print

import configure
from helpers import msgs


class IMGimage:
  '''Stores data for a single image.
  '''
  def __init__(self, file):
    log.debug('Start')

    self.file = file
    self.path_in: Path = None
    self.path_out: Path = None

    self.format_in: str = None
    self.mode_in: str = None

    self.format_out: str = None
    self.mode_out: str = None

    self.width_in: int = None
    self.height_in: int = None
    self.px_in: int = None

    self.width_out: int = None
    self.height_out: int = None
    self.px_out: int = None

    self.mb_in: float = None
    self.mb_out: float = None
    self.mb_change: float = None
    self.mb_change_percent: float = None
    self.mb_warn: bool = None

    self.proc_result: str = None
    self.proc_msg: str = None

    log.debug('End')

  def check_is_file(self):
    '''Returns bool indicating if file exists.
    '''
    log.debug('Start')

    if not self.path_in.is_file():
      self.proc_result = configure.PROC_ERROR
      self.proc_msg = configure.PROC_MSG_NOT_FOUND
      log.debug('End: False: Not a file')
      return False

    log.debug('End: True: Is a file')
    return True

  def check_max_mb(self):
    '''Returns bool indicating if file size is 
    less than or equal to the configured MAX_MB.
    '''
    log.debug('Start')
    self.mb_in = (self.path_in.stat().st_size)/1024/1024
    
    if self.mb_in > configure.MAX_MB:
      self.proc_result = configure.PROC_FALSE
      self.proc_msg = configure.PROC_MSG_MAX_PX
      log.debug(f'End: False: {self.mb_in} exceeds {configure.MAX_MB} MAX_MB')
      return False

    log.debug(f'End: True: {self.mb_in} MB')
    return True

  def check_format(self, opened):
    '''Returns bool indicating if file is a supported format.
    This check is in case file isn't caught by find_files(). 
    '''
    log.debug('Start')

    self.format_in = opened.format
    self.mode_in = opened.mode

    if self.format_in not in configure.FILE_FORMATS:
      self.proc_result = configure.PROC_FALSE
      self.proc_msg = configure.PROC_MSG_FORMAT
      log.debug(f'End: False: {self.format_in} is an unsupported format')
      return False

    log.debug(f'End: True: {self.format_in}')
    return True

  def check_max_pixels(self, opened):
    '''Returns bool indicating if the total
    number of pixels is less than the configured MAX_PX.
    '''
    log.debug('Start')
    self.width_in = opened.width
    self.height_in = opened.height
    self.px_in = self.width_in * self.height_in

    if self.px_in > configure.MAX_PX:
      self.proc_result = configure.PROC_FALSE
      self.proc_msg = configure.PROC_FALSE
      log.debug(f'End: False: {self.path_in} exceeds {configure.MAX_PX} MAX_PX')
      return False

    return True

  def check_saved(self):
    '''Checks the saved image for errors and data.
    '''
    log.debug('Start')

    try: 
      self.mb_out = (self.path_out.stat().st_size)/1024/1024
      self.mb_change = round((self.mb_out - self.mb_in), 2)
      self.mb_change_percent = (((self.mb_out/self.mb_in)*100)-100)

      if self.mb_out > self.mb_in:
        self.mb_warn = True

      with Image.open(self.path_out) as opened:
        self.format_out = opened.format
        self.mode_out = opened.mode
        self.width_out = opened.width
        self.height_out = opened.height
        self.px_out = self.width_out * self.height_out
        self.proc_result = configure.PROC_TRUE

      log.debug('End')

    except Exception as e:
      self.proc_result = configure.PROC_ERROR
      self.proc_msg = configure.PROC_MSG_SAVED_ERROR
      log.debug('End: Error')
      log.error(e)

  def print_results(self):
    '''Prints data about this image to console.
    '''
    log.debug('Start')

    if self.proc_result == configure.PROC_TRUE:
      print(f'[green]{self.proc_result}')
    elif self.proc_result == configure.PROC_FALSE:
      print(f'[yellow]{self.proc_result}')
    else:
      print(f'[red]{self.proc_result}')

    if self.mb_warn:
      print(f'[yellow]{configure.PROC_MSG_MB_UP}')

    if self.proc_msg:
      print(f'{self.proc_msg}')
    
    print(msgs.hr)
    for k, v in self.__dict__.items():
      print(f'{k}: {v}')

    log.debug('Start')

