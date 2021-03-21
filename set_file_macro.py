import sublime
import sublime_plugin
import re

class SetFileMacroCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    current_project_folder = open("/home/danilo/scripts/current_project_folder", "r").read()
    projectfolder = current_project_folder.split("\n")[1]

    file_name = re.sub(projectfolder, '', self.view.file_name())
    
    wids = open("/home/danilo/scripts/file_name_4", "w")
    wids.write(file_name)
    wids.close()
