import sys
import logging
from zind.api.file_filter_token import FilterToken
from zind.api.text_token import TextToken

class Loader:

  def __init__(self):
    self._file_filter_tokens = []
    self._text_tokens = []
    self._directory = "."
    self._output_mode = None # Options are 'filepath', 'filepath-force' or 'filecontent'
    self._suppress_output = True

  def print_arg_error(self, bad_arg):
    print("Error: Unknown input argument: " + bad_arg)

  def print_help(self):
    print("Basic Usage: ")
    print("\t\t[-g INCLUSIVE_MATCH ] \t# Include filepaths with matching pattern.")
    print("\t\t[-ge EXCLUSIVE_MATCH ] \t# Exclude filepaths with matching pattern.")
    print("\t\t[-t EXCLUSIVE_MATCH ] \t# Include filepaths containing matching text.")
    print("\t\t[-te EXCLUSIVE_MATCH ] \t# Exclude filepaths containing matching text.")
    print("\t\t[-d directory ] \t# Directory to run in.")
    print("\t\t[-ha ] \t\t\t# Print advanced usage.")

  def print_advanced_help(self):
    self.print_help()
    print()
    print("Advanced Usage: ")
    print("\t\t[-g<erfc> MATCH_TOKEN ] \t# Prints matching filepaths.")
    print("\t\t[-t<erfc> MATCH_TOKEN ] \t# Prints lines within files that match.")
    print("\t\t[-k ] \t# Keep output as filename only.")
    print("\t\t[-a ] \t# Do not suppress output.")
    print("Optional argument modifiers")
    print("Options -g and -t can have extra arguments to form an advanced argument, e.g. '-gfce token'): ")
    print("\t\t e \t# Exclude instead of include matches.")
    print("\t\t r \t# Match regex pattern instead of text match.")
    print("\t\t c \t# Case sensitive matches.")
    print("\t\t f \t# Match filename only.")

  def run(self):

    # Setup logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.WARN)

    input_file_key = None
    input_text_key = None
    input_directory = False
    index = 1
    for index in range(1, len(sys.argv)):
      arg = sys.argv[index]

      if(input_file_key != None):
        parsed = self._load_file_filter_token(input_file_key, arg)
        if(not parsed):
          self.print_arg_error(sys.argv[index -1])
          self.print_help()
          return False
        else:
          input_file_key = None
      elif(input_text_key != None):
        parsed = self._load_text_token(input_text_key, arg)
        if(not parsed):
          self.print_arg_error(sys.argv[index -1])
          self.print_help()
          return False
        else:
          input_text_key = None
      elif(input_directory):
        self._directory = arg
        input_directory = False
      elif(arg.startswith('-g')):
        input_file_key = arg[2:]
      elif(arg.startswith('--g')):
        input_file_key = arg[3:]
      elif(arg.startswith('-t')):
        input_text_key = arg[2:]
      elif(arg.startswith('--t')):
        input_text_key = arg[3:]
      elif(arg == '-h' or arg == '--help'):
        self.print_help()
        return False
      elif(arg == '-ha' or arg == '--help-advanced'):
        self.print_advanced_help()
        return False
      # Must check '-vv' before '-v'
      elif(arg.startswith('-vv')):
        logging.getLogger().setLevel(logging.DEBUG)
      elif(arg.startswith('-v')):
        logging.getLogger().setLevel(logging.INFO)
      elif(arg.startswith('-d')):
        input_directory = True
      elif(arg.startswith('-k')):
        self._output_mode = "filepath-force"
      elif(arg.startswith('-a')):
        self._suppress_output = False
      else:
        self.print_arg_error(arg)
        self.print_help()
        return False

    if(self._output_mode is None or len(self._text_tokens) == 0):
      self._output_mode = "filepath"
      
    if(input_file_key is not None):
      print("Error: match token must follow expression '" + sys.argv[index] + "'")
      self.print_help()
      return False

    return True
    
  def _load_file_filter_token(self, input_file_key, token):
    input_chars = [char for char in input_file_key]

    inclusive = True
    regex = False
    filename_only = False
    case_sensitive = False

    for char in input_chars:
      if(char == "e"):
        inclusive = False
      elif(char == "r"):
        regex = True
      elif(char == "f"):
        filename_only = True
      elif(char == "c"):
        case_sensitive = True
      else:
        return False

    filter_token = FilterToken(token, inclusive, regex, filename_only, case_sensitive)
    self._file_filter_tokens.append(filter_token)
    return True

  def _load_text_token(self, input_text_key, token):
    input_chars = [char for char in input_text_key]

    inclusive = True
    regex = False
    case_sensitive = False
    if (self._output_mode is None):
      self._output_mode = "filecontent"

    for char in input_chars:
      if(char == "e"):
        inclusive = False
      elif(char == "r"):
        regex = True
      elif(char == "c"):
        case_sensitive = True
      else:
        return False

    text_token = TextToken(token, inclusive, regex, case_sensitive)
    self._text_tokens.append(text_token)
    return True

  def get_output_mode(self):
    return self._output_mode

  def get_suppress_output(self):
    return self._suppress_output

  def get_file_filter_tokens(self):
    return self._file_filter_tokens

  def get_text_tokens(self):
    return self._text_tokens

  def get_directory(self):
    return self._directory
