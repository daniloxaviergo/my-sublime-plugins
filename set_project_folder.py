import sublime
import sublime_plugin
import re
import os
import json

# sublime.log_commands(True)
# sublime.log_input(True)
# window.run_command('show_overlay', {"overlay": "goto", "show_files": True})
# sublime.windows()
# /opt/sublime_text/sublime.py

class SetProjectFolderCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    str_json = open("/home/danilo/scripts/projectfolder.json", "r").read()
    self.projectfolder = json.loads(str_json)

    self.files = []
    for folder in self.projectfolder:
      # file = folder['image'] + ' - ' + folder['path']
      file = [folder['image'], folder['path']]
      self.files.append(file)

    # print(self.files)
    self.show_quick_panel(self.files, self.view.window())

  def show_quick_panel(self, files, window):
    window.show_quick_panel(files, self.on_done, sublime.MONOSPACE_FONT)

  def on_done(self, index):
    #  if user cancels with Esc key, do nothing
    #  if canceled, index is returned as  -1
    if index == -1:
      return

    # print(index)
    # print(self.files[index])
    # print(self.projectfolder[index])
    self.files[index][1] = '/home/danilo/' + self.files[index][1]
    text = "\n".join(self.files[index])

    wids = open("/home/danilo/scripts/current_project_folder", "w")
    wids.write(text)
    wids.close()
