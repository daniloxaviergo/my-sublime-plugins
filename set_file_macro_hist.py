import sublime
import sublime_plugin
import re
import os

class SetFileMacroHistCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    current_project_folder = open("/home/danilo/scripts/current_project_folder", "r").read()
    projectfolder = current_project_folder.split("\n")[1]

    outt = os.popen("find " + projectfolder + "spec/ -type f -printf '%T@ %p\\0' | sort -zk 1nr | sed -z 's/^[^ ]* //' | tr '\\0' '\\n' | head -n 50").read()
    outt = re.sub(projectfolder, '', outt)

    self.files = outt.split("\n")
    self.files.pop()
    self.show_quick_panel(self.files, self.view.window())

  def show_quick_panel(self, files, window):
    window.show_quick_panel(files, self.on_done)

  def on_done(self, index):
    #  if user cancels with Esc key, do nothing
    #  if canceled, index is returned as  -1
    if index == -1:
      return

    wids = open("/home/danilo/scripts/file_name_4", "w")
    wids.write(self.files[index])
    wids.close()
