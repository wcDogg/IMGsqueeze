import logging
log = logging.getLogger(__name__)

import filetype
from os import listdir
from pathlib import Path
from rich import print

import configure
from helpers import msgs
from helpers.TaskTimer import TaskTimer


class IMGsqueeze:
  '''Bulk process JPEG, PNG, and TIFF to reduce file size. 
  '''
  def __init__(self):
    log.debug('Start')

    self.task: str = None
    self.dir_proc: Path = None
    self.dir_save: Path = None
    self.task_log: Path = None
    self.timer = TaskTimer()

    self.files = []
    self.files_processed = []
    self.files_not_processed = []
    self.files_error = []
    self.files_mb_warn = []

    self.task_summary = {}
    self.timer_summary = {}
    self.files_summary = {}
    self.mb_summary = {}
    self.files_results = []

    log.debug('End')

  #
  # Pre-flight methods
  def preflight(self):
    '''Runs all of the pre-flight methods.
    Returns bool indicating if file processing can continue.
    '''
    log.debug('Start')

    if not self.get_files():
      log.debug('End: False')
      return False

    self.set_paths()

    if not self.prep_dir_save():
      log.debug('End: False')
      return False

    self.prep_task_log()
    self.timer_start()
    log.debug('End: True')
    return True

  def get_files(self):
    '''Gathers a list of JPEG, PNG, and TIFF files in dir_proc.
    Returns bool indicating if there are images to process.
    '''
    log.debug('Start')
    print(msgs.hr)
    print(f'{msgs.files_start}')

    if not listdir(self.dir_proc):
      print(f'[yellow]{msgs.files_false}')
      log.debug('End: False: No files found')
      return False

    temp = []

    for f in listdir(self.dir_proc):
      path = Path(self.dir_proc.joinpath(f)) 

      if path.is_file():
        guess = filetype.guess(path)
        if guess and guess.mime in configure.MIME_TYPES:
          temp.append(f)

    if not temp:
      print(f'[yellow]{msgs.files_false}')
      log.debug('End: False: No files found')
      return False

    self.files = temp
    print(f'[green]{len(self.files)} {msgs.files_true}')
    log.debug(f'End: True: {len(self.files)} files found')
    return True 
  
  def set_paths(self):
    '''Sets paths to dir_save and task_log.
    '''
    log.debug('Start')
    _proc_name = self.dir_proc.name
    _proc_parent = self.dir_proc.parent
    _save_name = _proc_name + '_' + self.task

    self.dir_save = Path(_proc_parent / _save_name)
    self.task_log = Path(self.dir_save / 'task.log')

    log.debug(self.dir_save)
    log.debug(self.task_log)
    log.debug('End')

  def prep_dir_save(self):
    '''Creates dir_save if it doesn't exist.
    Returns bool indicating if directory is ready for output.
    '''
    log.debug('Start')
    print(msgs.hr)
    print(f'{msgs.dir_save_start}')

    try: 
      if not self.dir_save.is_dir():
        self.dir_save.mkdir(parents=True, exist_ok=True)

      print(f'[green]{self.dir_save}')
      log.debug(f'End: True: {self.dir_save}')
      return True 

    except Exception as e:
      print(f'[red]{msgs.dir_save_error}')
      print(repr(e))
      log.error('End: Error')
      log.error(e)
      return False

  def prep_task_log(self):
    '''Tries to create a task.log file inside 
    dir_save if it doesn't exist.
    '''
    log.debug('Start')
    print(msgs.hr)
    print(msgs.log_prep)

    try:       
      if not self.task_log.is_file():
        self.task_log.write_text(msgs.log_ready)

      print(f'[green]{self.task_log}')
      log.debug(f'End: {self.task_log}')

    except Exception as e:
      self.task_log = None
      print(f'[red]{msgs.log_prep_error}')
      log.error('End: error')
      log.error(e)

  #
  # Task timer
  def timer_start(self):
    '''Starts the image processing timer. Captures the start time.
    '''
    self.timer.start()

  def timer_stop(self):
    '''Stops the image processing timer. Captures the stop + elapsed times.
    '''
    self.timer.stop()
    self.timer.elapsed()

  #
  # Post-flight methods
  def postlfight(self):
    '''Runs all of the post-flight methods.
    '''
    log.debug('Start')
    self.timer_stop()
    self.gather_task_data()
    self.write_log()
    self.write_console()
    log.debug('End')

  def gather_task_data(self):
    ''''Assembles various task data into summary dictionaries.
    '''
    log.debug('Start')
    print(msgs.hr)
    print(msgs.proc_end)
    print(msgs.log_gather)

    # Task
    self.task_summary['task'] = self.task
    self.task_summary['dir_proc'] = self.dir_proc
    self.task_summary['dir_save'] = self.dir_save
    self.task_summary['task_log'] = self.task_log

    # Timer
    self.timer_summary = self.timer.timer_results

    # Files
    if self.files_results: 
      for d in self.files_results:
        if d['proc_result'] == configure.PROC_TRUE:
          self.files_processed.append(d['file'])
        if d['proc_result'] == configure.PROC_FALSE:
          self.files_not_processed.append(d['file'])
        if d['proc_result'] == configure.PROC_ERROR:
          self.files_error.append(d['file'])
        if d['mb_warn'] == True:
          self.files_mb_warn.append(d['file'])

      self.files_summary['files_found'] = len(self.files)
      self.files_summary['files_processed'] = len(self.files_processed)
      self.files_summary['files_not_processed'] = len(self.files_not_processed)
      self.files_summary['files_error'] = len(self.files_error)
      self.files_summary['files_mb_warn'] = len(self.files_mb_warn)

    # MB
    if self.files_results: 
      mb_in = []
      mb_out = []

      for d in self.files_results:
        mb_in.append(d['mb_in'])
        mb_out.append(d['mb_out'])
    
      self.mb_summary['mb_in'] = round(sum(mb_in), 2)
      self.mb_summary['mb_out'] = round(sum(mb_out), 2)
      self.mb_summary['mb_change'] = round((sum(mb_out)-sum(mb_in)), 2)

      percent = (((sum(mb_out)/sum(mb_in))*100)-100)
      self.mb_summary['mb_change_percent'] = round(percent, 2)

    log.debug('End')

  def write_console(self):
    '''Writes the various task-level summaries to console.
    '''
    log.debug('Start')

    # Task summary
    print(msgs.hr)
    print(f'TASK SUMMARY')
    for k, v in self.task_summary.items():
      print(f'{k}: {v}')
        
    # Timer summary
    print(msgs.hr)
    print(f'TIME SUMMARY')
    for k, v in self.timer_summary.items():
      print(f'{k}: {v}')

    # Files summary
    print(msgs.hr)
    print(f'FILES SUMMARY')
    for k, v in self.files_summary.items():
      print(f'{k}: {v}')

    # MB summary
    print(msgs.hr)
    print(f'MB SUMMARY')
    for k, v in self.mb_summary.items():
      print(f'{k}: {v}')
    
    log.debug('End')

  def write_log(self):
    '''Writes the task.log file.
    '''
    log.debug('Start')

    if not self.task_log:
      log.debug('End: Task log False')
      return

    print(msgs.log_write)

    try: 
      with Path.open(self.task_log, 'r+') as opened:
        # Store any existing results
        existing = opened.read()
        # Write new results at top
        opened.seek(0)

        # Task summary
        opened.write(msgs.div_nl) 
        opened.write(f'TASK SUMMARY\n')
        for k, v in self.task_summary.items():
          opened.write(f'{k}: {v}\n') 
            
        # Timer summary
        opened.write(msgs.hr_nl)
        opened.write(f'TIME SUMMARY\n')
        for k, v in self.timer_summary.items():
          opened.write(f'{k}: {v}\n')  

        # Files summary
        opened.write(msgs.hr_nl)
        opened.write(f'FILES SUMMARY\n')
        for k, v in self.files_summary.items():
          opened.write(f'{k}: {v}\n')

        # List found
        if self.files:
          opened.write(msgs.hr_nl)
          opened.write(f'FILES FOUND\n')
          for f in self.files:
            opened.write(f'{f}\n')

        # List processed
        if self.files_processed: 
          opened.write(msgs.hr_nl)
          opened.write(f'FILES PROCESSED\n')
          for f in self.files_processed:
            opened.write(f'{f}\n')

        # List not processed
        if self.files_not_processed: 
          opened.write(msgs.hr_nl)
          opened.write(f'FILES NOT PROCESSED\n')
          for f in self.files_not_processed:
            opened.write(f'{f}\n')

        # List errors
        if self.files_error:
          opened.write(msgs.hr_nl)
          opened.write(f'FILES ERROR\n')
          for f in self.files_error:
            opened.write(f'{f}\n')

        # MB summary
        if self.files_processed: 
          opened.write(msgs.hr_nl)
          opened.write(f'MB SUMMARY\n')
          for k in self.mb_summary:
            opened.write(f'{k}: {self.mb_summary[k]}\n') 

        # MB warnings
        if self.files_mb_warn:
          opened.write(msgs.hr_nl)
          opened.write(f'FILES WITH INCREASED MB\n')
          for f in self.files_mb_warn:
            opened.write(f'{f}\n')

        # Processing details
        if self.files_results: 
          opened.write(msgs.hr_nl)
          opened.write(f'FILE PROCESSING RESULTS\n')
          for d in self.files_results:
            opened.write(msgs.hr_nl)
            for k, v in d.items(): 
              opened.write(f'{k}: {v}\n')

        # Append prior results
        opened.write(msgs.div_nl)
        opened.write(existing)
      
      log.debug('End: File written')

    except Exception as e:
      print(f'[red]{msgs.log_write_error}')
      print(repr(e))
      log.error('End: error')
      log.error(e)

  #
  # Endings
  def stopped(self):
    '''Famous last words.
    '''
    self.timer_stop()
    print('\n')
    print(msgs.hr)
    print(f'[red]{msgs.task_stopped}')
    print(msgs.div) 
    log.debug('Goodbye stopped')   

  def error(self, error):
    '''Famous last words.
    '''
    self.timer_stop()
    print(msgs.hr)
    print(error)
    print(msgs.hr)
    print(f'[red]{msgs.task_error}')
    print(msgs.div)
    log.debug('Goodbye error')

  def goodbye(self):
    '''Famous last words.
    '''
    print(msgs.hr)
    print(f'[green]{msgs.task_end}')
    print(msgs.div) 
    log.debug('Goodbye')  

