from zind.api.core_find import Find
from zind.api.core_text_find import TextFind
from zind.input.loader import Loader
import logging

class Runner:

  def __init__(self):
    self._suppress_line_length = 2000

  def run(self):

    try:

      loader = Loader()
      continue_run = loader.run()
      if(not continue_run):
        return

      file_filter_tokens = loader.get_file_filter_tokens()
      for file_filter_token in file_filter_tokens:
        logging.debug("File filter token: " + str(file_filter_token))
        

      find = Find()
      text_find = TextFind()

      scan_directory = loader.get_directory()
      file_matches = find.find(scan_directory, file_filter_tokens)

      output_mode = loader.get_output_mode()

      self._printed_warning = False

      for file_match in file_matches:
        if(output_mode.startswith("filepath")):
          if(output_mode == "filepath-force"):
            if(not file_match.endswith('/')):
              # In this mode, there must be at least one matching line
              lines = text_find.scan(file_match, loader.get_text_tokens())
              for line in lines:
                self.print_line(file_match, loader)
                break # Print the filename once
          else:
            print(file_match)
        elif(not file_match.endswith('/')):
          lines = text_find.scan(file_match, loader.get_text_tokens())
          for line in lines:
            self.print_line(file_match + ": " + line.rstrip(), loader)

    except KeyboardInterrupt:
      pass

  def print_line(self, text, loader):
    if(len(text) < self._suppress_line_length or not loader.get_suppress_output()):
      print(text)
    elif(not self._printed_warning):
      print()
      print("[WARNING] Suppressed matching line because it was too long, disable this behavior with -s")
      print()
      self._printed_warning = True

def main():
  runner = Runner()
  runner.run()
