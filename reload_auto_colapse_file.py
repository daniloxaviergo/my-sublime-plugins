import sublime
import sublime_plugin
import re
import json

class ReloadAutoColapseFileCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filename = self.view.file_name()

    str_json = open("/home/danilo/scripts/foldfiles.json", "r").read()
    jjson = json.loads(str_json)
    fold_level = jjson.get(filename)

    if fold_level:
      self.view.run_command('fold_by_level', {"level": fold_level})
    else:
      self.view.run_command('fold_by_level', {"level": 4})
