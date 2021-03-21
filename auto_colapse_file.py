import sublime
import sublime_plugin
import os
import json

class AutoColapseFileOnSave(sublime_plugin.EventListener):
  def on_load(self, view):
    filename = view.file_name()

    str_json = open("/home/danilo/scripts/foldfiles.json", "r").read()
    jjson = json.loads(str_json)
    fold_level = jjson.get(filename)
    if fold_level:
      view.run_command('fold_by_level', {"level": fold_level})
    else:
      view.run_command('fold_by_level', {"level": 4})
