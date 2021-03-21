import sublime
import sublime_plugin
import os
import json

class DecreaseFoldCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filename = self.view.file_name()

    str_json = open("/home/danilo/scripts/foldfiles.json", "r").read()
    jjson = json.loads(str_json)
    fold_level = jjson.get(filename)

    self.view.run_command('move_to', {"to": "bof", "extend": False})

    if fold_level and fold_level > -1:
      self.decrease_and_save(fold_level, jjson)
    else:
      self.decrease_and_save(7, jjson)

  def decrease_and_save(self, fold_level, jjson):
    fold_level = int(fold_level) - 1
    jjson[self.view.file_name()] = fold_level
    foldfiles = open("/home/danilo/scripts/foldfiles.json", "w")
    foldfiles.write(json.dumps(jjson))
    foldfiles.close()

    self.view.run_command('unfold_all')
    self.view.run_command('fold_by_level', {"level": fold_level})

    self.view.show_popup(
      '{fold_level}'.format(fold_level=fold_level),
      flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
    )

    # script = '/home/danilo/scripts/dmenu/dzen_monitor.sh'
    # os.popen("{script} 2 {fold_level}".format(script=script, fold_level=fold_level)).read()
