import sublime
import sublime_plugin
import re
import os
import json

# sublime.log_commands(True)
# sublime.log_input(True)
# window.run_command("show_overlay", {"overlay": "goto", "show_files": True})
# sublime.windows()
# /opt/sublime_text/sublime.py
# subl --command "insert {\"characters\": \"Hello, World\"}"
# subl --command "set_project_folder"
# subl --command "set_tabs_file {\"window_id\": \"3\", \"file\": \"ui/src/models/company.coffee\"}"
# subl --command "save_tabs_file"
# bytearray('insert {"characters": "Hello, World"}'.encode())
# bytearray('"save_tabs_file"'.encode())
# bytearray("{'cmd': 'insert', 'shell':False}".encode())

# save_tabs_file 
# [int(ii, 16) for ii in '07 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 0e 00 00 00 73 61 76 65 5f 74 61 62 73 5f 66 69 6c 65 00 01 00 00 00 00 00 00 00'.split(' ')]
# dbus-monitor "interface='com.sublimehq.px.CommandLine'"

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
