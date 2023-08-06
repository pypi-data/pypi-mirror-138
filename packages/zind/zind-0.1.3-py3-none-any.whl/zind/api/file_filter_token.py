class FilterToken:

  def __init__(self, token, is_inclusive, is_regex, is_filename_only, is_case_sensitive):
    self._token = token
    self._is_inclusive = is_inclusive
    self._is_regex = is_regex
    self._is_filename_only = is_filename_only
    self._is_case_sensitive = is_case_sensitive
    pass

  def get_token(self):
    return self._token

  def is_inclusive(self):
    return self._is_inclusive

  def is_regex(self):
    return self._is_regex

  def is_filename_only(self):
    return self._is_filename_only

  def is_case_sensitive(self):
    return self._is_case_sensitive

  def __str__(self):
    return self._token + " (inclusive=" + str(self._is_inclusive) + " regex=" + str(self._is_regex) + " filenameOnly=" + str(self._is_filename_only) + " caseSensitive=" + str(self._is_case_sensitive) + ")"
